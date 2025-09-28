from flask import request, jsonify
import logging

app_logger = logging.getLogger("api_logic_server_app")

def add_service(app, api, project_dir, swagger_host: str, PORT: str, method_decorators ):
    pass

    @app.route('/hello_newer_service')
    def hello_newer_service():
        """        
        Illustrates:
        * Use standard Flask, here for non-database endpoints.

        Test it with:
        
                http://localhost:5656/hello_newer_service?user=ApiLogicServer
        """
        user = request.args.get('user')
        app_logger.info(f'{user}')
        return jsonify({"result": f'hello from even_newer_service! from {user}'})
    
    
    @app.route('/test_parser', methods=['GET'])
    def test_parser():
        '''
         Invoke-RestMethod -Uri "http://localhost:5656/test_parser" -Method GET -ContentType "application/json"
        '''
        import requests
        PORT = 5656
        endpoint = "COMPANYTB"
        filter1 = '[{"name":"ACTIVE","op":"eq","val":1},{"name":"RC","op":"ilike","val":"%Gorelik%"},{"name":"CATEGORY","op":"ilike","val":"%Nut%"},{"name":"NAME","op":"ilike","val":"%Company%"}]'
        response1 = requests.get(f'http://localhost:{PORT}/api/{endpoint}?filter={filter1}')
        
        endpoint = "LabelTb"
        filter2 = '[{"name":"ACTIVE","op":"eq","val":1},{"name":"LABEL_SEQ_NUM","op":"gt","val":1}]'
        response2 = requests.get(f'http://localhost:{PORT}/api/{endpoint}?filter={filter2}')
        
        endpoint = "COMPANYTB"
        filter3 = '[{"name":"ACTIVE","op":"eq","val":1},{"name":"RC","op":"ilike","val":"%Gorelik%"},{"name":"STATUS","op":"eq","val":"Certified"}]'
        response3 = requests.get(f'http://localhost:{PORT}/api/{endpoint}?filter={filter3}')
        return jsonify({"result": f'hello test_parser! {response1.json()} {response2.json()} {response3.json()}'})

