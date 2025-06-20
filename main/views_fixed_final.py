{% extends "base.html" %}
{% block title %}Social Media Website{% endblock %}
{% block content %}
    <div class="row">
        <!-- Posts feed -->
        <div class="col-lg-8 mb-4">
            <h2>Feed</h2>
            {% for post in posts %}
            <div class="post card mb-3" data-post-id="{{ post.id }}">
                <div class="card-body">
                    <h5 class="card-title">{{ post.author.username }}</h5>
                    <h6 class="card-subtitle mb-2 text-muted">{{ post.created_at|timesince }} ago</h6>
                    <p class="card-text">{{ post.content }}</p>
                    <a href="#" class="card-link like-button" data-liked="{{ post.has_liked(user) }}">
                        <i class="fa-regular fa-thumbs-up"></i> Like (<span class="like-count">{{ post.total_likes }}</span>)
                    </a>
                    <a href="#" class="card-link"><i class="fa-regular fa-comment"></i> Comment</a>
                </div>
            </div>
            {% empty %}
            <p>No posts available.</p>
            {% endfor %}
        </div>

        <!-- User profile sidebar -->
        <div class="col-lg-4">
            <div class="card sticky-top" style="top: 80px;">
                <div class="card-body text-center">
                    {% if profile and profile.profile_image %}
                        <img src="{{ profile.profile_image.url }}" alt="User Avatar" class="rounded-circle img-fluid mb-3 border border-primary shadow" style="max-width: 100px; height: auto;" />
                    {% else %}
                        <img src="https://via.placeholder.com/100" alt="User Avatar" class="rounded-circle img-fluid mb-3 border border-primary shadow" style="max-width: 100px; height: auto;" />
                    {% endif %}
                    <h5 class="card-title">{{ user.username }}</h5>
                    <p class="card-text">Bio: {{ profile.bio|default:"No bio available." }}</p>
                    <a href="{% url 'profile_edit' %}" class="btn btn-primary btn-sm">Edit Profile</a>
                </div>
            </div>
        </div>
    </div>
{% endblock %}
