document.addEventListener('DOMContentLoaded', () => {
    const cards = document.querySelectorAll('.org-card');

    cards.forEach(card => {
        // Highlighting individual card pathing loops on click
        card.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn')) return; // Avoid breaking regular button actions
            
            cards.forEach(c => c.classList.remove('selected-path'));
            card.classList.add('selected-path');
        });
    });

    // Custom Button Logic Event Handler example
    const contactButtons = document.querySelectorAll('.connect-btn');
    contactButtons.forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation(); // Avoid triggering card selection highlight
            alert('Contact system placeholder initiated.');
        });
    });
});
