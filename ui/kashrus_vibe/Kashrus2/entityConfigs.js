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
        endpoint: 'v_plants/',
        primaryNameField: 'NAME',
        primaryIdField: 'PLANT_ID',
        statusField: 'STATUS',
        enableContextMenu: true,

        // Column definitions
        columns: [
            { field: 'PLANT_ID', label: 'Plant ID' },
            { field: 'NAME', label: 'Name' },
            { field: 'GP_NOTIFY', label: 'GP Notify' },
            { field: 'MULTILINES', label: 'Multi Lines' },
            { field: 'PASSOVER', label: 'Passover' },
            { field: 'SPECIAL_PROD', label: 'Special Prod' },
            { field: 'JEWISH_OWNED', label: 'Jewish Owned' },
            { field: 'PLANT_TYPE', label: 'Plant Type' },
            { field: 'PLANT_DIRECTIONS', label: 'Directions' },
            { field: 'ACTIVE', label: 'Active' },
            { field: 'USDA_CODE', label: 'USDA Code' },
            { field: 'PlantUID', label: 'Plant UID' },
            { field: 'DoNotAttach', label: 'Do Not Attach' },
            { field: 'OtherCertification', label: 'Other Certification' },
            { field: 'PrimaryCompany', label: 'Primary Company' },
            { field: 'DesignatedRFR', label: 'Designated RFR' },
            { field: 'ValidFromTime', label: 'Valid From' },
            { field: 'MaxOnSiteVisits', label: 'Max On-Site Visits' },
            { field: 'MaxVirtualVisits', label: 'Max Virtual Visits' },
            { field: 'IsDaily', label: 'Is Daily' },
            { field: 'PrimaryCompanyName', label: 'Primary Company Name' },
            { field: 'DesignatedRFRName', label: 'Designated RFR Name' },
            { field: 'STATUS', label: 'Status' }
        ],

        // Default columns to show initially
        defaultColumns: [
            { field: 'PLANT_ID', label: 'Plant ID' },
            { field: 'NAME', label: 'Name' },
            { field: 'PLANT_TYPE', label: 'Plant Type' },
            { field: 'PrimaryCompanyName', label: 'Primary Company Name' },
            { field: 'DesignatedRFRName', label: 'Designated RFR Name' },
            { field: 'STATUS', label: 'Status' }
        ],

        // Fields that support string-based filtering
        stringFields: ['NAME', 'PLANT_TYPE', 'USDA_CODE', 'PLANT_DIRECTIONS', 'PlantUID', 'OtherCertification', 'PrimaryCompany', 'DesignatedRFR', 'PrimaryCompanyName', 'DesignatedRFRName', 'STATUS'],

        // Required fields parameter for this API
        fields: {
            'v_plants': 'PLANT_ID,NAME,GP_NOTIFY,MULTILINES,PASSOVER,SPECIAL_PROD,JEWISH_OWNED,PLANT_TYPE,PLANT_DIRECTIONS,ACTIVE,USDA_CODE,PlantUID,DoNotAttach,OtherCertification,PrimaryCompany,DesignatedRFR,ValidFromTime,MaxOnSiteVisits,MaxVirtualVisits,IsDaily,PrimaryCompanyName,DesignatedRFRName,STATUS'
        },

        // Field formatters for special display logic
        fieldFormatters: {
            'JEWISH_OWNED': (value) => value ? 'Yes' : 'No',
            'SPECIAL_PROD': (value) => value ? 'Yes' : 'No',
            'GP_NOTIFY': (value) => value ? 'Yes' : 'No',
            'MULTILINES': (value) => value ? 'Yes' : 'No',
            'PASSOVER': (value) => value ? 'Yes' : 'No',
            'DoNotAttach': (value) => value ? 'Yes' : 'No',
            'IsDaily': (value) => value ? 'Yes' : 'No',
            'ValidFromTime': (value) => value ? new Date(value).toLocaleDateString() : 'N/A',
            'ValidToTime': (value) => value ? new Date(value).toLocaleDateString() : 'N/A'
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
        statusField: 'STATUS',
        enableContextMenu: true,

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
        ],

        // Context menu actions for companies
        contextMenuActions: {
            details: (item) => {
                displayService.showItemDetails(item.id);
            },
            plants: (item) => {
                const attributes = item.attributes || {};
                const plantsUrl = `plants.html?mode=company-related&companyId=${item.id}&companyName=${encodeURIComponent(attributes.NAME || 'Unknown Company')}`;
                window.open(plantsUrl, '_blank');
            },
            ingredients: (item) => {
                const attributes = item.attributes || {};
                const ingredientsUrl = `ingredients.html?mode=company-related&companyId=${item.id}&companyName=${encodeURIComponent(attributes.NAME || 'Unknown Company')}`;
                window.open(ingredientsUrl, '_blank');
            },
            products: (item) => {
                const attributes = item.attributes || {};
                const productsUrl = `products.html?mode=company-related&companyId=${item.id}&companyName=${encodeURIComponent(attributes.NAME || 'Unknown Company')}`;
                window.open(productsUrl, '_blank');
            }
        }
    },

    // Companies configuration - plant-related mode
    companiesPlantRelated: {
        entityName: 'Company',
        entityNamePlural: 'companies',
        pageTitle: 'Companies', // Will be updated with plant name
        endpoint: 'PLANTTB/{plantId}/OWNSTBList',
        primaryNameField: 'NAME',
        primaryIdField: 'COMPANY_ID',
        statusField: 'STATUS',
        enableContextMenu: true,

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

        // Context menu actions for companies (same as standalone)
        contextMenuActions: {
            details: (item) => {
                displayService.showItemDetails(item.id);
            },
            plants: (item) => {
                const attributes = item.attributes || {};
                const plantsUrl = `plants.html?mode=company-related&companyId=${item.id}&companyName=${encodeURIComponent(attributes.NAME || 'Unknown Company')}`;
                window.open(plantsUrl, '_blank');
            },
            ingredients: (item) => {
                const attributes = item.attributes || {};
                const ingredientsUrl = `ingredients.html?mode=company-related&companyId=${item.id}&companyName=${encodeURIComponent(attributes.NAME || 'Unknown Company')}`;
                window.open(ingredientsUrl, '_blank');
            },
            products: (item) => {
                const attributes = item.attributes || {};
                const productsUrl = `products.html?mode=company-related&companyId=${item.id}&companyName=${encodeURIComponent(attributes.NAME || 'Unknown Company')}`;
                window.open(productsUrl, '_blank');
            }
        },

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
        entityName: 'Ingredient',
        entityNamePlural: 'ingredients',
        pageTitle: 'Ingredients',
        endpoint: 'v_labels/',
        primaryNameField: 'BRAND_NAME',
        primaryIdField: 'ID',
        statusField: 'Status',
        enableContextMenu: true,
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

        // Default columns to show initially
        defaultColumns: [
            { field: 'ID', label: 'ID' },
            { field: 'BRAND_NAME', label: 'Brand Name' },
            { field: 'SYMBOL', label: 'Symbol' },
            { field: 'Status', label: 'Status' },
            { field: 'LABEL_TYPE', label: 'Label Type' }
        ],

        stringFields: ['BRAND_NAME', 'LABEL_NAME', 'SYMBOL', 'Status', 'LABEL_TYPE'],

        // Required fields parameter for this API
        fields: {
            'v_labels': 'ID,MERCHANDISE_ID,LABEL_SEQ_NUM,SYMBOL,INSTITUTIONAL,BLK,SEAL_SIGN,GRP,SEAL_SIGN_FLAG,BRAND_NAME,SRC_MAR_ID,LABEL_NAME,INDUSTRIAL,CONSUMER,LABEL_TYPE,ACTIVE,SPECIAL_PRODUCTION,CREATE_DATE,LAST_MODIFY_DATE,STATUS_DATE,JEWISH_ACTION,CREATED_BY,MODIFIED_BY,LABEL_NUM,NUM_NAME,Confidential,AgencyID,LOChold,LOCholdDate,PassoverSpecialProduction,COMMENT,DisplayNewlyCertifiedOnWeb,Status,ValidFromTime,LastChangeDate,LastChangeReason,LastChangeType,ReplacedByAgencyId,TransferredFromAgencyId,Kitniyot,IsDairyEquipment,NameNum,AS_STIPULATED,STIPULATION,RETAIL,FOODSERVICE,OUP_REQUIRED,GENERIC,SPECIFIED_SOURCE,SPECIFIED_SYMBOL,DESCRIPTION,DPM,PESACH,CONFIDENTIAL_TEXT,GROUP_COMMENT,LOC_CATEGORY,LOC_SELECTED,COMMENTS_SCHED_B,PROD_NUM,INTERMEDIATE_MIX,ALTERNATE_NAME,BrochoCode,Brocho2Code,CAS,LOC,UKDdisplay,Reviewed,TransferredTo,TransferredMerch,Special_Status'
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
        ],

        // Context menu actions for ingredients
        contextMenuActions: {
            details: (item) => {
                displayService.showItemDetails(item.id);
            },
            plants: (item) => {
                const attributes = item.attributes || {};
                const plantsUrl = `plants.html?mode=ingredient-related&ingredientId=${item.id}&ingredientName=${encodeURIComponent(attributes.BRAND_NAME || 'Unknown Ingredient')}`;
                window.open(plantsUrl, '_blank');
            },
            companies: (item) => {
                const attributes = item.attributes || {};
                const companiesUrl = `companies.html?mode=ingredient-related&ingredientId=${item.id}&ingredientName=${encodeURIComponent(attributes.BRAND_NAME || 'Unknown Ingredient')}`;
                window.open(companiesUrl, '_blank');
            },
            products: (item) => {
                const attributes = item.attributes || {};
                const productsUrl = `products.html?mode=ingredient-related&ingredientId=${item.id}&ingredientName=${encodeURIComponent(attributes.BRAND_NAME || 'Unknown Ingredient')}`;
                window.open(productsUrl, '_blank');
            }
        }
    },

    // Ingredients configuration - plant-related mode
    ingredientsPlantRelated: {
        entityName: 'Ingredient',
        entityNamePlural: 'ingredients',
        pageTitle: 'Ingredients', // Will be updated with plant name
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
    },

    // Products configuration - standalone mode (same as ingredients but with different title)
    productsStandalone: {
        entityName: 'Product',
        entityNamePlural: 'products',
        pageTitle: 'Products',
        endpoint: 'LabelTb/',
        primaryNameField: 'BRAND_NAME',
        primaryIdField: 'ID',
        statusField: 'Status',
        enableContextMenu: true,
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

        // Default columns to show initially
        defaultColumns: [
            { field: 'ID', label: 'ID' },
            { field: 'BRAND_NAME', label: 'Brand Name' },
            { field: 'SYMBOL', label: 'Symbol' },
            { field: 'Status', label: 'Status' },
            { field: 'LABEL_TYPE', label: 'Label Type' }
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
        ],

        // Context menu actions for products
        contextMenuActions: {
            details: (item) => {
                displayService.showItemDetails(item.id);
            },
            plants: (item) => {
                const attributes = item.attributes || {};
                const plantsUrl = `plants.html?mode=product-related&productId=${item.id}&productName=${encodeURIComponent(attributes.BRAND_NAME || 'Unknown Product')}`;
                window.open(plantsUrl, '_blank');
            },
            companies: (item) => {
                const attributes = item.attributes || {};
                const companiesUrl = `companies.html?mode=product-related&productId=${item.id}&productName=${encodeURIComponent(attributes.BRAND_NAME || 'Unknown Product')}`;
                window.open(companiesUrl, '_blank');
            },
            ingredients: (item) => {
                const attributes = item.attributes || {};
                const ingredientsUrl = `ingredients.html?mode=product-related&productId=${item.id}&productName=${encodeURIComponent(attributes.BRAND_NAME || 'Unknown Product')}`;
                window.open(ingredientsUrl, '_blank');
            }
        }
    },

    // Plants configuration - company-related mode
    plantsCompanyRelated: {
        entityName: 'Plant',
        entityNamePlural: 'plants',
        pageTitle: 'Plants', // Will be updated with company name
        endpoint: 'COMPANYTB/{companyId}/PLANTTBList',
        primaryNameField: 'NAME',
        primaryIdField: 'PLANT_ID',
        enableContextMenu: true,

        columns: [
            { field: 'PLANT_ID', label: 'ID' },
            { field: 'NAME', label: 'Name' },
            { field: 'PLANT_TYPE', label: 'Type' },
            { field: 'USDA_CODE', label: 'USDA Code' },
            { field: 'JEWISH_OWNED', label: 'Jewish Owned' },
            { field: 'SPECIAL_PROD', label: 'Special Prod' },
            { field: 'PLANT_DIRECTIONS', label: 'Directions' },
            { field: 'GP_NOTIFY', label: 'GP Notify' },
            { field: 'MULTILINES', label: 'Multi Lines' },
            { field: 'PASSOVER', label: 'Passover' },
            { field: 'PlantUID', label: 'Plant UID' },
            { field: 'DoNotAttach', label: 'Do Not Attach' },
            { field: 'OtherCertification', label: 'Other Certification' },
            { field: 'PrimaryCompany', label: 'Primary Company' },
            { field: 'DesignatedRFR', label: 'Designated RFR' },
            { field: 'ValidFromTime', label: 'Valid From' },
            { field: 'ValidToTime', label: 'Valid To' },
            { field: 'MaxOnSiteVisits', label: 'Max On-Site Visits' },
            { field: 'MaxVirtualVisits', label: 'Max Virtual Visits' },
            { field: 'IsDaily', label: 'Is Daily' }
        ],

        stringFields: ['NAME', 'PLANT_TYPE', 'USDA_CODE', 'PLANT_DIRECTIONS', 'PlantUID', 'OtherCertification', 'PrimaryCompany', 'DesignatedRFR'],

        fieldFormatters: {
            'JEWISH_OWNED': (value) => value ? 'Yes' : 'No',
            'SPECIAL_PROD': (value) => value ? 'Yes' : 'No',
            'GP_NOTIFY': (value) => value ? 'Yes' : 'No',
            'MULTILINES': (value) => value ? 'Yes' : 'No',
            'PASSOVER': (value) => value ? 'Yes' : 'No',
            'DoNotAttach': (value) => value ? 'Yes' : 'No',
            'IsDaily': (value) => value ? 'Yes' : 'No',
            'ValidFromTime': (value) => value ? new Date(value).toLocaleDateString() : 'N/A',
            'ValidToTime': (value) => value ? new Date(value).toLocaleDateString() : 'N/A'
        },


        baseFilters: [
            {
                name: 'ACTIVE',
                op: 'eq',
                val: 1
            }
        ],

        // Context menu actions for company-related plants
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
            products: (item) => {
                const attributes = item.attributes || {};
                const productsUrl = `products.html?mode=plant-related&plantId=${item.id}&plantName=${encodeURIComponent(attributes.NAME || 'Unknown Plant')}`;
                window.open(productsUrl, '_blank');
            }
        }
    }
};

/**
 * Helper function to get configuration based on page type and mode
 */
function getEntityConfig(entityType, mode = 'standalone', params = {}) {
    let configKey;

    switch (entityType) {
        case 'plants':
            configKey = mode === 'company-related' ? 'plantsCompanyRelated' : 'plants';
            break;
        case 'companies':
            configKey = mode === 'plant-related' ? 'companiesPlantRelated' : 'companiesStandalone';
            break;
        case 'ingredients':
            configKey = mode === 'plant-related' ? 'ingredientsPlantRelated' : 'ingredientsStandalone';
            break;
        case 'products':
            configKey = 'productsStandalone'; // Only standalone mode for now
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
    if (config.defaultColumns) {
        config.defaultColumns = config.defaultColumns.map(col => ({...col}));
    } else {
        // Inherit defaultColumns from standalone configuration if not present
        let standaloneConfigKey;
        switch (entityType) {
            case 'companies':
                if (mode === 'plant-related') standaloneConfigKey = 'companiesStandalone';
                break;
            case 'plants':
                if (mode === 'company-related') standaloneConfigKey = 'plants';
                break;
            case 'ingredients':
                if (mode === 'plant-related') standaloneConfigKey = 'ingredientsStandalone';
                break;
        }

        if (standaloneConfigKey && EntityConfigs[standaloneConfigKey]?.defaultColumns) {
            config.defaultColumns = EntityConfigs[standaloneConfigKey].defaultColumns.map(col => ({...col}));
        }
    }
    // Keep contextMenuActions, fieldFormatters, and dataProcessor as-is (they contain functions)

    // Apply dynamic parameters
    if (params.plantId && config.endpoint.includes('{plantId}')) {
        config.relationshipParams = { plantId: params.plantId };
    }

    if (params.companyId && config.endpoint.includes('{companyId}')) {
        config.relationshipParams = { companyId: params.companyId };
    }

    if (params.plantName && mode === 'plant-related') {
        config.pageTitle = `${config.pageTitle} - ${params.plantName}`;
    }

    if (params.companyName && mode === 'company-related') {
        config.pageTitle = `${config.pageTitle} - ${params.companyName}`;
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