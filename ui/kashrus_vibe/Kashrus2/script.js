// Master launch page functionality for Kashrus Directory

document.addEventListener('DOMContentLoaded', () => {
    setupLaunchCards();
});

function setupLaunchCards() {
    const launchCards = document.querySelectorAll('.launch-card');

    launchCards.forEach(card => {
        const button = card.querySelector('.launch-btn');
        const module = card.dataset.module;

        // Add click handler to both card and button
        const clickHandler = () => {
            handleModuleLaunch(module);
        };

        card.addEventListener('click', clickHandler);
        button.addEventListener('click', (e) => {
            e.stopPropagation(); // Prevent double-click when clicking button directly
            clickHandler();
        });

        // Add hover effects
        card.addEventListener('mouseenter', () => {
            card.style.transform = 'translateY(-5px)';
        });

        card.addEventListener('mouseleave', () => {
            card.style.transform = 'translateY(0)';
        });
    });
}

function handleModuleLaunch(module) {
    switch (module) {
        case 'plants':
            window.location.href = 'plants.html';
            break;
        case 'companies':
            // Launch companies in standalone mode (no plant relationship)
            window.location.href = 'companies.html?mode=standalone';
            break;
        case 'ingredients':
            // Launch ingredients in standalone mode (no plant relationship)
            window.location.href = 'ingredients.html?mode=standalone';
            break;
        case 'products':
            // Products functionality not yet implemented
            alert('Products functionality is coming soon!');
            break;
        default:
            console.warn('Unknown module:', module);
    }
}