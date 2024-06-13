document.addEventListener('DOMContentLoaded', function () {
    const ellipsisButton = document.getElementById('ellipsisButton');
    const dropdownMenu = document.getElementById('dropdownMenu');

    ellipsisButton.addEventListener('click', function (event) {
        event.stopPropagation();
        if (dropdownMenu.classList.contains('show')) {
            dropdownMenu.classList.remove('show');
        } else {
            dropdownMenu.classList.add('show');
        }
    });

    document.addEventListener('click', function (event) {
        if (!ellipsisButton.contains(event.target) && !dropdownMenu.contains(event.target)) {
            dropdownMenu.classList.remove('show');
        }
    });
});
