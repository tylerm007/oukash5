/**
 * Entity Configuration System
 * Defines configurations for different data types and their display properties
 */

const EntityConfigs = {
    // Plants configuration
    plants: {
        entityName: 'Plant',
        entityNamePlural: 'plants',
        pageTitle: 'Plant Directory',
        endpoint: 'PLANTTB/',
        primaryNameField: 'NAME',
        primaryIdField: 'PLANT_ID',
        enableContextMenu: true,

        // Column definitions
        columns: [
            { field: 'PLANT_ID', label: 'ID' },
            { field: 'NAME', label: 'Name' },
            { field: 'PLANT_TYPE', label: 'Type' },
            { field: 'USDA_CODE', label: 'USDA Code' },
            { field: 'JEWISH_OWNED', label: 'Jewish Owned' },
            { field: 'SPECIAL_PROD', label: 'Special Prod' },
            { field: 'PLANT_DIRECTIONS', label: 'Directions' }
        ],

        // Fields that support string-based filtering
        stringFields: ['NAME', 'PLANT_TYPE', 'USDA_CODE', 'PLANT_DIRECTIONS'],

        // Field formatters for special display logic
        fieldFormatters: {
            'JEWISH_OWNED': (value) => value ? 'Yes' : 'No',
            'SPECIAL_PROD': (value) => value ? 'Yes' : 'No'
        },

        // Base filters that are always applied
        baseFilters: [
            {
                name: 'ACTIVE',
                op: 'eq',
                val: 1
            }
        ],

        // Context menu actions
        contextMenuActions: {
            details: (item) => {
                displayService.showItemDetails(item.id);
            },
            companies: (item) => {
                const attributes = item.attributes || {};
                const companiesUrl = `companies.html?mode=plant-related&plantId=${item.id}&plantName=${encodeURIComponent(attributes.NAME || 'Unknown Plant')}`;
                window.open(companiesUrl, '_blank');
            },
            ingredients: (item) => {
                const attributes = item.attributes || {};
                const ingredientsUrl = `ingredients.html?mode=plant-related&plantId=${item.id}&plantName=${encodeURIComponent(attributes.NAME || 'Unknown Plant')}`;
                window.open(ingredientsUrl, '_blank');
            },
            products: () => {
                alert('Products functionality coming soon...');
            },
            inspections: () => {
                alert('Inspections functionality coming soon...');
            }
        }
    },

    // Companies configuration - standalone mode
    companiesStandalone: {
        entityName: 'Company',
        entityNamePlural: 'companies',
        pageTitle: 'Companies',
        endpoint: 'COMPANYTB/',
        primaryNameField: 'NAME',
        primaryIdField: 'COMPANY_ID',
        enableContextMenu: false,

        columns: [
            { field: 'COMPANY_ID', label: 'Company ID' },
            { field: 'NAME', label: 'Company Name' },
            { field: 'STATUS', label: 'Status' },
            { field: 'CATEGORY', label: 'Category' },
            { field: 'COMPANY_TYPE', label: 'Company Type' },
            { field: 'JEWISH_OWNED', label: 'Jewish Owned' },
            { field: 'LIST', label: 'List' },
            { field: 'PRODUCER', label: 'Producer' },
            { field: 'MARKETER', label: 'Marketer' },
            { field: 'SOURCE', label: 'Source' },
            { field: 'PRIVATE_LABEL', label: 'Private Label' },
            { field: 'PARENT_CO', label: 'Parent Company' },
            { field: 'RC', label: 'RC' }
        ],

        // Default columns to show initially (same as plant-related view)
        defaultColumns: [
            { field: 'COMPANY_ID', label: 'Company ID' },
            { field: 'NAME', label: 'Company Name' },
            { field: 'STATUS', label: 'Status' },
            { field: 'CATEGORY', label: 'Category' },
            { field: 'RC', label: 'RC' }
        ],

        stringFields: ['NAME', 'CATEGORY', 'COMPANY_TYPE', 'STATUS', 'JEWISH_OWNED', 'LIST', 'PARENT_CO', 'RC'],

        fieldFormatters: {
            'PRODUCER': (value) => value ? 'Yes' : 'No',
            'MARKETER': (value) => value ? 'Yes' : 'No',
            'SOURCE': (value) => value ? 'Yes' : 'No',
            'PRIVATE_LABEL': (value) => value ? 'Yes' : 'No'
        },

        baseFilters: [
            {
                name: 'ACTIVE',
                op: 'eq',
                val: 1
            }
        ]
    },

    // Companies configuration - plant-related mode
    companiesPlantRelated: {
        entityName: 'Company',
        entityNamePlural: 'companies',
        pageTitle: 'Companies', // Will be updated with plant name
        endpoint: 'PLANTTB/{plantId}/OWNSTBList',
        primaryNameField: 'NAME',
        primaryIdField: 'COMPANY_ID',
        enableContextMenu: false,

        columns: [
            { field: 'COMPANY_ID', label: 'Company ID' },
            { field: 'NAME', label: 'Company Name' },
            { field: 'STATUS', label: 'Status' },
            { field: 'CATEGORY', label: 'Category' },
            { field: 'COMPANY_TYPE', label: 'Company Type' },
            { field: 'JEWISH_OWNED', label: 'Jewish Owned' },
            { field: 'LIST', label: 'List' },
            { field: 'PRODUCER', label: 'Producer' },
            { field: 'MARKETER', label: 'Marketer' },
            { field: 'SOURCE', label: 'Source' },
            { field: 'PRIVATE_LABEL', label: 'Private Label' },
            { field: 'PARENT_CO', label: 'Parent Company' },
            { field: 'RC', label: 'RC' }
        ],

        // Default columns for plant-related view (focused subset)
        defaultColumns: [
            { field: 'COMPANY_ID', label: 'Company ID' },
            { field: 'NAME', label: 'Company Name' },
            { field: 'STATUS', label: 'Status' },
            { field: 'CATEGORY', label: 'Category' },
            { field: 'RC', label: 'RC' }
        ],

        stringFields: ['NAME', 'CATEGORY', 'COMPANY_TYPE', 'STATUS', 'JEWISH_OWNED', 'LIST', 'PARENT_CO', 'RC'],

        include: 'COMPANY_TB',

        fields: {
            'OWNSTB': 'COMPANY_ID,PLANT_ID,START_DATE,END_DATE,TYPE,VISIT_FREQUENCY,INVOICE_TYPE,INVOICE_FREQUENCY,INVOICE_DTL,HOLD,ROYALTIES,SPECIAL_TICKET,STATUS,ID,ACTIVE,Setup_By,AcquiredFrom,NoRFRneeded,LOCtext,MoveToGP,DefaultPO,VisitBilling,PlantName,ShareAB,POexpiry,BillingName,PLANT_BILL_TO_NAME,AutoCertification,primaryCompany,Override,VisitPO,VisitPOexpiry,ValidFromTime,ValidToTime,CHANGESET_ID,BoilerplateInvoiceComment,IsCertBillingOverride'
        },

        baseFilters: [
            {
                name: 'ACTIVE',
                op: 'eq',
                val: 1
            }
        ],

        // Custom data processor for relationship endpoint
        dataProcessor: (responseData) => {
            const ownstbRecords = responseData.data || [];
            const companyIds = ownstbRecords.map(ownstb => ownstb.attributes?.COMPANY_ID).filter(id => id);

            return responseData.included
                ? responseData.included.filter(item =>
                    item.type === 'COMPANYTB' && companyIds.includes(parseInt(item.id))
                )
                : [];
        }
    },

    // Ingredients configuration - standalone mode
    ingredientsStandalone: {
        entityName: 'Label',
        entityNamePlural: 'labels',
        pageTitle: 'Labels',
        endpoint: 'LabelTb/',
        primaryNameField: 'BRAND_NAME',
        primaryIdField: 'ID',
        enableContextMenu: false,
        defaultSort: 'id',

        columns: [
            { field: 'ID', label: 'ID' },
            { field: 'BRAND_NAME', label: 'Brand Name' },
            { field: 'LABEL_NAME', label: 'Label Name' },
            { field: 'SYMBOL', label: 'Symbol' },
            { field: 'Status', label: 'Status' },
            { field: 'LABEL_TYPE', label: 'Label Type' },
            { field: 'GRP', label: 'Group' },
            { field: 'MERCHANDISE_ID', label: 'Merchandise ID' },
            { field: 'LABEL_SEQ_NUM', label: 'Sequence' }
        ],

        stringFields: ['BRAND_NAME', 'LABEL_NAME', 'SYMBOL', 'Status', 'LABEL_TYPE'],

        // Required fields parameter for this API
        fields: {
            'LabelTb': 'ID,MERCHANDISE_ID,LABEL_SEQ_NUM,SYMBOL,INSTITUTIONAL,BLK,SEAL_SIGN,GRP,SEAL_SIGN_FLAG,BRAND_NAME,SRC_MAR_ID,LABEL_NAME,INDUSTRIAL,CONSUMER,LABEL_TYPE,ACTIVE,SPECIAL_PRODUCTION,CREATE_DATE,LAST_MODIFY_DATE,STATUS_DATE,JEWISH_ACTION,CREATED_BY,MODIFIED_BY,LABEL_NUM,NUM_NAME,Confidential,AgencyID,LOChold,LOCholdDate,PassoverSpecialProduction,COMMENT,DisplayNewlyCertifiedOnWeb,Status,ValidFromTime,ValidToTime,CHANGESET_ID,LastChangeDate,LastChangeReason,LastChangeType,ReplacedByAgencyId,TransferredFromAgencyId,Kitniyot,IsDairyEquipment,NameNum'
        },

        fieldFormatters: {
            'INDUSTRIAL': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'CONSUMER': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'INSTITUTIONAL': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'SPECIAL_PRODUCTION': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'IsDairyEquipment': (value) => value ? 'Yes' : 'No'
        },

        baseFilters: [
            {
                name: 'ACTIVE',
                op: 'eq',
                val: 1
            },
            {
                name: 'LABEL_SEQ_NUM',
                op: 'gt',
                val: 1
            }
        ]
    },

    // Ingredients configuration - plant-related mode
    ingredientsPlantRelated: {
        entityName: 'Label',
        entityNamePlural: 'labels',
        pageTitle: 'Labels', // Will be updated with plant name
        endpoint: 'LabelTb/',
        primaryNameField: 'BRAND_NAME',
        primaryIdField: 'ID',
        enableContextMenu: false,
        defaultSort: 'id',

        columns: [
            { field: 'ID', label: 'ID' },
            { field: 'BRAND_NAME', label: 'Brand Name' },
            { field: 'LABEL_NAME', label: 'Label Name' },
            { field: 'SYMBOL', label: 'Symbol' },
            { field: 'Status', label: 'Status' },
            { field: 'LABEL_TYPE', label: 'Label Type' },
            { field: 'GRP', label: 'Group' },
            { field: 'MERCHANDISE_ID', label: 'Merchandise ID' },
            { field: 'LABEL_SEQ_NUM', label: 'Sequence' }
        ],

        stringFields: ['BRAND_NAME', 'LABEL_NAME', 'SYMBOL', 'Status', 'LABEL_TYPE'],

        // Required fields parameter for this API
        fields: {
            'LabelTb': 'ID,MERCHANDISE_ID,LABEL_SEQ_NUM,SYMBOL,INSTITUTIONAL,BLK,SEAL_SIGN,GRP,SEAL_SIGN_FLAG,BRAND_NAME,SRC_MAR_ID,LABEL_NAME,INDUSTRIAL,CONSUMER,LABEL_TYPE,ACTIVE,SPECIAL_PRODUCTION,CREATE_DATE,LAST_MODIFY_DATE,STATUS_DATE,JEWISH_ACTION,CREATED_BY,MODIFIED_BY,LABEL_NUM,NUM_NAME,Confidential,AgencyID,LOChold,LOCholdDate,PassoverSpecialProduction,COMMENT,DisplayNewlyCertifiedOnWeb,Status,ValidFromTime,ValidToTime,CHANGESET_ID,LastChangeDate,LastChangeReason,LastChangeType,ReplacedByAgencyId,TransferredFromAgencyId,Kitniyot,IsDairyEquipment,NameNum'
        },

        fieldFormatters: {
            'INDUSTRIAL': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'CONSUMER': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'INSTITUTIONAL': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'SPECIAL_PRODUCTION': (value) => value === 'Y' ? 'Yes' : value === 'N' ? 'No' : value,
            'IsDairyEquipment': (value) => value ? 'Yes' : 'No'
        },

        include: 'USEDIN1TBList,USEDIN1TBList.OWNSTB',

        baseFilters: [
            {
                name: 'ACTIVE',
                op: 'eq',
                val: 1
            },
            {
                name: 'LABEL_SEQ_NUM',
                op: 'gt',
                val: 1
            }
        ],

        specialFilters: ['PLANT_RELATION']
    }
};

/**
 * Helper function to get configuration based on page type and mode
 */
function getEntityConfig(entityType, mode = 'standalone', params = {}) {
    let configKey;

    switch (entityType) {
        case 'plants':
            configKey = 'plants';
            break;
        case 'companies':
            configKey = mode === 'plant-related' ? 'companiesPlantRelated' : 'companiesStandalone';
            break;
        case 'ingredients':
            configKey = mode === 'plant-related' ? 'ingredientsPlantRelated' : 'ingredientsStandalone';
            break;
        default:
            throw new Error(`Unknown entity type: ${entityType}`);
    }

    // Deep clone but preserve functions
    const config = Object.assign({}, EntityConfigs[configKey]);

    // Deep clone arrays and objects but preserve functions
    if (config.columns) {
        config.columns = config.columns.map(col => ({...col}));
    }
    if (config.baseFilters) {
        config.baseFilters = config.baseFilters.map(filter => ({...filter}));
    }
    if (config.stringFields) {
        config.stringFields = [...config.stringFields];
    }
    // Keep contextMenuActions, fieldFormatters, and dataProcessor as-is (they contain functions)

    // Apply dynamic parameters
    if (params.plantId && config.endpoint.includes('{plantId}')) {
        config.relationshipParams = { plantId: params.plantId };
    }

    if (params.plantName && mode === 'plant-related') {
        config.pageTitle = `${config.pageTitle} - ${params.plantName}`;
    }

    // Add plant relation filter for ingredients
    if (entityType === 'ingredients' && mode === 'plant-related' && params.plantId) {
        if (!config.baseFilters) config.baseFilters = [];

        // Add special filter that will be handled in buildFilterJson
        config.plantRelationFilter = {
            name: 'USEDIN1TBList.OWNSTB.PLANT_ID',
            op: 'eq',
            val: params.plantId
        };
    }

    return config;
}

// Make available globally
window.EntityConfigs = EntityConfigs;
window.getEntityConfig = getEntityConfig;