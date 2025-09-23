/**
 * Plants Page - Refactored to use generalized architecture
 */

// Global variables
let displayService;
let config;

document.addEventListener('DOMContentLoaded', () => {
    // Get configuration for plants
    config = getEntityConfig('plants');

    // Initialize display service
    displayService = new DisplayService(window.dataService);
    displayService.initialize(config);

    // Load initial data
    displayService.loadInitialData();

    // Make displayService globally available for event handlers
    window.displayService = displayService;
});