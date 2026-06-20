/* ========================================
   Tournament 1st Edition — Custom Scripts
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {
    const starsContainer = document.querySelector('.hero-stars');
    if (!starsContainer) return;

    const starCount = 27;
    const sizes = [2, 3, 4, 5, 6];
    const colors = ['#ffffff', '#1FB5FD'];

    for (let i = 0; i < starCount; i++) {
        const star = document.createElement('span');
        star.className = 'star';

        const size = sizes[Math.floor(Math.random() * sizes.length)];
        const color = colors[Math.floor(Math.random() * colors.length)];
        const top = Math.random() * 100;
        const left = Math.random() * 100;
        const delay = Math.random() * 3;

        star.style.setProperty('--star-size', size + 'px');
        star.style.backgroundColor = color;
        star.style.color = color;
        star.style.top = top + '%';
        star.style.left = left + '%';
        star.style.animationDelay = delay + 's';

        starsContainer.appendChild(star);
    }
});

