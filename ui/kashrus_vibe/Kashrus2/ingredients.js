/**
 * Ingredients Page - Refactored to use generalized architecture
 * Supports both standalone and plant-related modes
 */

// Global variables
let displayService;
let config;

document.addEventListener('DOMContentLoaded', () => {
    // Parse URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode') || 'standalone';
    const plantId = urlParams.get('plantId');
    const plantName = urlParams.get('plantName');

    // Get configuration based on mode
    const configParams = {
        plantId: plantId,
        plantName: plantName
    };

    config = getEntityConfig('ingredients', mode, configParams);

    // For plant-related mode, add the plant relation filter to the data service
    if (mode === 'plant-related' && plantId) {
        window.dataService.addFilter('PLANT_RELATION', plantId, 'exact');
    }

    // Initialize display service
    displayService = new DisplayService(window.dataService);
    displayService.initialize(config);

    // Load initial data
    displayService.loadInitialData();

    // Make displayService globally available for event handlers
    window.displayService = displayService;
});