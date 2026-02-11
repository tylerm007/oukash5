from math import e
from unittest import result
from flask import request, jsonify
from database import models
import logging
import time
from integration.vector_store.vector_store import add_company_to_vectorstore, find_matching
from integration.matchers.matcher import (
    CompanyMatcher, 
    MatchConfig, 
    MatchTier,
    match_company,
)

import safrs
from sqlalchemy import text
import json

session = safrs.DB.session
EXISTING_COMPANIES = None

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators = []):
    pass

    @app.route('/load_existing_companies', methods=['GET'])
    def load_companies():
        args = request.args
        company_id = args.get('company_id', default=2539, type=int)
        global EXISTING_COMPANIES
        if EXISTING_COMPANIES is None:
            EXISTING_COMPANIES = load_existing_companies()

        company = session.query(models.Company).filter_by(company_id=company_id).first()
        if company is None:
            return jsonify({ "error": f"Company {company_id} not found" }), 404
            
        # Get the first address from the AddressList (it's a list, not a method)
        address_list = company.AddressList
        address = address_list[0] if address_list else None
        
        if address is None:
            return jsonify({ "error": f"Company {company_id} has no addresses" }), 404
            
        match = {
           'name': company.company_name,
           'street': address.street_address,
           'city': address.city,
           'state': address.state_province,
           'postal': address.postal_code,
           'phone': company.phone,
           "website": company.website
        }
        for company_data in EXISTING_COMPANIES:
            add_company_to_vectorstore(company_data)
        results = find_matching(match, k=3)

        for company_data, score in results:
            print(f"Score: {score:.4f}")
            print(f"  Company: {company_data}")
        return jsonify({
            "record_count": len(EXISTING_COMPANIES)
        }), 200
    
    @app.route("/match_company_vectorstore", methods=["GET"])
    def match_company_vectorstore():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://devvm01.nyc.ou.org:5655/match_company_vectorstore?app_id=1
        """
        args = request.args
        app_id = args.get('app_id', default=0, type=int)
        if app_id == 0:
            return jsonify({ "error": "app_id parameter is required" }), 400
        company = session.query(models.SubmissionApplication).filter_by(SubmissionAppId=app_id).first()
        if company is None:
            return jsonify({ "error": f"SubmissionApplication {app_id} not found" }), 404
        email = (company.contactEmail).split('@')[1] if company.contactEmail and "@" in company.contactEmail else None
        match = {
           'name': company.companyName,
           'street': company.companyAddress,
           'street1': company.companyAddress2,
           'city': company.companyCity,
           'state': company.companyState,
           'postal': company.ZipPostalCode,
           'phone': company.companyPhone,
           'country': company.companyCountry,
           "website": company.companyWebsite if company.companyWebsite else (f"http://www.{email}" if email else None)      
        }
        results = find_matching(match, k=3, score_threshold=0.75)

        if results:
            print(f"Found {len(results)} matching companies:\n")
            for i, (company_data, similarity_pct) in enumerate(results, 1):
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
                print(f"   ID: {company_data.get('id', 'N/A')}")
                print(f"   Name: {company_data.get('name', 'Unknown')}")
                print(f"   Address: {company_data.get('street', '')}, {company_data.get('city', '')}, {company_data.get('state', '')} {company_data.get('postal', '')}")
                print(f"   Phone: {company_data.get('phone', 'N/A')}")
                print(f"   Website: {company_data.get('website', 'N/A')}")
                print()
        else:
            print("No matching companies found above 75% threshold.")
        
        return jsonify({
            "match_company": match,
            "matches": [
                {
                    "company_data": company_data,
                    "similarity_pct": similarity_pct
                }
                for company_data, similarity_pct in results
            ]
        }), 200

    @app.route('/match_company')
    def companymatch():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://devvm01.nyc.ou.org:5655/match_company?company_id=1
        """
        # Initialize timers
        timers = {}
        global EXISTING_COMPANIES
        app_id = request.args.get('app_id', default=1, type=int)
        company = session.query(models.SubmissionApplication).filter_by(SubmissionAppId=app_id).first()
        if company is None:
            return jsonify({ "error": f"SubmissionApplication {app_id} not found" }), 404
            
        # Get the first address from the AddressList (it's a list, not a method)
          
        match = {
           'name': company.companyName,
           'street': company.companyAddress,
           'street1': company.companyAddress2,
           'city': company.companyCity,
           'state': company.companyState,
           'postal': company.ZipPostalCode,
           'country': company.companyCountry,
           'phone': company.companyPhone,
           "website": company.companyWebsite
        }
        '''
        match =  {
            'name': 'Seneca Foods Corporation',  # Missing Inc., uppercase
            'street': '350 Willow Brook Office Park',  # Abbreviated
            'city': 'Fairport',
            'state': 'NY',
            'postal': '14450',
            'phone': '315-781-8772'
        }
        '''
        # Time SQL execution
        sql_start = time.time()
        if EXISTING_COMPANIES is None:
            EXISTING_COMPANIES = load_existing_companies()
        sql_end = time.time()
        timers['sql_processing_ms'] = round((sql_end - sql_start) * 1000, 2)

        # Time match_company execution
        match_start = time.time()
        # Use configurable matcher from environment variables
        matcher_config = get_matcher_config()
        result = match_company(match, EXISTING_COMPANIES, matcher_config)
        match_end = time.time()
        timers['match_company_ms'] = round((match_end - match_start) * 1000, 2)
        
        # Calculate total time
        timers['total_ms'] = round(timers['sql_processing_ms'] + timers['match_company_ms'], 2)
        
        return jsonify({
            "result": result,
            "match_company": match,
            "meta": {
                "timings": timers,
                "record_count": len(EXISTING_COMPANIES)
            }
        }), 200

def load_existing_companies():
    results = session.execute(text(get_company_sql())).fetchall()
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
        data['name'] = data['c'][0]['name']
        #data['id'] = data['c'][0]['id']
        data['phone'] = data['c'][0]['cc'][0]['phone']
        data.pop('c', None)  # Remove the nested 'c' key after extracting the name   
        existing.append(data)
    return existing

def _match_company_async(match:dict)-> list:
    # This is a placeholder for an asynchronous version of match_company if needed in the future.
    # For now, it simply calls the synchronous version.

    results =find_matching(match, k=3, score_threshold=0.75)

    if results:
        print(f"Found {len(results)} matching companies:\n")
        for i, (company_data, similarity_pct) in enumerate(results, 1):
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
            print(f"   ID: {company_data.get('id', 'N/A')}")
            print(f"   Name: {company_data.get('name', 'Unknown')}")
            print(f"   Address: {company_data.get('street', '')}, {company_data.get('city', '')}, {company_data.get('state', '')} {company_data.get('postal', '')}")
            print(f"   Phone: {company_data.get('phone', 'N/A')}")
            print(f"   Website: {company_data.get('website', 'N/A')}")
            print()
    else:
        print("No matching companies found above 75% threshold.")
    
    return {
        "match_company": match,
        "matches": [
            {
                "company_data": company_data,
                "similarity_pct": similarity_pct
            }
            for company_data, similarity_pct in results
        ]
    }

def get_company_sql():
    # Use owns to limit it to existing companies with plants 
    return """
        SELECT 
            --TOP (1000) 
            -- [ID] as 'id'
            a.[COMPANY_ID] as 'id'
            , c.[NAME] as 'name'
            -- ,[ADDRESS_SEQ_NUM]
            --,[TYPE]
            --,[ATTN]
            ,[STREET1] as 'street'
            ,[STREET2] as 'street2'
            ,[STREET3] as 'street3'
            ,[CITY] as 'city'
            ,[STATE] as 'state'
            ,[ZIP] as 'postal'
            ,[COUNTRY] as 'country'
            ,[Voice] as 'phone'
            , null as 'website'
        FROM [ou_kash].[dbo].[COMPANY_ADDRESS] a
        JOIN [ou_kash].[dbo].[COMPANY_TB] c on c.COMPANY_ID = a.COMPANY_ID
        JOIN [ou_kash].[dbo].companycontacts cc ON c.company_id = cc.company_id
                                     AND cc.active = 1
                                     AND cc.PrimaryCT = 'Y'
        WHERE 
            --TYPE = 'Physical' and 
            c.COMPANY_ID in
            (select o.COMPANY_ID
            FROM [ou_kash].[dbo].[OWNS_TB] o
            JOIN [ou_kash].[dbo].COMPANY_TB c
            on c.COMPANY_ID = o.COMPANY_ID)
        FOR JSON AUTO

    """ 