document.addEventListener("DOMContentLoaded", function() {
    const themeToggle = document.getElementById("theme-toggle");
    const themeIcon = document.getElementById("theme-icon");
    const htmlTag = document.documentElement;

    // Load saved theme from localStorage or default to dark
    const savedTheme = localStorage.getItem("theme") || "dark";
    htmlTag.setAttribute("data-bs-theme", savedTheme);
    themeIcon.className = savedTheme === "dark" ? "bi bi-moon-fill" : "bi bi-sun-fill";

    // Toggle theme on button click
    themeToggle.addEventListener("click", function() {
        const currentTheme = htmlTag.getAttribute("data-bs-theme");
        const newTheme = currentTheme === "dark" ? "light" : "dark";
        htmlTag.setAttribute("data-bs-theme", newTheme);
        localStorage.setItem("theme", newTheme);

        // Update icon
        themeIcon.className = newTheme === "dark" ? "bi bi-moon-fill" : "bi bi-sun-fill";
        

    });
});

document.querySelectorAll('.like-btn').forEach(button => {
    button.addEventListener('click', function() {
        const tweetId = this.closest('.like-form').dataset.id;
        const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        fetch(`/tweet/like/${tweetId}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrftoken },
        })
        .then(res => res.json())
        .then(data => {
            this.querySelector('.like-count').textContent = data.likes_count;
        });
    });
});
