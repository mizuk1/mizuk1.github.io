/* ========================================
   Tournament 1st Edition — Custom Scripts
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {
    const starsContainer = document.querySelector('.hero-stars');
    if (!starsContainer) return;

    const starCount = 27;
    const distantCount = 40;
    const sizes = [2, 3, 4, 5, 6];
    const distantSizes = [1, 1.5, 2];
    const colors = ['#ffffff', '#1FB5FD'];

    for (let i = 0; i < distantCount; i++) {
        const star = document.createElement('span');
        star.className = 'star star--distant';

        const size = distantSizes[Math.floor(Math.random() * distantSizes.length)];
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

    const beamContainer = document.querySelector('.spotlight-container');
    if (beamContainer) {
        const beamCount = 20;

        for (let i = 0; i < beamCount; i++) {
            const beam = document.createElement('div');
            beam.className = 'spotlight_swivel';

            const rotMin = -(Math.random() * 80 + 10);
            const rotMax = Math.random() * 80 + 10;
            const delay = -(Math.random() * 15).toFixed(1);
            const opacity = (Math.random() * 0.5 + 0.2).toFixed(2);
            const lampWidth = Math.floor(Math.random() * 60 + 30);
            const lampHeight = Math.floor(Math.random() * 500 + 400);

            beam.style.setProperty('--rot-min', rotMin + 'deg');
            beam.style.setProperty('--rot-max', rotMax + 'deg');
            beam.style.setProperty('--beam-delay', delay + 's');
            beam.style.setProperty('--beam-opacity', opacity);
            beam.style.setProperty('--lamp-width', lampWidth + 'px');
            beam.style.setProperty('--lamp-height', lampHeight + 'px');

            const lamp = document.createElement('div');
            lamp.className = 'lamp';
            beam.appendChild(lamp);
            beamContainer.appendChild(beam);
        }
    }
});

