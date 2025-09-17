document.addEventListener("DOMContentLoaded", function () {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const htmlTag = document.documentElement;

    // Detect system preference if no saved theme
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    const savedTheme = localStorage.getItem("theme") || (prefersDark ? "dark" : "light");

    // Apply theme on load
    htmlTag.setAttribute("data-bs-theme", savedTheme);
    updateIcon(savedTheme);

    // Toggle on button click
    themeToggle.addEventListener("click", function () {
        const currentTheme = htmlTag.getAttribute("data-bs-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        htmlTag.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);
        updateIcon(newTheme);
    });

    // Helper to update icon
    function updateIcon(theme) {
        themeIcon.className = theme === "dark" ? "bi bi-sun-fill" : "bi bi-moon-fill";
    }
});


// Likes handling
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.like-form').forEach(form => {
        const button = form.querySelector('.like-btn');
        button.addEventListener('click', function (e) {
            e.preventDefault(); // prevent any default form submission

            const tweetId = form.dataset.id;
            const csrftoken = form.querySelector('[name=csrfmiddlewaretoken]').value;

            fetch(`/like/${tweetId}/`, {  // Correct URL
                method: 'POST',
                headers: { 'X-CSRFToken': csrftoken },
            })
            .then(res => res.json())
            .then(data => {
                if (data.likes_count !== undefined) {
                    form.querySelector('.like-count').textContent = data.likes_count;
                } else if (data.error) {
                    alert(data.error);
                }
            })
            .catch(err => console.error('Error:', err));
        });
    });
});

