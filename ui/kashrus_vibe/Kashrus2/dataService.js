/**
 * Generalized Data Service Layer
 * Handles all API interactions for different entity types
 */

class DataService {
    constructor() {
        this.baseApiUrl = 'http://172.30.3.133:5656/api/';
        this.bearerToken = localStorage.getItem('plant_app_bearer_token') ||
            'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc1ODgyMDMyMCwianRpIjoiMGRlMjllYjAtZjAwNi00NzNhLTk4YWQtMzBlMjNmMWNmNzU2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImFkbWluIiwibmJmIjoxNzU4ODIwMzIwLCJleHAiOjE3NTg4MzM2NDB9.ETf29fcfRTWe3kvfPGsK-jTYjDjCOvR5wEqxLnEG3y4';

        // Pagination state
        this.currentPage = 0;
        this.pageSize = 20;
        this.isLoading = false;
        this.hasMoreData = true;
        this.allData = [];

        // Sorting and filtering state
        this.sortField = null;
        this.sortDirection = 'asc';
        this.filters = {};
    }

    updateBearerToken(newToken) {
        this.bearerToken = newToken.startsWith('Bearer ') ? newToken : `Bearer ${newToken}`;
        localStorage.setItem('plant_app_bearer_token', this.bearerToken);
    }

    resetPaginationState() {
        this.currentPage = 0;
        this.hasMoreData = true;
        this.allData = [];
    }

    setSorting(field, direction = 'asc') {
        this.sortField = field;
        this.sortDirection = direction;
    }

    setFilters(filters) {
        this.filters = filters;
    }

    addFilter(field, value, type = 'contains') {
        if (value && value.trim()) {
            this.filters[field] = {
                value: value.trim(),
                type: type
            };
        } else {
            delete this.filters[field];
        }
    }

    removeFilter(field) {
        delete this.filters[field];
    }

    clearFilters() {
        this.filters = {};
    }

    buildApiUrl(config, page = 0, limit = this.pageSize) {
        const offset = page * limit;
        const params = new URLSearchParams();

        // Pagination parameters
        params.append('page[offset]', offset.toString());
        params.append('page[limit]', limit.toString());

        // Sorting parameter (use config default if no user sort set)
        if (this.sortField) {
            const sortParam = this.sortDirection === 'desc' ? `-${this.sortField}` : this.sortField;
            params.append('sort', sortParam);
        } else if (config.defaultSort) {
            params.append('sort', config.defaultSort);
        }

        // Filter parameter as JSON string
        const filterJson = this.buildFilterJson(config);
        if (filterJson.length > 0) {
            params.append('filter', JSON.stringify(filterJson));
        }

        // Include parameter for relationships
        if (config.include) {
            params.append('include', config.include);
        }

        // Fields parameter for specific field selection
        if (config.fields) {
            Object.keys(config.fields).forEach(table => {
                params.append(`fields[${table}]`, config.fields[table]);
            });
        }

        // Build the final URL based on endpoint configuration
        let baseUrl = `${this.baseApiUrl}${config.endpoint}`;

        // Handle relationship endpoints (e.g., plant-specific companies)
        if (config.relationshipParams) {
            Object.keys(config.relationshipParams).forEach(param => {
                baseUrl = baseUrl.replace(`{${param}}`, config.relationshipParams[param]);
            });
        }

        return `${baseUrl}?${params.toString()}`;
    }

    buildFilterJson(config) {
        const filterArray = [];

        // Add custom base filters from config first
        if (config.baseFilters) {
            config.baseFilters.forEach(filter => {
                filterArray.push(filter);
            });
        }

        // Only add ACTIVE=1 filter if not already present in baseFilters
        const hasActiveFilter = config.baseFilters?.some(filter => filter.name === 'ACTIVE');
        if (!hasActiveFilter) {
            filterArray.push({
                name: 'ACTIVE',
                op: 'eq',
                val: 1
            });
        }

        // Add plant relation filter for ingredients if present
        if (config.plantRelationFilter) {
            filterArray.push(config.plantRelationFilter);
        }

        // Process user filters
        Object.keys(this.filters).forEach(field => {
            const filter = this.filters[field];

            // Handle special filter for plant relation in ingredients
            if (field === 'PLANT_RELATION') {
                // This is handled by plantRelationFilter in config
                return;
            }

            // Skip special filter types that are handled elsewhere
            if (config.specialFilters && config.specialFilters.includes(field)) {
                return;
            }

            if (config.stringFields && config.stringFields.includes(field)) {
                let operator, value;

                switch (filter.type) {
                    case 'starts_with':
                        operator = 'ilike';
                        value = `${filter.value}%`;
                        break;
                    case 'ends_with':
                        operator = 'ilike';
                        value = `%${filter.value}`;
                        break;
                    case 'contains':
                        operator = 'ilike';
                        value = `%${filter.value}%`;
                        break;
                    case 'exact':
                        operator = 'eq';
                        value = filter.value;
                        break;
                    default:
                        operator = 'ilike';
                        value = `%${filter.value}%`;
                }

                filterArray.push({
                    name: field,
                    op: operator,
                    val: value
                });
            } else {
                filterArray.push({
                    name: field,
                    op: 'eq',
                    val: filter.value
                });
            }
        });

        return filterArray;
    }

    async fetchData(config, page = 0, append = false, resetData = false) {
        if (this.isLoading || (!this.hasMoreData && page > 0)) {
            return { success: false, data: [], hasMore: this.hasMoreData };
        }

        this.isLoading = true;

        try {
            if (page === 0 || resetData) {
                this.resetPaginationState();
                append = false;
            }

            const apiUrl = this.buildApiUrl(config, page);
            console.log('API URL:', apiUrl);

            const response = await fetch(apiUrl, {
                method: 'GET',
                headers: {
                    'Authorization': this.bearerToken,
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                }
            });

            if (!response.ok) {
                if (response.status === 401) {
                    return { success: false, error: 'auth_required', status: 401 };
                }
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const responseData = await response.json();
            let processedData = [];

            // Process the response based on configuration
            if (config.dataProcessor) {
                processedData = config.dataProcessor(responseData);
            } else {
                processedData = responseData.data || [];
            }

            if (processedData.length < this.pageSize) {
                this.hasMoreData = false;
            }

            if (append && page > 0) {
                this.allData = [...this.allData, ...processedData];
            } else {
                this.allData = processedData;
            }

            this.currentPage = page;

            return {
                success: true,
                data: this.allData,
                hasMore: this.hasMoreData,
                currentPage: this.currentPage
            };

        } catch (error) {
            console.error('Error fetching data:', error);
            return {
                success: false,
                error: error.message,
                data: []
            };
        } finally {
            this.isLoading = false;
        }
    }

    async loadMoreData(config) {
        if (!this.isLoading && this.hasMoreData) {
            return await this.fetchData(config, this.currentPage + 1, true);
        }
        return { success: false, data: this.allData };
    }

    // Helper method to get current data without fetching
    getCurrentData() {
        return this.allData;
    }

    // Helper method to check if currently loading
    isCurrentlyLoading() {
        return this.isLoading;
    }

    // Helper method to check if more data available
    hasMore() {
        return this.hasMoreData;
    }
}

// Create a global instance that can be shared
window.dataService = new DataService();