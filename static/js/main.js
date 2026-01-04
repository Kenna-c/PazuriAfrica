function toggleMenu() {
    const menu = document.getElementById('nav-menu');
    menu.style.display = menu.style.display === 'flex' ? 'none' : 'flex';
}

window.addEventListener('scroll', () => {
    const reveals = document.querySelectorAll('.reveal');
    reveals.forEach(reveal => {
        const windowHeight = window.innerHeight;
        const elementTop = reveal.getBoundingClientRect().top;
        if (elementTop < windowHeight - 50) {
            reveal.classList.add('active');
        }
    });
});
