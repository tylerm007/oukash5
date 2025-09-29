/**
 * Generalized Display/UI Service
 * Handles all UI rendering and interactions for different entity types
 */

class DisplayService {
    constructor(dataService) {
        this.dataService = dataService;
        this.currentView = 'card';
        this.config = null;
        this.displayedColumns = [];
        this.currentFilterField = null;
        this.currentItemId = null;
        this.currentItem = null;

        // DOM elements cache
        this.elements = {};
        this.bindEvents();
    }

    initialize(config) {
        this.config = config;
        // Use defaultColumns if specified, otherwise use all columns
        this.displayedColumns = config.defaultColumns ? [...config.defaultColumns] : [...config.columns];
        this.cacheElements();
        this.setupUI();
        this.updatePageTitle();
        this.setupCertifiedToggle();
    }

    cacheElements() {
        this.elements = {
            // Main containers
            loading: document.getElementById('loading'),
            loadingMore: document.getElementById('loading-more'),
            error: document.getElementById('error'),
            noMoreData: document.getElementById('no-more-data'),
            itemList: document.getElementById('plant-list'),

            // Header elements
            pageTitle: document.getElementById('page-title'),

            // View controls
            backBtn: document.getElementById('back-btn'),
            cardViewBtn: document.getElementById('card-view-btn'),
            tableViewBtn: document.getElementById('table-view-btn'),
            columnsBtn: document.getElementById('columns-btn'),
            refreshBtn: document.getElementById('refresh-btn'),

            // Auth elements
            authError: document.getElementById('auth-error'),
            tokenInput: document.getElementById('token-input'),
            updateTokenBtn: document.getElementById('update-token-btn'),

            // Certified Only toggle
            certifiedOnlyToggle: document.getElementById('certified-only-toggle'),

            // Sort/Filter info
            sortFilterInfo: document.getElementById('sort-filter-info'),
            sortInfo: document.getElementById('sort-info'),
            sortDetails: document.getElementById('sort-details'),
            filterInfo: document.getElementById('filter-info'),
            filterDetails: document.getElementById('filter-details'),

            // Filter dialog
            filterDialog: document.getElementById('filter-dialog'),
            filterDialogTitle: document.getElementById('filter-dialog-title'),
            filterInput: document.getElementById('filter-input'),
            filterTypeContainer: document.getElementById('filter-type-container'),
            filterTypeSelect: document.getElementById('filter-type-select'),
            applyFilterBtn: document.getElementById('apply-filter-btn'),
            clearFilterBtn: document.getElementById('clear-filter-btn'),
            cancelFilterBtn: document.getElementById('cancel-filter-btn'),

            // Column dialog
            columnDialog: document.getElementById('column-dialog'),
            availableColumns: document.getElementById('available-columns'),
            displayedColumnsEl: document.getElementById('displayed-columns'),
            applyColumnsBtn: document.getElementById('apply-columns-btn'),
            resetColumnsBtn: document.getElementById('reset-columns-btn'),
            cancelColumnsBtn: document.getElementById('cancel-columns-btn'),

            // Context menu and details
            contextMenu: document.getElementById('plant-context-menu'),
            detailsPopup: document.getElementById('plant-details-popup'),
            detailsName: document.getElementById('details-plant-name'),
            detailsContent: document.getElementById('details-content'),
            closeDetailsBtn: document.getElementById('close-details-btn')
        };
    }

    bindEvents() {
        // Will bind events after elements are cached
    }

    setupUI() {
        if (!this.elements.backBtn) return;

        // Back button
        this.elements.backBtn?.addEventListener('click', () => {
            window.location.href = 'index.html';
        });

        // View toggle buttons
        this.elements.cardViewBtn?.addEventListener('click', () => {
            this.setView('card');
        });

        this.elements.tableViewBtn?.addEventListener('click', () => {
            this.setView('table');
        });

        // Refresh button
        this.elements.refreshBtn?.addEventListener('click', () => {
            this.refresh();
        });

        // Columns button
        this.elements.columnsBtn?.addEventListener('click', () => {
            this.showColumnDialog();
        });

        // Certified Only toggle
        this.elements.certifiedOnlyToggle?.addEventListener('change', () => {
            this.handleCertifiedToggle();
        });

        // Login form handling
        const loginForm = document.getElementById('login-form');
        if (loginForm) {
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                await this.handleLogin();
            });
        }

        // Auth token update (fallback)
        this.elements.updateTokenBtn?.addEventListener('click', () => {
            this.updateToken();
        });

        this.elements.tokenInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.updateToken();
            }
        });

        // Filter dialog
        this.elements.applyFilterBtn?.addEventListener('click', () => {
            this.applyFilter();
        });

        this.elements.clearFilterBtn?.addEventListener('click', () => {
            this.clearCurrentFilter();
        });

        this.elements.cancelFilterBtn?.addEventListener('click', () => {
            this.hideFilterDialog();
        });

        this.elements.filterInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.applyFilter();
            } else if (e.key === 'Escape') {
                this.hideFilterDialog();
            }
        });

        // Column dialog
        this.elements.applyColumnsBtn?.addEventListener('click', () => {
            this.applyColumnChanges();
        });

        this.elements.resetColumnsBtn?.addEventListener('click', () => {
            this.resetColumns();
        });

        this.elements.cancelColumnsBtn?.addEventListener('click', () => {
            this.hideColumnDialog();
        });

        // Close dialogs when clicking outside
        this.elements.filterDialog?.addEventListener('click', (e) => {
            if (e.target.id === 'filter-dialog') {
                this.hideFilterDialog();
            }
        });

        this.elements.columnDialog?.addEventListener('click', (e) => {
            if (e.target.id === 'column-dialog') {
                this.hideColumnDialog();
            }
        });

        // Details popup
        this.elements.closeDetailsBtn?.addEventListener('click', () => {
            this.hideItemDetails();
        });

        this.elements.detailsPopup?.addEventListener('click', (e) => {
            if (e.target.id === 'plant-details-popup') {
                this.hideItemDetails();
            }
        });

        // Context menu items - use event delegation since menu is dynamic
        document.addEventListener('click', (e) => {
            if (e.target.closest('.context-menu-item')) {
                console.log('Context menu item clicked:', e.target);
                const menuItem = e.target.closest('.context-menu-item');
                const action = menuItem.dataset.action;
                console.log('Action from dataset:', action);
                this.handleContextMenuAction(action);
            }
        });

        // Infinite scroll
        this.setupInfiniteScroll();
    }

    updatePageTitle() {
        if (this.elements.pageTitle && this.config.pageTitle) {
            this.elements.pageTitle.textContent = this.config.pageTitle;
        }
    }

    setupCertifiedToggle() {
        // Hide the toggle if not enabled for this entity type
        if (this.config.enableCertifiedToggle === false && this.elements.certifiedOnlyToggle) {
            const toggleContainer = this.elements.certifiedOnlyToggle.closest('.certified-toggle');
            if (toggleContainer) {
                toggleContainer.style.display = 'none';
            }
        } else if (this.elements.certifiedOnlyToggle) {
            // Ensure toggle is visible if not explicitly disabled
            const toggleContainer = this.elements.certifiedOnlyToggle.closest('.certified-toggle');
            if (toggleContainer) {
                toggleContainer.style.display = '';
            }
        }
    }

    setView(view) {
        this.currentView = view;

        // Update button states
        if (view === 'card') {
            this.elements.cardViewBtn?.classList.add('active');
            this.elements.tableViewBtn?.classList.remove('active');
        } else {
            this.elements.tableViewBtn?.classList.add('active');
            this.elements.cardViewBtn?.classList.remove('active');
        }

        // Re-render current data
        const currentData = this.dataService.getCurrentData();
        if (currentData.length > 0) {
            this.displayData(currentData);
        }
    }

    async refresh() {
        this.showLoading();
        const result = await this.dataService.fetchData(this.config, 0, false, true);
        this.handleDataResult(result);
    }

    async handleCertifiedToggle() {
        // Skip if toggle is disabled for this entity type
        if (this.config.enableCertifiedToggle === false) {
            return;
        }

        const isChecked = this.elements.certifiedOnlyToggle.checked;
        const statusField = this.config.statusField || 'Status';

        if (isChecked) {
            // Add certified filter
            this.dataService.addFilter(statusField, 'Certified', 'exact');
        } else {
            // Remove certified filter
            this.dataService.removeFilter(statusField);
        }

        // Refresh data with new filter
        await this.refresh();
        this.updateSortFilterInfo();
    }

    async loadInitialData() {
        this.showLoading();
        const result = await this.dataService.fetchData(this.config);
        this.handleDataResult(result);
    }

    async loadMoreData() {
        if (!this.dataService.isCurrentlyLoading() && this.dataService.hasMore()) {
            this.showLoadingMore();
            const result = await this.dataService.loadMoreData(this.config);
            this.handleDataResult(result, false);
        }
    }

    handleDataResult(result, isInitial = true) {
        this.hideLoading();
        this.hideLoadingMore();

        if (!result.success) {
            if (result.error === 'auth_required') {
                this.showAuthError();
            } else {
                this.showError(result.error || 'Failed to load data. Please try again.');
            }
            return;
        }

        this.hideAuthError();
        this.hideError();

        if (!result.hasMore) {
            this.showNoMoreData();
        } else {
            this.hideNoMoreData();
        }

        this.displayData(result.data);
    }

    displayData(data) {
        if (!this.elements.itemList) return;

        if (data.length === 0) {
            this.elements.itemList.innerHTML = `<p class="no-plants">No ${this.config.entityNamePlural} found matching the current filters.</p>`;
            this.updateSortFilterInfo();
            return;
        }

        if (this.currentView === 'card') {
            this.displayCardView(data);
        } else {
            this.displayTableView(data);
        }

        this.updateSortFilterInfo();
    }

    displayCardView(data) {
        this.elements.itemList.className = 'plant-grid';

        this.elements.itemList.innerHTML = data.map(item => {
            const attributes = item.attributes || {};

            // Find primary fields for header
            const nameColumn = this.displayedColumns.find(col => col.field === this.config.primaryNameField);
            const idColumn = this.displayedColumns.find(col => col.field === this.config.primaryIdField);

            // Generate detail rows for other displayed columns
            const detailColumns = this.displayedColumns.filter(col =>
                col.field !== this.config.primaryNameField &&
                col.field !== this.config.primaryIdField
            );

            const cardEvents = this.config.enableContextMenu ?
                `oncontextmenu="displayService.showItemContextMenu(event, ${item.id}); return false;" ondblclick="displayService.showItemDetails(${item.id})"` : '';

            return `
                <div class="plant-card" data-item-id="${item.id}" ${cardEvents}>
                    <div class="plant-header">
                        ${nameColumn ? `
                            <h3 class="plant-name clickable-field" data-field="${this.config.primaryNameField}"
                                onclick="displayService.handleSort('${this.config.primaryNameField}')"
                                oncontextmenu="displayService.showFilterDialog(event, '${this.config.primaryNameField}'); return false;">
                                ${this.formatFieldValue(this.config.primaryNameField, attributes[this.config.primaryNameField], attributes) || `Unknown ${this.config.entityName}`}
                            </h3>
                        ` : ''}
                        ${idColumn ? `
                            <span class="plant-id clickable-field" data-field="${this.config.primaryIdField}"
                                onclick="displayService.handleSort('${this.config.primaryIdField}')"
                                oncontextmenu="displayService.showFilterDialog(event, '${this.config.primaryIdField}'); return false;">
                                ID: ${attributes[this.config.primaryIdField] || 'N/A'}
                            </span>
                        ` : ''}
                    </div>
                    <div class="plant-details">
                        ${detailColumns.map(column => {
                            const value = this.formatFieldValue(column.field, attributes[column.field], attributes);

                            return `
                                <div class="detail-row">
                                    <span class="label clickable-field" data-field="${column.field}"
                                        onclick="displayService.handleSort('${column.field}')"
                                        oncontextmenu="displayService.showFilterDialog(event, '${column.field}'); return false;">
                                        ${column.label}:
                                    </span>
                                    <span class="value">${value}</span>
                                </div>
                            `;
                        }).join('')}
                    </div>
                </div>
            `;
        }).join('');
    }

    displayTableView(data) {
        this.elements.itemList.className = 'plant-table-container';

        this.elements.itemList.innerHTML = `
            <table class="plant-table">
                <thead>
                    <tr>
                        ${this.displayedColumns.map(column => {
                            const isSorted = this.dataService.sortField === column.field;
                            const isFiltered = this.dataService.filters[column.field];
                            const sortIcon = isSorted ? (this.dataService.sortDirection === 'asc' ? '▲' : '▼') : '';
                            const filterIcon = isFiltered ? '🔍' : '';

                            return `
                                <th class="sortable-header ${isSorted ? 'sorted' : ''}"
                                    data-field="${column.field}"
                                    oncontextmenu="displayService.showFilterDialog(event, '${column.field}'); return false;">
                                    <span class="header-content">
                                        ${column.label}
                                        <span class="sort-icon">${sortIcon}</span>
                                        <span class="filter-icon">${filterIcon}</span>
                                    </span>
                                </th>
                            `;
                        }).join('')}
                    </tr>
                </thead>
                <tbody>
                    ${data.map(item => {
                        const attributes = item.attributes || {};
                        const rowEvents = this.config.enableContextMenu ?
                            `oncontextmenu="displayService.showItemContextMenu(event, ${item.id}); return false;" ondblclick="displayService.showItemDetails(${item.id})"` : '';

                        return `
                            <tr data-item-id="${item.id}" ${rowEvents}>
                                ${this.displayedColumns.map(column => {
                                    const cellContent = this.formatFieldValue(column.field, attributes[column.field], attributes);
                                    const cellClass = column.field === this.config.primaryNameField ? 'plant-name-cell' : '';

                                    return `<td class="${cellClass}">${cellContent}</td>`;
                                }).join('')}
                            </tr>
                        `;
                    }).join('')}
                </tbody>
            </table>
        `;

        // Add click handlers for sorting
        this.elements.itemList.querySelectorAll('.sortable-header').forEach(header => {
            header.addEventListener('click', (e) => {
                const field = e.currentTarget.dataset.field;
                this.handleSort(field);
            });
        });
    }

    formatFieldValue(fieldName, value, allAttributes) {
        if (this.config.fieldFormatters && this.config.fieldFormatters[fieldName]) {
            return this.config.fieldFormatters[fieldName](value, allAttributes);
        }

        if (value === null || value === undefined) {
            return 'N/A';
        }

        if (typeof value === 'boolean') {
            return value ? 'Yes' : 'No';
        }

        return value.toString();
    }

    async handleSort(field) {
        const currentDirection = this.dataService.sortField === field ? this.dataService.sortDirection : 'asc';
        const newDirection = currentDirection === 'asc' ? 'desc' : 'asc';

        this.dataService.setSorting(field, newDirection);
        await this.refresh();
    }

    showFilterDialog(event, field) {
        event.preventDefault();
        this.currentFilterField = field;

        if (!this.elements.filterDialog) return;

        const column = this.config.columns.find(col => col.field === field);
        this.elements.filterDialogTitle.textContent = `Filter by ${column ? column.label : field}`;

        // Show/hide filter type selection based on field type
        if (this.config.stringFields && this.config.stringFields.includes(field)) {
            this.elements.filterTypeContainer?.classList.remove('hidden');
            this.elements.filterTypeSelect.value = this.dataService.filters[field]?.type || 'contains';
        } else {
            this.elements.filterTypeContainer?.classList.add('hidden');
        }

        this.elements.filterInput.value = this.dataService.filters[field]?.value || '';
        this.elements.filterDialog.classList.remove('hidden');
        this.elements.filterInput.focus();
    }

    hideFilterDialog() {
        this.elements.filterDialog?.classList.add('hidden');
        this.currentFilterField = null;
    }

    async applyFilter() {
        if (!this.currentFilterField) return;

        const value = this.elements.filterInput.value.trim();
        const type = this.config.stringFields?.includes(this.currentFilterField) ?
            this.elements.filterTypeSelect.value : 'exact';

        this.dataService.addFilter(this.currentFilterField, value, type);
        this.hideFilterDialog();
        await this.refresh();
    }

    async clearCurrentFilter() {
        if (!this.currentFilterField) return;

        this.dataService.removeFilter(this.currentFilterField);
        this.hideFilterDialog();
        await this.refresh();
    }

    updateSortFilterInfo() {
        if (!this.elements.sortFilterInfo) return;

        let hasInfo = false;

        // Update sort info
        if (this.dataService.sortField) {
            this.elements.sortInfo?.classList.remove('hidden');
            const column = this.config.columns.find(col => col.field === this.dataService.sortField);
            const direction = this.dataService.sortDirection === 'asc' ? '↑' : '↓';
            this.elements.sortDetails.textContent = `${column ? column.label : this.dataService.sortField} ${direction}`;
            hasInfo = true;
        } else {
            this.elements.sortInfo?.classList.add('hidden');
        }

        // Update filter info
        const filterKeys = Object.keys(this.dataService.filters);
        if (filterKeys.length > 0) {
            this.elements.filterInfo?.classList.remove('hidden');
            this.elements.filterDetails.innerHTML = filterKeys.map(field => {
                const filter = this.dataService.filters[field];
                const column = this.config.columns.find(col => col.field === field);
                const typeLabel = this.getFilterTypeLabel(filter.type);

                return `<span class="filter-tag" data-field="${field}" onclick="displayService.editFilter('${field}')">
                    ${column ? column.label : field} ${typeLabel} "${filter.value}" ×
                </span>`;
            }).join('');
            hasInfo = true;
        } else {
            this.elements.filterInfo?.classList.add('hidden');
        }

        // Show/hide the entire info box
        if (hasInfo) {
            this.elements.sortFilterInfo?.classList.remove('hidden');
        } else {
            this.elements.sortFilterInfo?.classList.add('hidden');
        }
    }

    getFilterTypeLabel(type) {
        const typeLabels = {
            'contains': 'contains',
            'starts_with': 'starts with',
            'ends_with': 'ends with',
            'exact': 'equals'
        };
        return typeLabels[type] || 'contains';
    }

    editFilter(field) {
        const event = { preventDefault: () => {} };
        this.showFilterDialog(event, field);
    }

    showItemContextMenu(event, itemId) {
        if (!this.config.enableContextMenu) return;

        event.preventDefault();
        this.currentItemId = itemId;
        this.currentItem = this.dataService.getCurrentData().find(item => item.id == itemId);

        if (!this.elements.contextMenu) return;

        this.elements.contextMenu.classList.remove('hidden');
        this.elements.contextMenu.style.left = event.pageX + 'px';
        this.elements.contextMenu.style.top = event.pageY + 'px';

        // Hide menu when clicking elsewhere
        setTimeout(() => {
            const hideHandler = (e) => {
                if (!e.target.closest('#plant-context-menu')) {
                    this.hideItemContextMenu();
                    document.removeEventListener('click', hideHandler);
                }
            };
            document.addEventListener('click', hideHandler);
        }, 0);
    }

    hideItemContextMenu() {
        this.elements.contextMenu?.classList.add('hidden');
    }

    showItemDetails(itemId) {
        this.currentItem = this.dataService.getCurrentData().find(item => item.id == itemId);
        if (!this.currentItem || !this.elements.detailsPopup) return;

        const attributes = this.currentItem.attributes || {};
        const primaryName = attributes[this.config.primaryNameField] || `Unknown ${this.config.entityName}`;

        this.elements.detailsName.textContent = primaryName;

        // Build detailed content
        this.elements.detailsContent.innerHTML = `
            <div class="details-grid">
                ${this.config.columns.map(column => {
                    const value = this.formatFieldValue(column.field, attributes[column.field], attributes);

                    return `
                        <div class="detail-item">
                            <label>${column.label}:</label>
                            <span>${value}</span>
                        </div>
                    `;
                }).join('')}
            </div>
        `;

        this.elements.detailsPopup.classList.remove('hidden');
    }

    hideItemDetails() {
        this.elements.detailsPopup?.classList.add('hidden');
    }

    handleContextMenuAction(action) {
        this.hideItemContextMenu();

        console.log('Context menu action:', action, 'Current item:', this.currentItem, 'Config actions:', this.config.contextMenuActions);

        if (!this.currentItem || !this.config.contextMenuActions) {
            console.error('Missing currentItem or contextMenuActions:', {
                currentItem: this.currentItem,
                hasActions: !!this.config.contextMenuActions
            });
            return;
        }

        const actionHandler = this.config.contextMenuActions[action];
        if (actionHandler) {
            console.log('Executing action handler for:', action);
            actionHandler(this.currentItem);
        } else {
            console.error('No action handler found for:', action);
        }
    }

    async handleLogin() {
        const username = document.getElementById('username')?.value.trim();
        const password = document.getElementById('password')?.value.trim();
        const loginBtn = document.getElementById('login-btn');
        const loginBtnText = loginBtn?.querySelector('.login-btn-text');
        const loginSpinner = loginBtn?.querySelector('.login-spinner');
        const loginError = document.getElementById('login-error');

        if (!username || !password) {
            this.showLoginError('Please enter both username and password');
            return;
        }

        // Show loading state
        if (loginBtn) loginBtn.disabled = true;
        if (loginBtnText) loginBtnText.classList.add('hidden');
        if (loginSpinner) loginSpinner.classList.remove('hidden');
        if (loginError) loginError.classList.add('hidden');

        try {
            const result = await window.authService.login(username, password);

            if (result.success) {
                // Clear form
                document.getElementById('username').value = '';
                document.getElementById('password').value = '';

                // Hide auth error and refresh data
                this.hideAuthError();
                this.refresh();
            } else {
                this.showLoginError(result.error || 'Login failed');
            }
        } catch (error) {
            this.showLoginError('Login failed. Please try again.');
            console.error('Login error:', error);
        } finally {
            // Reset loading state
            if (loginBtn) loginBtn.disabled = false;
            if (loginBtnText) loginBtnText.classList.remove('hidden');
            if (loginSpinner) loginSpinner.classList.add('hidden');
        }
    }

    showLoginError(message) {
        const loginError = document.getElementById('login-error');
        if (loginError) {
            loginError.textContent = message;
            loginError.classList.remove('hidden');
        }
    }

    updateToken() {
        const newToken = this.elements.tokenInput?.value.trim();
        if (newToken) {
            this.dataService.updateBearerToken(newToken);
            this.elements.tokenInput.value = '';
            this.hideAuthError();
            this.refresh();
        }
    }

    showColumnDialog() {
        if (!this.elements.columnDialog) return;

        // Clear existing content
        this.elements.availableColumns.innerHTML = '';
        this.elements.displayedColumnsEl.innerHTML = '';

        // Get available columns (not displayed)
        const displayedFields = this.displayedColumns.map(col => col.field);
        const availableColumns = this.config.columns.filter(col => !displayedFields.includes(col.field));

        // Populate available columns
        availableColumns.forEach(column => {
            const columnItem = this.createColumnItem(column);
            this.elements.availableColumns.appendChild(columnItem);
        });

        // Populate displayed columns
        this.displayedColumns.forEach(column => {
            const columnItem = this.createColumnItem(column);
            this.elements.displayedColumnsEl.appendChild(columnItem);
        });

        this.elements.columnDialog.classList.remove('hidden');
    }

    createColumnItem(column) {
        const div = document.createElement('div');
        div.className = 'column-item';
        div.draggable = true;
        div.dataset.field = column.field;
        div.textContent = column.label;

        // Add drag event listeners
        div.addEventListener('dragstart', (e) => {
            e.dataTransfer.setData('text/plain', column.field);
            div.classList.add('dragging');
        });

        div.addEventListener('dragend', () => {
            div.classList.remove('dragging');
        });

        return div;
    }

    applyColumnChanges() {
        const columnItems = this.elements.displayedColumnsEl.querySelectorAll('.column-item');

        this.displayedColumns = Array.from(columnItems).map(item => {
            const field = item.dataset.field;
            return this.config.columns.find(col => col.field === field);
        });

        const currentData = this.dataService.getCurrentData();
        if (currentData.length > 0) {
            this.displayData(currentData);
        }

        this.hideColumnDialog();
    }

    resetColumns() {
        this.displayedColumns = [...this.config.columns];
        this.showColumnDialog(); // Refresh the dialog
    }

    hideColumnDialog() {
        this.elements.columnDialog?.classList.add('hidden');
    }

    setupInfiniteScroll() {
        window.addEventListener('scroll', () => {
            const scrollTop = document.documentElement.scrollTop || document.body.scrollTop;
            const scrollHeight = document.documentElement.scrollHeight || document.body.scrollHeight;
            const clientHeight = document.documentElement.clientHeight;

            if (scrollTop + clientHeight >= scrollHeight - 200) {
                this.loadMoreData();
            }
        });
    }

    // Loading states
    showLoading() {
        this.elements.loading?.style && (this.elements.loading.style.display = 'block');
        this.hideError();
        this.hideNoMoreData();
    }

    hideLoading() {
        this.elements.loading?.style && (this.elements.loading.style.display = 'none');
    }

    showLoadingMore() {
        this.elements.loadingMore?.classList.remove('hidden');
    }

    hideLoadingMore() {
        this.elements.loadingMore?.classList.add('hidden');
    }

    showError(message) {
        if (!this.elements.error) return;
        this.elements.error.classList.remove('hidden');
        this.elements.error.textContent = message;
    }

    hideError() {
        this.elements.error?.classList.add('hidden');
    }

    showAuthError() {
        this.hideLoading();
        this.hideError();
        this.elements.authError?.classList.remove('hidden');
    }

    hideAuthError() {
        this.elements.authError?.classList.add('hidden');
    }

    showNoMoreData() {
        this.elements.noMoreData?.classList.remove('hidden');
    }

    hideNoMoreData() {
        this.elements.noMoreData?.classList.add('hidden');
    }
}

// Global instance will be created by individual pages
window.DisplayService = DisplayService;