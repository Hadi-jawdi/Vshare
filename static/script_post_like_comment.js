console.log("Social media frontend loaded.");

document.addEventListener('DOMContentLoaded', function() {
    const container = document.querySelector('#posts-feed'); // container for posts feed

    container.addEventListener('click', function(event) {
        if (event.target.closest('.like-button')) {
            event.preventDefault();
            const button = event.target.closest('.like-button');
            const postCard = button.closest('.post');
            const postId = postCard.getAttribute('data-post-id');
            const liked = button.getAttribute('data-liked') === 'True';

            fetch('/like/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: `post_id=${postId}`
            })
            .then(response => {
                if (!response.ok) {
                    console.error('Like request failed with status:', response.status);
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.liked !== undefined) {
                    button.setAttribute('data-liked', data.liked ? 'True' : 'False');
                    const likeCountSpan = button.querySelector('.like-count');
                    likeCountSpan.textContent = data.total_likes;
                    if (data.liked) {
                        button.querySelector('i').classList.remove('fa-regular');
                        button.querySelector('i').classList.add('fa-solid');
                    } else {
                        button.querySelector('i').classList.remove('fa-solid');
                        button.querySelector('i').classList.add('fa-regular');
                    }
                } else if (data.error) {
                    console.error('Like request error:', data.error);
                }
            })
            .catch(error => console.error('Error:', error));
        }

        if (event.target.closest('.comment-toggle')) {
            event.preventDefault();
            const toggle = event.target.closest('.comment-toggle');
            const postCard = toggle.closest('.post');
            const commentsSection = postCard.querySelector('.comments-section');
            if (commentsSection.style.display === 'none' || commentsSection.style.display === '') {
                commentsSection.style.display = 'block';
                loadComments(postCard);
            } else {
                commentsSection.style.display = 'none';
            }
        }
    });

    function loadComments(postCard) {
        const postId = postCard.getAttribute('data-post-id');
        const commentsList = postCard.querySelector('.comments-list');
        commentsList.innerHTML = '<p>Loading comments...</p>';

        fetch(`/comments/${postId}/`)
            .then(response => {
                if (!response.ok) {
                    console.error('Get comments failed with status:', response.status);
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
.then(data => {
    commentsList.innerHTML = '';
    if (data.comments.length === 0) {
        commentsList.innerHTML = '<p>No comments yet.</p>';
    } else {
        data.comments.forEach(comment => {
            const commentDiv = document.createElement('div');
            commentDiv.classList.add('comment');
            commentDiv.innerHTML = `
                <div class="comment-header" style="display: flex; align-items: center; margin-bottom: 5px;">
                    <img src="${comment.profile_image_url}" alt="Profile Image" style="width: 30px; height: 30px; border-radius: 50%; object-fit: cover; margin-right: 8px;">
                    <strong>${comment.author}</strong>
                    <small style="margin-left: auto; font-size: 0.8em; color: #666;">${comment.created_at}</small>
                </div>
                <p>${comment.content}</p>
            `;
            commentsList.appendChild(commentDiv);
        });
    }
})
            .catch(error => {
                commentsList.innerHTML = '<p>Error loading comments.</p>';
                console.error('Error:', error);
            });
    }

    // Handle comment form submission
    container.addEventListener('submit', function(event) {
        if (event.target.classList.contains('comment-form')) {
            event.preventDefault();
            const form = event.target;
            const postCard = form.closest('.post');
            const postId = postCard.getAttribute('data-post-id');
            const textarea = form.querySelector('textarea[name="content"]');
            const content = textarea.value.trim();
            if (!content) {
                alert('Comment cannot be empty.');
                return;
            }

            fetch('/add_comment/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                body: `post_id=${postId}&content=${encodeURIComponent(content)}`
            })
            .then(response => {
                if (!response.ok) {
                    console.error('Add comment failed with status:', response.status);
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    textarea.value = '';
                    loadComments(postCard);
                } else {
                    alert('Error submitting comment.');
                    console.error('Add comment error:', data.errors);
                }
            })
            .catch(error => {
                alert('Error submitting comment.');
                console.error('Error:', error);
            });
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
