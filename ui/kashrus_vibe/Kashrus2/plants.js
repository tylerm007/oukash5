/**
 * Plants Page - Refactored to use generalized architecture
 */

// Global variables
let displayService;
let config;

document.addEventListener('DOMContentLoaded', () => {
    // Parse URL parameters
    const urlParams = new URLSearchParams(window.location.search);
    const mode = urlParams.get('mode') || 'standalone';
    const companyId = urlParams.get('companyId');
    const companyName = urlParams.get('companyName');

    // Get configuration for plants with mode and parameters
    config = getEntityConfig('plants', mode, {
        companyId,
        companyName
    });

    // Initialize display service
    displayService = new DisplayService(window.dataService);
    displayService.initialize(config);

    // Load initial data
    displayService.loadInitialData();

    // Make displayService globally available for event handlers
    window.displayService = displayService;
});