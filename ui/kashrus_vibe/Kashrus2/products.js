/**
 * Products Page Controller
 * Uses the generalized architecture to display products (labels)
 */

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Create display service instance
    window.displayService = new DisplayService(window.dataService);

    // Get entity configuration for products
    const config = getEntityConfig('products');

    // Initialize display service with configuration
    displayService.initialize(config);

    // Load initial data
    displayService.loadInitialData();
});