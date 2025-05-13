console.log("Social media frontend loaded.");

document.addEventListener('DOMContentLoaded', function() {
    const likeButtons = document.querySelectorAll('.like-button');

    likeButtons.forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();
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
            .then(response => response.json())
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
                }
            })
            .catch(error => console.error('Error:', error));
        });
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
