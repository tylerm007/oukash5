from re import sub
import requests
import json

class JotFormAPI:
    def __init__(self, api_key, team_id):
        self.api_key = api_key
        self.base_url = "https://ou.jotform.com"
        self.headers = {
            'APIKEY': api_key,
            'Content-Type': 'application/json',
            'jf-team-id': team_id # '240425799590063'
        }
    
    def get_user_files(self, limit=20, offset=0):
        """Get all files uploaded by the user"""
        url = f"{self.base_url}/API/user/files"
        params = {
            'limit': limit,
            'offset': offset
        }
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            print("User Files" , response.json())
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def get_form_files(self, form_id):
        """Get all files from a specific form"""
        url = f"{self.base_url}/API/form/{form_id}/files"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print("Form Files" , response.json())
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def get_submission_files(self, submission_id):
        """Get files from a specific submission"""
        url = f"{self.base_url}/API/submission/{submission_id}/files"
        
        response = requests.get(url, headers=self.headers)
        
        if response.status_code == 200:
            print("Submission Files" , response.json())
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def get_submission(self, submission_id):
        """Get details of a specific submission, including form_id"""
        url = f"{self.base_url}/API/submission/{submission_id}?apiKey={self.api_key}"
        print("url:",url)
        
        # Include team-id header for team submissions
        headers = {
            'jf-team-id': '243646438272058'
        }
        
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def get_form_ids_for_submissions(self, submission_ids):
        """Get form_ids for a list of submission_ids"""
        form_ids = {}
        submission_set = set(submission_ids)
        
        # Get all forms first
        print("Fetching all forms...")
        forms_data = self.get_forms(limit=100)
        
        if not forms_data or 'content' not in forms_data:
            print("Could not fetch forms")
            return form_ids
        
        # For each form, get submissions and check if any match our submission_ids
        for form in forms_data['content']:
            form_id = form['id']
            print(f"Checking form {form_id} ({form.get('title', 'Untitled')})...")
            
            # Get submissions for this form
            submissions_data = self.get_submissions(form_id, limit=1000)
            
            if submissions_data and 'content' in submissions_data:
                for submission in submissions_data['content']:
                    sub_id = submission.get('id')
                    if sub_id in submission_set:
                        form_ids[sub_id] = form_id
                        print(f"  ✓ Found: Submission {sub_id} -> Form {form_id}")
                        
                        # Remove found submission from set to speed up search
                        submission_set.discard(sub_id)
                        
                        # If we found all submissions, we can stop
                        if not submission_set:
                            print("All submissions found!")
                            return form_ids
        
        # Mark any submissions we didn't find
        for sub_id in submission_set:
            form_ids[sub_id] = None
            print(f"  ✗ Not found: Submission {sub_id}")
        
        return form_ids
    
    def get_forms(self, limit=20):
        """Get list of forms (to find form IDs)"""
        url = f"{self.base_url}/API/user/forms"
        params = {'limit': limit}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def get_submissions(self, form_id, limit=20):
        """Get submissions for a form (to find submission IDs)"""
        url = f"{self.base_url}/API/form/{form_id}/submissions"
        params = {'limit': limit}
        
        response = requests.get(url, headers=self.headers, params=params)
        
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    
    def download_file(self, file_url, save_path):
        """Download a file from JotForm"""
        response = requests.get(file_url)
        
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            print(f"File downloaded: {save_path}")
            return True
        else:
            print(f"Failed to download file: {response.status_code}")
            return False

# Usage Example
if __name__ == "__main__":
    # Replace with your actual API key
    API_KEY = "6a43a5bd9eb0000522ee130271621f53"
    TEAM_ID = "243646438272058"
    jf = JotFormAPI(API_KEY, TEAM_ID)
    
       # Example 3: Get files from specific submission
    # You would need to know the submission ID
    submission_id = "251546753116861" #"243646438272058" # "243646438272058" #6449503610313204435"# "6381931699029307083"  # Replace with actual ID from Application
    submission_files = jf.get_submission_files(submission_id) or []

    for file in submission_files:
        print(f"  - {file}") 

    # Example 4: Get form_ids for a list of submission_ids
    print("\nGetting form_ids for submission_ids...")
    submission_ids = [
        "6460093567122060187",
        "6460079425427306594",

        # Add more submission IDs here
    ]
    form_ids_map = jf.get_form_ids_for_submissions(submission_ids)
    print(f"\nSubmission to Form mapping: {json.dumps(form_ids_map, indent=2)}")


    # Example 1: Get all user files
    print("Getting all user files...")
    user_files = jf.get_user_files(limit=50)
    
    if user_files:
        print(f"Found {len(user_files.get('content', []))} files")
        for file_info in user_files.get('content', []):
            print(f"File: {file_info.get('name', 'N/A')}")
            print(f"  URL: {file_info.get('url', 'N/A')}")
            print(f"  Size: {file_info.get('size', 'N/A')} bytes")
            print(f"  Type: {file_info.get('type', 'N/A')}")
            print(f"  Date: {file_info.get('date', 'N/A')}")
            print("---")
    
    # Example 2: Get forms first, then files from a specific form
    print("\nGetting forms...")
    forms = jf.get_forms()
    
    if forms and forms.get('content'):
        # Use the first form as example
        first_form = forms['content'][0]
        form_id = first_form['id']
        print(f"Getting files from form: {first_form.get('title', 'Untitled')} (ID: {form_id})")
        
        form_files = jf.get_form_files(form_id)
        if form_files:
            print(f"Found {len(form_files.get('content', []))} files in this form")
            for file_info in form_files.get('content', []):
                print(f"  - {file_info.get('name', 'N/A')}")
    
 
    
#curl -X POST -d "webhookURL=http://my.webhook.url/connect-to-DB.ext" -d "apiKey={myApiKey}" "https://api.jotform.com/v1/form/{myFormID}/webhooks"