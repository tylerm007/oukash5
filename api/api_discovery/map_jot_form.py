from flask import request, jsonify
import logging
import os
import time
import safrs
import traceback
session = safrs.DB.session

from sqlalchemy import text
import json
from database.models import JotFormCompany, JotFormPlant, JotFormProduct, JotFormIngredient, JotFormFileLink, JotFormRawDatum
app_logger = logging.getLogger("api_logic_server_app")
api_key = os.environ.get('JotFormAPIKey') or "6a43a5bd9eb0000522ee130271621f53"

# Load JotForm mapping configuration
#MAPPING_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'integration', 'jotfrom', 'JotFormMapping.json')
MAPPING_BY_TARGET_FILE = os.path.join(os.path.dirname(__file__), '..', '..', 'integration', 'jotfrom', 'JotFormMapping_by_target.json')

# Load mapping data
#with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
#    JOTFORM_MAPPING = json.load(f)

with open(MAPPING_BY_TARGET_FILE, 'r', encoding='utf-8') as f:
    JOTFORM_MAPPING_BY_TARGET = json.load(f)

#print(f"✓ Loaded {len(JOTFORM_MAPPING)} JotForm field mappings")
print(f"✓ Loaded mappings for targets: {', '.join(JOTFORM_MAPPING_BY_TARGET.keys())}")
    
# Mapping from JotForm field names to JotFormDatum model attributes
def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass

    def map_jotform(parsed_submission: list) -> dict:
        """
        Map JotForm submission data to database model structure using JOTFORM_MAPPING_BY_TARGET.
        Groups data by target entity and uses field_name for proper mapping.
        
        Args:
            parsed_submission: List of dicts with 'order', 'text', 'name', 'answer' keys
            
        Returns:
            Dictionary with keys: 'main', 'contact', 'plant', 'plantContact', 'product', 'ingredient', 'file'
        """
        
        result = {
            'main': {},           # JotFormCompany fields
            'plant': [],          # JotFormPlant records
            'product': [],        # JotFormProduct records
            'ingredient': [],     # JotFormIngredient records
            'file': {}            # JotFormFileLink records
        }
        
        # Create lookup index by jot_field name for fast access
        plant_data = {}
        for target in JOTFORM_MAPPING_BY_TARGET:
            mapping_index = {}
            mappings = JOTFORM_MAPPING_BY_TARGET[target]
            for row in mappings:
                mapping_index[f'{row["prompt"]}:{row["jot_field"]}'] = row
                
            # Track current plant context for fields that follow plant declarations
            current_plant_num = None

            for field_dict in parsed_submission:
                data = dict(field_dict)
                jot_field = data.get('name')
                answer = data.get('answer')
                text = data.get('text', '')
                order = data.get('order')
                mapping = mapping_index.get(f'{text}:{jot_field}')
                if not mapping or not answer or answer == '' or answer == '[]':
                    continue
                
                field_name = mapping.get('field_name')
                plant_num = mapping.get('plant_number')
                current_plant_num = int(plant_num) if str(plant_num ).isdigit() else current_plant_num
                prompt = mapping.get('prompt', '')                
                # === MAIN ENTITY ===
                if target == 'main':
                    # Handle boolean fields
                    if field_name in ['OUcertified', 'everCertified', 'veganCert', 'listInCopack']:
                        result['main'][field_name] = answer.lower() in ['yes', 'true', '1', 'y']
                    # Handle integer fields
                    elif field_name == 'numberOfPlants':
                        result['main'][field_name] = int(answer) if str(answer).isdigit() else 1
                    else:
                        result['main'][field_name] = answer
                
                
                # === PLANT ENTITY ===
                elif target == 'plant':
                    if  current_plant_num is None:
                        continue  # Default to plant 1
                    
                    # Initialize plant dict if not exists
                    if current_plant_num not in plant_data:
                        plant_data[current_plant_num] = {'plantNumber': current_plant_num}
                    
                    # Handle boolean fields
                    
                    if field_name in ['otherProducts', 'areAny']:
                        plant_data[current_plant_num][field_name] = answer.lower() in ['yes', 'true', '1', 'y']
                    else:
                        plant_data[current_plant_num][field_name] = answer
                    
                
                # === PRODUCT ENTITY ===
                elif target == 'product':
                    # Products are stored as JSON arrays in the form
                    try:
                        if answer.startswith('['):
                            products_list = json.loads(answer)
                            for prod in products_list:
                                result['product'].append({
                                    'plant_number': current_plant_num or 1,
                                    'productName': prod.get('Product Name'),
                                    'retail': prod.get('Retail?', '').lower() in ['y', 'yes', 'true', '1'],
                                    'industrial': prod.get('Industrial?', '').lower() in ['y', 'yes', 'true', '1'],
                                    'brandName': prod.get('Brand Name'),
                                    'inHouse': prod.get('In-house?', '').lower() in ['y', 'yes', 'true', '1'],
                                    'privateLabel': prod.get('Private Label?', '').lower() in ['y', 'yes', 'true', '1'],
                                    'privateLabelCo': prod.get('Private Label Co')
                                })
                    except:
                        pass
                
                # === INGREDIENT ENTITY ===
                elif target == 'ingredient':
                    # Ingredients are stored as JSON arrays in the form
                    try:
                        if answer.startswith('['):
                            ingredients_list = json.loads(answer)
                            for ing in ingredients_list:
                                result['ingredient'].append({
                                    'plant_number': current_plant_num or 1,
                                    'ukdId': ing.get('UKD-ID'),
                                    'rawMaterialCode': ing.get('Raw Material Code'),
                                    'ingredientLabelName': ing.get('Ingredient Label Name'),
                                    'manufacturer': ing.get('Manufacturer'),
                                    'brandName': ing.get('Brand Name'),
                                    'packagedBulk': ing.get('Packaged/Bulk'),
                                    'certifyingAgency': ing.get('Certifying Agency')
                                })
                    except:
                        pass
                
                # === FILE ENTITY ===
                elif target == 'file':
                    if answer and answer != '[]':
                        result['file'][field_name] = answer
        
        # Convert plant dict to list
        result['plant'] = list(plant_data.values())
        
        return result


    def insert_raw_data(jotform_id, sub_list):
        for row in sub_list:
            jotform_raw = JotFormRawDatum(
                JotFormId=jotform_id,
                entryorder=row.get('order'),
                prompt=row.get('text',''),   
                name =row.get('name'),
                control_type =row.get('type'),
                answer =row.get('answer')
            )
            if jotform_raw.answer != '':
                print(jotform_raw.prompt, ":    \t", jotform_raw.answer)
            session.add(jotform_raw)
                
       
    
    @app.route('/map_jot_form')
    def map_jot_form():
        # Start overall timer
        start_time = time.time()
        timings = {}
        
        args = request.args
        submission_id = args.get('submission_id')
        if not submission_id:   
            return jsonify({ "error": "submission_id parameter is required" }), 400

        
        if not api_key:
            print("Error: JotFormAPIKey environment variable not set")
            return
        
        # JotForm configuration
        base_url = "https://ou.jotform.com"
        team_id = "240425799590063"
        
        # Form IDs
        #form_id_prod = "260253336843860" #"243646438272058"  # PROD Kashrus Application form
        #form_id_test = "253065393574867"  # TEST application form
        
        # Use PROD form
        #form_id = form_id_prod          
        
        try:
            from integration.jotfrom.jotform_submission_queries import get_jotform_data, parse_submission
            
            # Timer: Fetch JotForm data
            fetch_start = time.time()
            print("Fetching JotForm data...")
            data = get_jotform_data(api_key, team_id, submission_id, base_url)
            timings['fetch_api'] = round(time.time() - fetch_start, 3)
            
            # Get first submission
            submissions = data['submissions'].get('content', [])
            if not submissions:
                print("No submissions found")
                return
        
            print(f"\nFound {len(submissions)} submission(s)")
            print("\nProcessing first submission...")
            
            # Timer: Parse submission
            parse_start = time.time()
            submission = submissions[0]
            sub_list = parse_submission(submission)
            timings['parse_submission'] = round(time.time() - parse_start, 3)
            
            # Timer: Map to model structure
            map_start = time.time()
            mapped_data = map_jotform(sub_list)
            timings['map_to_model'] = round(time.time() - map_start, 3)
            
            #print(f"\nSubmission ID: {submission.get('id', 'N/A')}")
            #print(f"Submission Date: {submission.get('created_at', 'N/A')}")
            #print(f"\nParsed Fields ({len(sub_list)}):\n")
            
            #result = print_submission_table(sub_list)
            
            # Print mapped data structure
            print("\n" + "="*70)
            print("MAPPED DATA STRUCTURE")
            print("="*70)
            
            # Timer: Insert main record
            db_start = time.time()
            print("\n1. Main JotFormCompany fields:")
            jotform = JotFormCompany()
            for key, value in mapped_data['main'].items():
                print(f"   {key}: {value}")
                setattr(jotform, key, value)
            setattr(jotform, 'submission_id', submission_id)
            session.add(jotform)
            session.flush()
            jot_form_id = jotform.JotFormId
            timings['db_insert_company'] = round(time.time() - db_start, 3)
            # Insert raw data
            insert_raw_data(jot_form_id, sub_list)

            # Timer: Insert plants
            plant_ids = {}
            plant_start = time.time()
            print("\n3. Plants:")
            for i, plant in enumerate(mapped_data['plant'], 1):
                print(f"   Plant {i}:")
                jotform_plant = JotFormPlant()
                for key, value in plant.items():
                    print(f"      {key}: {value}")
                    setattr(jotform_plant, key, value)
                setattr(jotform_plant, 'JotFormId', jot_form_id)
                session.add(jotform_plant)
                session.flush()
                plant_ids[i] = jotform_plant.PlantId
            timings['db_insert_plants'] = round(time.time() - plant_start, 3)
            
            # Timer: Insert products
            product_start = time.time()
            print("\n4. Products:")
            for i, product in enumerate(mapped_data['product'], 1):
                print(f"   Product {i}:")
                jotform_product = JotFormProduct()
                plant_number = product['plant_number']
                for key, value in product.items():
                    print(f"      {key}: {value}")
                    setattr(jotform_product, key, value)
                setattr(jotform_product, 'JotPlantId', plant_ids[plant_number])
                session.add(jotform_product)
            timings['db_insert_products'] = round(time.time() - product_start, 3)
            
            # Timer: Insert ingredients
            ingredient_start = time.time()
            print("\n5. Ingredients:")
            for i, ingredient in enumerate(mapped_data['ingredient'], 1):
                print(f"   Ingredient {i}:")
                jotform_ingredient = JotFormIngredient()
                plant_number = ingredient['plant_number']
                for key, value in ingredient.items():
                    print(f"      {key}: {value}")
                    setattr(jotform_ingredient, key, value)
                setattr(jotform_ingredient, 'JotPlantId', plant_ids[plant_number])
                session.add(jotform_ingredient)
            timings['db_insert_ingredients'] = round(time.time() - ingredient_start, 3)

            timings['db_insert_ingredients'] = round(time.time() - ingredient_start, 3)

            # Timer: Insert files
            files_start = time.time()
            print("\n6. Files:")
            jotform_files = JotFormFileLink()
            if mapped_data['file']:
                for key, value in mapped_data['file'].items():
                    print(f"   {key}: {value}")
                    setattr(jotform_files, key, value[0] if isinstance(value,list) else value)
            setattr(jotform_files, 'JotFormId', jot_form_id)
            session.add(jotform_files)
            session.commit()
            timings['db_insert_files'] = round(time.time() - files_start, 3)
            
            # Calculate total time
            timings['total'] = round(time.time() - start_time, 3)
            
            # Calculate database total
            timings['db_total'] = round(
                timings['db_insert_company'] +  
                timings['db_insert_plants'] + 
                timings['db_insert_products'] + 
                timings['db_insert_files'], 3
            )
            
            print("\n" + "="*70)
            print("PERFORMANCE TIMINGS (seconds)")
            print("="*70)
            print(f"API Fetch:         {timings['fetch_api']}s")
            print(f"Parse Submission:  {timings['parse_submission']}s")
            print(f"Map to Model:      {timings['map_to_model']}s")
            print(f"DB Insert Main:    {timings['db_insert_company']}s")
            print(f"DB Insert Plants:  {timings['db_insert_plants']}s")
            print(f"DB Insert Products: {timings['db_insert_products']}s")
            print(f"DB Insert Files:   {timings['db_insert_files']}s")
            print(f"DB Total:          {timings['db_total']}s")
            print(f"TOTAL:             {timings['total']}s")
            print("="*70)
            
            return jsonify({
                "message": f"Fetched and mapped {len(submissions)} submissions from JotForm",
                "submission_id": submission.get('id'),
                "jotform_id": jot_form_id,
                "mapped_data": mapped_data,
                "meta": {
                    "timings": timings,
                    "performance_summary": {
                        "api_operations": round(timings['fetch_api'] + timings['parse_submission'], 3),
                        "data_processing": timings['map_to_model'],
                        "database_operations": timings['db_total'],
                        "total_duration": timings['total']
                    }
                }
            }), 200
        except Exception as e:
            error_traceback = traceback.format_exc()
            print(error_traceback)
            print(f"Error fetching data from JotForm API: {e}")
            return jsonify({ "error": f"Error fetching data from JotForm API: {e}" }), 500

        return jsonify({ "message": f"Fetched {len(submissions)} submissions from JotForm" }), 200  