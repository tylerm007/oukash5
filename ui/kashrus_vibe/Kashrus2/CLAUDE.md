# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a plant directory web application for managing Kashrus (kosher certification) data. It's a client-side JavaScript application that consumes a REST API to display and manage plant, company, and ingredient information.

## Architecture

### Core Structure
- **Frontend-only application**: No build process, uses vanilla HTML/CSS/JavaScript
- **API-driven**: Consumes REST API at `http://172.30.3.133:5656/api/`
- **Multi-page application**: Separate HTML pages for different entity types:
  - `index.html` - Main plant directory (PLANTTB)
  - `companies.html` - Companies view (COMPANYTB via OWNSTB relationships)
  - `ingredients.html` - Ingredients view (INGREDIENTTB)

### Key Components
- **Authentication**: JWT Bearer token stored in localStorage as `plant_app_bearer_token`
- **Data Models**: Works with PLANTTB, COMPANYTB, OWNSTB, INGREDIENTTB tables
- **Views**: Card view and table view with sortable/filterable columns
- **Navigation**: Context menu system for drilling down from plants to related entities

### File Structure
```
├── index.html          # Main plant directory page
├── companies.html      # Companies page (plant relationships)
├── ingredients.html    # Ingredients page
├── script.js          # Main plant directory logic
├── companies.js       # Companies page logic
├── ingredients.js     # Ingredients page logic
├── styles.css         # Shared styles for all pages
└── package.json       # Basic project metadata
```

## API Integration

### Base URL
`http://172.30.3.133:5656/api/`

### Authentication
All requests require Bearer token in Authorization header. Token is managed via:
- `updateBearerToken(newToken)` function
- Stored in localStorage
- UI handles 401 errors with token refresh dialog

### Key Endpoints
- `PLANTTB/` - Plant data with pagination, sorting, filtering
- `PLANTTB/{plantId}/OWNSTBList` - Companies related to specific plant
- `PLANTTB/{plantId}/INGREDIENTTBList` - Ingredients related to specific plant

### API Parameters
- `page[offset]` & `page[limit]` - Pagination
- `sort` - Field sorting (prefix with `-` for descending)
- `filter` - JSON array of filter objects with `name`, `op`, `val` properties
- `include` - Include related entity data
- `fields[TABLE]` - Specify which fields to return

## Development Commands

This is a static web application with no build process. To develop:

1. **Local Development**: Open HTML files directly in browser or serve via local web server
2. **Testing**: Manual testing via browser (no automated test framework)
3. **No package manager**: Uses vanilla JavaScript, no dependencies

## Common Development Patterns

### Adding New Filters
1. Add field to `stringFields` array if it supports text matching
2. Add field label to `fieldLabels` object
3. Update `buildFilterJson()` if special handling needed

### Adding New Columns
1. Add column definition to `allColumns` array
2. Update display logic in `displayCardView()` and `displayTableView()`
3. Handle special formatting in the switch statements

### Token Management
- Token expiry is handled automatically with 401 error detection
- New tokens can be entered via UI dialog
- Token is persisted across page refreshes

### Cross-Page Navigation
- Uses URL parameters to pass context (plantId, plantName)
- `window.open()` for new tabs
- Context menus provide drill-down navigation

## Code Conventions

- **Variable naming**: camelCase for JavaScript, UPPER_CASE for API field names
- **DOM manipulation**: Direct DOM API usage, no frameworks
- **Event handling**: Mix of inline handlers and addEventListener
- **State management**: Global variables for application state
- **Error handling**: Try/catch with user-friendly error messages