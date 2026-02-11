from flask import request, jsonify
import logging
import os
import time
import safrs
import traceback

from sympy import print_ccode
session = safrs.DB.session

from sqlalchemy import text
import json
from database.models import SubmissionApplication, SubmissionPlant, SubmissionProduct, SubmissionIngredient, SubmissionFileLink, SubmissionRawDatum
app_logger = logging.getLogger("api_logic_server_app")
api_key = os.environ.get('JOT_APIKEY')
team_id = os.environ.get('JOT_TEAM_ID')

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

    def map_submission(parsed_submission: list) -> dict:
        """
        Map JotForm SubmissionRawDatum to database model structure using JOTFORM_MAPPING_BY_TARGET.
        Groups data by target entity and uses field_name for proper mapping.
        
        Args:
            parsed_SubmissionRawDatum: List of dicts with 'order', 'text', 'name', 'answer' keys
            
        Returns:
            Dictionary with keys: 'main', 'contact', 'plant', 'plantContact', 'product', 'ingredient', 'file'
        """
        
        result = {
            'main': {},           # SubmissionApplication fields
            'plant': [],          # SubmissionPlant records
            'product': [],        # SubmissionProduct records
            'ingredient': [],     # SubmissionIngredient records
            'file': {}            # SubmissionFileLink records
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


    def insert_raw_data(submission_app_id, sub_list):
        for row in sub_list:
            jotform_raw = SubmissionRawDatum(
                SubmissionAppId=submission_app_id,
                entryorder=row.get('order'),
                prompt=row.get('text',''),   
                name =row.get('name'),
                control_type =row.get('type'),
                answer =row.get('answer')
            )
            if jotform_raw.answer != '':
                print(jotform_raw.prompt, ":    \t", jotform_raw.answer)
            session.add(jotform_raw)
                
       
    
    @app.route('/map_submission_form')
    def map_submission_form():
        # Start overall timer
        start_time = time.time()
        timings = {}
        
        args = request.args
        form_id = args.get('form_id')
        if not form_id:   
            return jsonify({ "error": "form_id parameter is required" }), 400

        # Check if Submission already exists to prevent duplicates
        
        
        if not api_key:
            print("Error: JotFormAPIKey environment variable not set")
            return jsonify({ "error": "JotFormAPIKey not configured" }), 500
        
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
            
            # Timer: Fetch JotForm data (OUTSIDE database transaction)
            fetch_start = time.time()
            print("Fetching JotForm data...")
            data = get_jotform_data(api_key, team_id, form_id, base_url)
            timings['fetch_api'] = round(time.time() - fetch_start, 3)
            
            # Get first Submission
            submissions = data['submissions'].get('content', [])
            if not submissions:
                print("No submissions found")
                return jsonify({ "error": "No submissions found" }), 404
        
            print(f"\nFound {len(submissions)} submission(s)")
            print("\nProcessing first submission...")
            
            # Timer: Parse Submission (OUTSIDE database transaction)
            parse_start = time.time()
            for submission in submissions:
                sub_list = parse_submission(submission)
                timings['parse_submission'] = round(time.time() - parse_start, 3)
                submission_id = submission.get('id')
                # Timer: Map to model structure (OUTSIDE database transaction)
                map_start = time.time()
                mapped_data = map_submission(sub_list)
                timings['map_to_model'] = round(time.time() - map_start, 3)                # Print mapped data structure
                print("\n" + "="*70)
                print("MAPPED DATA STRUCTURE")
                print("="*70)
                
                # =============================================================
                # DATABASE TRANSACTION - Keep this as SHORT as possible
                # =============================================================
                db_start = time.time()
                
                # Use a nested transaction with explicit rollback on error
                # This prevents deadlocks by keeping the transaction short
                try:
                    # Double-check for duplicate (race condition protection)
                    existing = session.query(SubmissionApplication).filter(
                        SubmissionApplication.submission_id == submission.get('id')
                    ).first()
                    if existing:
                        print({ 
                            "message": "Submission already processed (race condition)",
                            "Submission_id": submission.get('id'),
                            "SubmissionAppId": existing.SubmissionAppId,
                            "status": "duplicate"
                        })
                        continue
                    
                    # Timer: Insert main record
                    print("\n1. Main SubmissionApplication fields:")
                    submission_application = SubmissionApplication()
                    for key, value in mapped_data['main'].items():
                        print(f"   {key}: {value}")
                        setattr(submission_application, key, value)
                    setattr(submission_application, 'submission_id', submission.get('id'))
                    session.add(submission_application)
                    session.flush()  # Get the SubmissionAppId
                    submission_app_id = submission_application.SubmissionAppId
                    timings['db_insert_company'] = round(time.time() - db_start, 3)
                    
                    # Insert raw data
                    insert_raw_data(submission_app_id, sub_list)
                    # Timer: Insert plants
                    plant_ids = {}
                    plant_start = time.time()
                    print("\n3. Plants:")
                    for i, plant in enumerate(mapped_data['plant'], 1):
                        print(f"   Plant {i}:")
                        submission_plant = SubmissionPlant()
                        for key, value in plant.items():
                            print(f"      {key}: {value}")
                            setattr(submission_plant, key, value)
                        setattr(submission_plant, 'SubmissionAppId', submission_app_id)
                        session.add(submission_plant)
                        session.flush()  # Get PlantId for foreign key
                        plant_ids[i] = submission_plant.PlantId
                    timings['db_insert_plants'] = round(time.time() - plant_start, 3)
                    
                    # Timer: Insert products
                    product_start = time.time()
                    print("\n4. Products:")
                    for i, product in enumerate(mapped_data['product'], 1):
                        print(f"   Product {i}:")
                        submission_product = SubmissionProduct()
                        plant_number = product['plant_number']
                        for key, value in product.items():
                            print(f"      {key}: {value}")
                            setattr(submission_product, key, value)
                        setattr(submission_product, 'SubmissionPlantId', plant_ids[plant_number])
                        session.add(submission_product)
                    timings['db_insert_products'] = round(time.time() - product_start, 3)
                    
                    # Timer: Insert ingredients
                    ingredient_start = time.time()
                    print("\n5. Ingredients:")
                    for i, ingredient in enumerate(mapped_data['ingredient'], 1):
                        print(f"   Ingredient {i}:")
                        submission_ingredient = SubmissionIngredient()
                        plant_number = ingredient['plant_number']
                        for key, value in ingredient.items():
                            print(f"      {key}: {value}")
                            setattr(submission_ingredient, key, value)
                        setattr(submission_ingredient, 'SubmissionPlantId', plant_ids[plant_number])
                        session.add(submission_ingredient)
                    timings['db_insert_ingredients'] = round(time.time() - ingredient_start, 3)

                    # Timer: Insert files
                    files_start = time.time()
                    print("\n6. Files:")
                    submission_files = SubmissionFileLink()
                    if mapped_data['file']:
                        for key, value in mapped_data['file'].items():
                            print(f"   {key}: {value}")
                            setattr(submission_files, key, value[0] if isinstance(value,list) else value)
                    setattr(submission_files, 'SubmissionAppId', submission_app_id)
                    session.add(submission_files)
                    
                    # Single commit at the end
                    session.commit()
                    timings['db_insert_files'] = round(time.time() - files_start, 3)
                    
                except Exception as db_error:
                    # Rollback on any database error
                    session.rollback()
                    error_traceback = traceback.format_exc()
                    print(f"Database error: {error_traceback}")
                    
                    # Check if it's a deadlock error
                    if '40001' in str(db_error) or 'deadlock' in str(db_error).lower():
                        return jsonify({ 
                            "error": "Database deadlock detected. Please retry your request.",
                            "submission_id": submission_id,
                            "retry": True
                        }), 409  # Conflict status code
                    else:
                        return jsonify({ 
                            "error": f"Database error: {str(db_error)}",
                            "submission_id": submission_id
                        }), 500
                
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
                "message": f"Successfully processed Submission from JotForm",
                "submission_id": submission.get('id'),
                "form_id": submission_app_id,
                "mapped_data": mapped_data,
                "status": "success",
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
            # Make sure to rollback on any uncaught exception
            try:
                session.rollback()
            except:
                pass
            
            error_traceback = traceback.format_exc()
            print(error_traceback)
            print(f"Error fetching data from JotForm API: {e}")
            
            # Check if it's a deadlock error
            if '40001' in str(e) or 'deadlock' in str(e).lower():
                return jsonify({ 
                    "error": "Database deadlock detected. Please retry your request.",
                    "Submission_id": Submission_id,
                    "retry": True
                }), 409  # Conflict status code
            else:
                return jsonify({ 
                    "error": f"Error processing Submission: {str(e)}",
                    "traceback": error_traceback if app_logger.getEffectiveLevel() <= logging.DEBUG else None
                }), 500  