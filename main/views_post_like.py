from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import UserProfile
from .models_post_like_fixed import Post
from .forms import PostForm
from .forms import ProfileEditForm


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


@login_required
def home(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    posts = Post.objects.select_related('author__profile').all().order_by('-created_at')
    # Annotate each post with user_has_liked attribute
    for post in posts:
        post.user_has_liked = post.likes.filter(id=user.id).exists()
    post_form = PostForm()
    return render(request, 'index_post_like.html', {'profile': profile, 'posts': posts, 'post_form': post_form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Post created successfully.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'post_form': form})


@login_required
def profile(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = None
    posts = Post.objects.filter(author=user).order_by('-created_at')
    for post in posts:
        post.user_has_liked = post.likes.filter(id=user.id).exists()
    return render(request, 'profile.html', {'profile': profile, 'posts': posts})


@login_required
def profile_edit(request):
    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=user)
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileEditForm(instance=profile, user=user)
    return render(request, 'profile_edit.html', {'form': form})


@login_required
def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        return JsonResponse({'liked': liked, 'total_likes': post.total_likes()})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


@login_required
def notifications(request):
    return render(request, 'notifications.html')


from .models import UserProfile, Message
from .forms import PostForm, ProfileEditForm, MessageForm
from django.db.models import Q

@login_required
def messages_view(request):
    user = request.user
    message_form = MessageForm()
    selected_user = None
    messages = []

    # Get list of users who have messaged or been messaged by the current user
    conversation_users = User.objects.filter(
        Q(sent_messages__receiver=user) | Q(received_messages__sender=user)
    ).distinct()

    # Prepare conversation users with latest message preview
    conversation_previews = []
    for u in conversation_users:
        latest_message = Message.objects.filter(
            (Q(sender=user) & Q(receiver=u)) | (Q(sender=u) & Q(receiver=user))
        ).order_by('-timestamp').first()
        conversation_previews.append({
            'user': u,
            'latest_message': latest_message,
        })

    # Get all users except the current user
    all_users = User.objects.exclude(id=user.id)

    if request.method == 'POST':
        message_form = MessageForm(request.POST)
        selected_user_id = request.POST.get('selected_user_id')
        if selected_user_id:
            selected_user = User.objects.filter(id=selected_user_id).first()
        if message_form.is_valid() and selected_user:
            message = message_form.save(commit=False)
            message.sender = user
            message.receiver = selected_user
            message.save()
            message_form = MessageForm()  # reset form after sending

    else:
        selected_user_id = request.GET.get('user')
        if selected_user_id:
            selected_user = User.objects.filter(id=selected_user_id).first()

    if selected_user:
        messages = Message.objects.filter(
            (Q(sender=user) & Q(receiver=selected_user)) |
            (Q(sender=selected_user) & Q(receiver=user))
        ).order_by('timestamp')

    return render(request, 'messages.html', {
        'conversation_users': conversation_users,
        'conversation_previews': conversation_previews,
        'selected_user': selected_user,
        'messages': messages,
        'message_form': message_form,
        'all_users': all_users,
    })
