#!/usr/bin/env python3
"""
API Endpoint Testing Script
Automatically discovers and tests all API endpoints from the database models.
This only works for GenAI Logic running without security (no Authorization header).
"""

import requests
import json
import time
from typing import List, Dict, Any
import logging
import inspect
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Base API URL
BASE_URL = "http://localhost:5656/api" 
#BASE_URL = "http://172.30.3.133:5656/api"

# List of all API endpoints (collection names from models.py)
import importlib.util

def get_api_endpoints_from_models():
    """
    Dynamically discover API endpoints from models.py class definitions
    """
    # Adjust the path to your models.py file
    models_path = os.path.join(os.path.dirname(__file__),'..','database', 'models.py')
    
    # Add the parent directory to sys.path so relative imports work
    import sys
    parent_dir = os.path.join(os.path.dirname(__file__), '..')
    parent_dir = os.path.abspath(parent_dir)
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

    spec = importlib.util.spec_from_file_location("models", models_path)
    models = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(models)
    
    endpoints = []
    for name, obj in inspect.getmembers(models):
        if inspect.isclass(obj) and hasattr(obj, '__tablename__'):
            # Use class name as endpoint (or __tablename__ if preferred)
            endpoints.append(name)
    
    return sorted(endpoints)

# Replace the hardcoded list with dynamic discovery
API_ENDPOINTS = get_api_endpoints_from_models()

class APITester:
    """Class to test API endpoints"""
    
    def __init__(self, base_url: str = BASE_URL, timeout: int = 10):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.results = {}
        
    def test_endpoint(self, endpoint: str) -> Dict[str, Any]:
        """
        Test a single API endpoint
        
        Args:
            endpoint: The endpoint name to test
            
        Returns:
            Dictionary with test results
        """
        url = f"{self.base_url}/{endpoint}?page[limit]=10"
        result = {
            "endpoint": endpoint,
            "url": url,
            "status_code": None,
            "success": False,
            "response_time": None,
            "record_count": 0,
            "error": None,
            "response_size": 0
        }
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout)
            end_time = time.time()
            
            result["status_code"] = response.status_code
            result["response_time"] = round((end_time - start_time) * 1000, 2)  # ms
            result["response_size"] = len(response.content)
            
            if response.status_code == 200:
                result["success"] = True
                try:
                    json_data = response.json()
                    if isinstance(json_data, dict) and 'data' in json_data:
                        result["record_count"] = len(json_data['data'])
                    elif isinstance(json_data, list):
                        result["record_count"] = len(json_data)
                except json.JSONDecodeError:
                    result["error"] = "Invalid JSON response"
            else:
                result["error"] = f"HTTP {response.status_code}: {response.text[:200]}"
                
        except requests.exceptions.Timeout:
            result["error"] = "Request timeout"
        except requests.exceptions.ConnectionError:
            result["error"] = "Connection error"
        except requests.exceptions.RequestException as e:
            result["error"] = f"Request error: {str(e)}"
        except Exception as e:
            result["error"] = f"Unexpected error: {str(e)}"
            
        return result
    
    def test_all_endpoints(self, endpoints: List[str] = None) -> Dict[str, Any]:
        """
        Test all API endpoints
        
        Args:
            endpoints: List of endpoints to test (defaults to API_ENDPOINTS)
            
        Returns:
            Dictionary with summary and detailed results
        """
        if endpoints is None:
            endpoints = API_ENDPOINTS
            
        logger.info(f"Testing {len(endpoints)} API endpoints...")
        
        results = []
        successful = 0
        failed = 0
        total_time = 0
        
        for i, endpoint in enumerate(endpoints, 1):
            logger.info(f"Testing {i}/{len(endpoints)}: {endpoint}")
            
            result = self.test_endpoint(endpoint)
            results.append(result)
            
            if result["success"]:
                successful += 1
                logger.info(f"✅ {endpoint}: {result['record_count']} records ({result['response_time']}ms)")
            else:
                failed += 1
                logger.error(f"❌ {endpoint}: {result['error']}")
                
            if result["response_time"]:
                total_time += result["response_time"]
                
            # Small delay to avoid overwhelming the server
            time.sleep(0.1)
        
        summary = {
            "total_endpoints": len(endpoints),
            "successful": successful,
            "failed": failed,
            "success_rate": round((successful / len(endpoints)) * 100, 2),
            "total_response_time": round(total_time, 2),
            "average_response_time": round(total_time / len(endpoints), 2) if endpoints else 0
        }
        
        self.results = {
            "summary": summary,
            "results": results
        }
        
        return self.results
    
    def print_summary(self):
        """Print a summary of test results"""
        if not self.results:
            logger.warning("No test results available")
            return
            
        summary = self.results["summary"]
        
        print("\n" + "="*60)
        print("API ENDPOINT TEST SUMMARY")
        print("="*60)
        print(f"Total Endpoints Tested: {summary['total_endpoints']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']}%")
        print(f"Total Response Time: {summary['total_response_time']}ms")
        print(f"Average Response Time: {summary['average_response_time']}ms")
        print("="*60)
        
    def print_detailed_results(self, show_successful: bool = True, show_failed: bool = True):
        """Print detailed test results"""
        if not self.results:
            logger.warning("No test results available")
            return
            
        results = self.results["results"]
        
        if show_successful:
            print("\n✅ SUCCESSFUL ENDPOINTS:")
            print("-" * 40)
            for result in results:
                if result["success"]:
                    print(f"{result['endpoint']:<30} | {result['record_count']:>6} records | {result['response_time']:>6}ms")
        
        if show_failed:
            print("\n❌ FAILED ENDPOINTS:")
            print("-" * 40)
            for result in results:
                if not result["success"]:
                    print(f"{result['endpoint']:<30} | {result['error']}")
    
    def save_results_to_file(self, filename: str = "api_test_results.json"):
        """Save test results to a JSON file"""
        if not self.results:
            logger.warning("No test results to save")
            return
            
        try:
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
            logger.info(f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {e}")
    
    def test_specific_endpoint_with_id(self, endpoint: str, record_id: Any) -> Dict[str, Any]:
        """
        Test a specific endpoint with a record ID
        
        Args:
            endpoint: The endpoint name
            record_id: The ID of a specific record
            
        Returns:
            Dictionary with test results
        """
        url = f"{self.base_url}/{endpoint}/{record_id}"
        result = {
            "endpoint": f"{endpoint}/{record_id}",
            "url": url,
            "status_code": None,
            "success": False,
            "response_time": None,
            "error": None
        }
        
        try:
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout)
            end_time = time.time()
            
            result["status_code"] = response.status_code
            result["response_time"] = round((end_time - start_time) * 1000, 2)
            
            if response.status_code == 200:
                result["success"] = True
                logger.info(f"✅ {endpoint}/{record_id}: Success ({result['response_time']}ms)")
            else:
                result["error"] = f"HTTP {response.status_code}: {response.text[:200]}"
                logger.error(f"❌ {endpoint}/{record_id}: {result['error']}")
                
        except Exception as e:
            result["error"] = f"Error: {str(e)}"
            logger.error(f"❌ {endpoint}/{record_id}: {result['error']}")
            
        return result


def main():
    """Main function to run API tests"""
    print("🚀 Starting API Endpoint Testing...")
    #from config,Config import Args as args
    okta_auth_config = "http://localhost:5656/auth/login" #f'{args.http_scheme}://{args.swagger_host}:{args.swagger_port}/auth/login'
    # Create tester instance
    tester = APITester()
    
    # Test all endpoints
    results = tester.test_all_endpoints()
    
    # Print results
    tester.print_summary()
    tester.print_detailed_results()
    
    # Save results to file
    tester.save_results_to_file()
    
    # Example: Test specific records if needed
    print("\n🔍 Testing specific records...")
    if results["summary"]["successful"] > 0:
        # Test first successful endpoint with ID 1
        successful_endpoints = [r for r in results["results"] if r["success"]]
        if successful_endpoints:
            endpoint = successful_endpoints[0]["endpoint"]
            tester.test_specific_endpoint_with_id(endpoint, 1)


if __name__ == "__main__":
    main()