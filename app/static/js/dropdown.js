document.addEventListener('DOMContentLoaded', function () {
    const userMenuContainer = document.querySelector('.user-menu-container');
    const userMenuTrigger = document.querySelector('.user-menu-trigger');

    if (userMenuContainer && userMenuTrigger) {
        userMenuTrigger.addEventListener('click', function (event) {
            event.stopPropagation();
            userMenuContainer.classList.toggle('active');
        });

        document.addEventListener('click', function (event) {
            if (!userMenuContainer.contains(event.target)) {
                userMenuContainer.classList.remove('active');
            }
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                userMenuContainer.classList.remove('active');
            }
        });
    }
});
