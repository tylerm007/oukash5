from math import e
from unittest import result
from flask import request, jsonify
from database import models
import logging
import time
from integration.vector_store.vector_store import add_plant_to_vectorstore, find_matching
from integration.matchers.matcher import ( 
    MatchConfig, 
    MatchTier,
    match_plant,
)

import safrs
from sqlalchemy import text
import json

session = safrs.DB.session
EXISTING_PLANTS = None

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    pass
    
    @app.route('/load_existing_plants', methods=['GET'])
    def load_plants():
        args = request.args
        plant_id = args.get('plant_id', default=2539, type=int)
        global EXISTING_PLANTS
        if EXISTING_PLANTS is None:
            EXISTING_PLANTS = load_existing_plants()
       
        plant = session.query(models.Facility).filter_by(facility_id=plant_id).first()
        if plant is None:
            return jsonify({ "error": f"Plant {plant_id} not found" }), 404
            
        # Get the first address from the AddressList (it's a list, not a method)
        address_list = plant.AddressList
        address = address_list[0] if address_list else None
        plant.FacilityContactList
        
        if address is None:
            return jsonify({ "error": f"Plant {plant_id} has no addresses" }), 404
            
        match = {
           'name': plant.facility_name,
           'street': address.street_address,
           'city': address.city,
           'state': address.state_province,
           'postal': address.postal_code,
           #'phone': plant.get('phone'),
           #"website": plant.get('website')
        }
        
        for plant_data in EXISTING_PLANTS:
            add_plant_to_vectorstore(plant_data)
        results = find_matching(match, k=3, use_company_vectorstore=False)

        for plant_data, score in results:
            print(f"Score: {score:.4f}")
            print(f"  Plant: {plant_data}")
        return jsonify({
            "record_count": len(EXISTING_PLANTS)
        }), 200
    

    @app.route('/match_plant')
    def plantmatch():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://devvm01.nyc.ou.org:5655/match_plant?plant_id=1
        """
        # Initialize timers
        timers = {}
        global EXISTING_PLANTS
        plant_id = request.args.get('plant_id', default=1, type=int)
        plant = session.query(models.SubmissionPlant).filter_by(PlantId=plant_id).first()
        if plant is None:
            return jsonify({ "error": f"SubmissionPlant {plant_id} not found" }), 404
            
        #address_list = plant.AddressList
        #address = address_list[0] if address_list else None
        match = {
           'name': plant.facility_name,
           'street': plant.plantAddress,
           'city': plant.plantCity,
           'state': plant.plantState,
           'postal': plant.plantZip,
           'phone': plant.contactPhone,
           "website": None
        }
        '''
        match =  {
            'name': 'A B Food Company-Philadelphia',  # Missing Inc., uppercase
            'street': 'Blue Grass Road & Grant Avenue',  # Abbreviated
            'city': 'Philadelphia',
            'state': 'PA',
            'postal': '19114',
            'phone': '315-781-8772'
        }
        '''
        # Time SQL execution
        sql_start = time.time()
        if EXISTING_PLANTS is None:
            EXISTING_PLANTS = load_existing_plants()
        sql_end = time.time()
        timers['sql_processing_ms'] = round((sql_end - sql_start) * 1000, 2)

        # Time plant execution
        match_start = time.time()
        result = match_plant(match, EXISTING_PLANTS, MatchConfig())
        match_end = time.time()
        timers['match_plant_ms'] = round((match_end - match_start) * 1000, 2)
        
        # Calculate total time
        timers['total_ms'] = round(timers['sql_processing_ms'] + timers['match_plant_ms'], 2)
        
        return jsonify({
            "result": result,
            "match_plant": match,
            "meta": {
                "timings": timers,
                "record_count": len(EXISTING_PLANTS)
            }
        }), 200

    @app.route("/match_plant_vectorstore", methods=["GET"])
    def match_plant_vectorstore():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://devvm01.nyc.ou.org:5655/match_plant_vectorstore?plant_id=1
        """
        args = request.args
        plant_id = args.get('plant_id', default=3, type=int)
        
        plant = session.query(models.SubmissionPlant).filter_by(PlantId=plant_id).first()
        if plant is None:
            return jsonify({ "error": f"SubmissionPlant {plant_id} not found" }), 404

        match = {
           'name': plant.plantName,
           'street': plant.plantAddress,
           'street1': None,
           'city': plant.plantCity,
           'state': plant.plantState,
           'postal': plant.plantZip,
           'phone': plant.contactPhone,
           'country': plant.plantCountry,
           "website": None
        }
        results = find_matching(match, k=3, score_threshold=0.85, use_company_vectorstore=False)

        if results:
            print(f"Found {len(results)} matching plants:\n")
            for i, (plant_data, similarity_pct) in enumerate(results, 1):
                # Determine match quality
                if similarity_pct >= 95:
                    quality = "Excellent"
                elif similarity_pct >= 85:
                    quality = "Good"
                elif similarity_pct >= 70:
                    quality = "Moderate"
                else:
                    quality = "Weak"
                
                print(f"{i}. Match: {similarity_pct}% ({quality})")
                print(f"   ID: {plant_data.get('id', 'N/A')}")
                print(f"   Name: {plant_data.get('name', 'Unknown')}")
                print(f"   Address: {plant_data.get('street', '')}, {plant_data.get('city', '')}, {plant_data.get('state', '')} {plant_data.get('postal', '')}")
                print(f"   Phone: {plant_data.get('phone', 'N/A')}")
                #print(f"   Website: {plant_data.get('website', 'N/A')}")
                print()
        else:
            print("No matching plants found above 85% threshold.")
        
        return jsonify({
            "match_plant": match,
            "matches": [
                {
                    "plant_data": plant_data,
                    "similarity_pct": similarity_pct
                }
                for plant_data, similarity_pct in results
            ]
        }), 200

def load_existing_plants():
    results = session.execute(text(get_plant_sql())).fetchall()
    existing = []
    json_data = []
    # SQL Server FOR JSON AUTO returns complete JSON string
    # Concatenate all fragments from the result rows
    for row in results:
        # Each row contains a JSON fragment that needs to be concatenated
        if row and row[0]:
            json_data.append(row[0])
    
    # Join all JSON fragments into a single JSON string
    json_str = ''.join(json_data) if json_data else '[]'
    json_data = json.loads(json_str)
    for row in json_data:
        data = row
        if 'c' in data:
            data['street'] = data['c'][0]['street'] if 'street' in data['c'][0] else None
            data['street2'] = data['c'][0]['street2'] if 'street2' in data['c'][0] else None
            data['street3'] = data['c'][0]['street3'] if 'street3' in data['c'][0] else None
            data['city'] = data['c'][0]['city'] if 'city' in data['c'][0] else None
            data['state'] = data['c'][0]['state'] if 'state' in data['c'][0] else None
            data['postal'] = data['c'][0]['postal'] if 'postal' in data['c'][0] else None
            data['country'] = data['c'][0]['country'] if 'country' in data['c'][0] else None    
            data.pop('c', None)  # Remove the nested 'c' key after extracting
        if 'p' in data:
            data['name'] = data['p'][0]['name']
            #data['id'] = data['p'][0]['id']
            #data['phone'] = data['p'][0]['cc'][0]['phone']
            data.pop('p', None)  # Remove the nested 'p' key after extracting the name   
        existing.append(data)
    return existing

def _match_plant_async(match:dict)-> list:
    # This is a placeholder for an asynchronous version of match_plant if needed in the future.
    # For now, it simply calls the synchronous version.
    
    results = find_matching(match, k=3, score_threshold=0.85, use_company_vectorstore=False)

    if results:
        print(f"Found {len(results)} matching plants:\n")
        for i, (plant_data, similarity_pct) in enumerate(results, 1):
            # Determine match quality
            if similarity_pct >= 95:
                quality = "Excellent"
            elif similarity_pct >= 85:
                quality = "Good"
            elif similarity_pct >= 70:
                quality = "Moderate"
            else:
                quality = "Weak"
            
            print(f"{i}. Match: {similarity_pct}% ({quality})")
            print(f"   ID: {plant_data.get('id', 'N/A')}")
            print(f"   Name: {plant_data.get('name', 'Unknown')}")
            print(f"   Address: {plant_data.get('street', '')}, {plant_data.get('city', '')}, {plant_data.get('state', '')} {plant_data.get('postal', '')}")
            print(f"   Phone: {plant_data.get('phone', 'N/A')}")
            #print(f"   Website: {plant_data.get('website', 'N/A')}")
            print()
    else:
        print("No matching plants found above 85% threshold.")
    
    return {
        "match_plant": match,
        "matches": [
            {
                "plant_data": plant_data,
                "similarity_pct": similarity_pct
            }
            for plant_data, similarity_pct in results
        ]
    }

def get_plant_sql():
    return """
       SELECT 
        -- TOP (1000) 
        -- [ID] as 'id'
        p.[PLANT_ID] as 'id'
        ,[NAME] as 'name'
        --,[ADDRESS_SEQ_NUM]
        --,[TYPE]
        --,[ATTN]
        ,[STREET1] as 'street'
        ,[STREET2] as 'street2'
        ,[STREET3] as 'street3'
        ,[CITY] as 'city'
        ,[STATE] as 'state'
        ,[ZIP] as 'postal'
        ,[COUNTRY] as 'country'
        , null as 'phone'
        , null as 'website'
    FROM [ou_kash].[dbo].[PLANT_ADDRESS_TB] c
    JOIN [ou_kash].[dbo].[PLANT_TB] p on p.PLANT_ID = c.PLANT_ID
    --JOIN [ou_kash].[dbo].[PlantContacts] pc on pc.owns_ID in 
    --(select o.PLANT_ID
                --FROM [ou_kash].[dbo].[OWNS_TB] o
                --JOIN [ou_kash].[dbo].COMPANY_TB c
                --on c.COMPANY_ID = o.COMPANY_ID)
    where c.STREET1 != '' and c.ACTIVE = 1
    and c.PLANT_ID in
                (select o.PLANT_ID
                FROM [ou_kash].[dbo].[OWNS_TB] o
                JOIN [ou_kash].[dbo].[PLANT_TB] p
                on p.PLANT_ID = o.PLANT_ID)
    FOR JSON AUTO
    """