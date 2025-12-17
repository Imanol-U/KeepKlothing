document.addEventListener('DOMContentLoaded', function () {
    const userMenuContainer = document.querySelector('.user-menu-container');
    const userMenuTrigger = document.querySelector('.user-menu-trigger');

    if (userMenuContainer && userMenuTrigger) {
        // Toggle dropdown on click
        userMenuTrigger.addEventListener('click', function (event) {
            event.stopPropagation(); // Prevents the document click listener from firing immediately
            userMenuContainer.classList.toggle('active');
        });

        // Close dropdown when clicking outside
        document.addEventListener('click', function (event) {
            if (!userMenuContainer.contains(event.target)) {
                userMenuContainer.classList.remove('active');
            }
        });

        // Close dropdown when pressing Escape key
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                userMenuContainer.classList.remove('active');
            }
        });
    }
});
