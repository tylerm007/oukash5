"""
JotForm Submission Queries

This script retrieves form information and submissions from JotForm API.
Converts PowerShell script to Python.
"""

import os
import requests
from typing import Optional, List, Dict, Any


def get_jotform_data(api_key: str, team_id: str, form_id: str, base_url: str = "https://ou.jotform.com"):
    """
    Retrieve JotForm data including form info, properties, and submissions.
    
    Args:
        api_key: JotForm API key
        team_id: JotForm team ID
        form_id: JotForm form ID
        base_url: JotForm base URL
        
    Returns:
        Dictionary containing form info, properties, and submissions
    """
    # Match PowerShell headers exactly
    headers = {
        'jf-team-id': team_id,
        'apiKey': api_key
    }
    
    # Get form info - URL exactly as PowerShell does it
    form_url = f"{base_url}/API/form/{form_id}/submissions?limit=1000&apiKey={api_key}"
    print(f"Request URL: {form_url}")
    print(f"Headers: {headers}")
    form_response = requests.get(form_url, headers=headers)
    form_response.raise_for_status()
    form_data = form_response.json()
    print("Form Content:")
    print(form_data.get('content'))
    
    # Get form properties (including HTML)
    properties_url = f"{base_url}/API/form/{form_id}/properties?limit=1000&apiKey={api_key}"
    properties_response = requests.get(properties_url, headers=headers)
    properties_response.raise_for_status()
    properties_data = properties_response.json()
    
    # Get form submissions
    submissions_url = f"{base_url}/API/form/{form_id}/submissions?limit=1000&apiKey={api_key}"
    submissions_response = requests.get(submissions_url, headers=headers)
    submissions_response.raise_for_status()
    submissions_data = submissions_response.json()
    
    return {
        'form': form_data,
        'properties': properties_data,
        'submissions': submissions_data
    }


def parse_submission(submission: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Parse a JotForm submission and extract all relevant fields.
    
    Excludes control types: control_text, control_head, control_button, 
    control_widget, control_pagebreak, control_collapse
    
    Args:
        submission: JotForm submission dictionary
        
    Returns:
        List of parsed submission fields
    """
    # Types to exclude
    excluded_types = [
        'control_text', 'control_head', 'control_button', 
         'control_pagebreak', 'control_collapse'
    ]
    
    sub_list = []
    
    if 'answers' not in submission:
        return sub_list
    
    for answer_key, answer_data in submission['answers'].items():
        if not isinstance(answer_data, dict):
            continue
            
        answer_type = answer_data.get('type', '')
        
        # Skip excluded types
        if answer_type in excluded_types:
            continue
        
        # Handle full name separately (split into first and last)
        if answer_type == 'control_fullname':
            answer_obj = answer_data.get('answer', {})
            if isinstance(answer_obj, dict):
                sub_list.append({
                    'order': int(answer_data.get('order', 0)),
                    'name': 'contactFirst',
                    'type': answer_type,
                    'answer': answer_obj.get('first', ''),
                    'text': answer_data.get('text')
                })
                sub_list.append({
                    'order': int(answer_data.get('order', 0)),
                    'name': 'contactLast',
                    'type': answer_type,
                    'answer': answer_obj.get('last', ''),
                    'text': answer_data.get('text')
                })
        else:
            sub_list.append({
                'order': int(answer_data.get('order', 0)),
                'name': answer_data.get('name', ''),
                'type': answer_type,
                'answer': answer_data.get('answer', ''),
                'text': answer_data.get('text')
            })
    
    # Sort by order
    sub_list.sort(key=lambda x: x['order'])
    
    return sub_list


def print_submission_table(sub_list: List[Dict[str, Any]]):
    """
    Print submission data in a formatted table.
    
    Args:
        sub_list: List of parsed submission fields
    """
    if not sub_list:
        print("No submissions to display")
        return
    
    # Calculate column widths
    name_width = max(len(item['name']) for item in sub_list) if sub_list else 10
    text_width = min(max(len(item['text']) for item in sub_list) if sub_list else 20, 50)
    answer_width = min(max(len(str(item['answer'])) for item in sub_list) if sub_list else 20, 50)
    
    # Ensure minimum widths
    name_width = max(name_width, 10)
    text_width = max(text_width, 20)
    answer_width = max(answer_width, 20)
    
    # Print header
    header = f"{'Name'} | {'Text'} | {'Answer'}"
    print(header)
    print("-" * len(header))
    
    result = []
    #print(sub_list[0]) type. order
    # Print rows
    for item in sub_list:
        name = item['name']
        text = str(item['text'])
        answer = str(item['answer'])
        # print(f"{name} | {text} | {answer}")
        if answer.strip() != "":
            result.append({ text:{'name': name, 'answer': answer}})
    return result

def main():
    """Main execution function."""
    # Get API key from environment variable
    api_key = os.environ.get('JotFormAPIKey') or "6a43a5bd9eb0000522ee130271621f53"
    
    if not api_key:
        print("Error: JotFormAPIKey environment variable not set")
        return
    
    # JotForm configuration
    base_url = "https://ou.jotform.com"
    team_id = "240425799590063"
    
    # Form IDs
    form_id_prod = "260253336843860" #"243646438272058"  # PROD Kashrus Application form
    form_id_test = "253065393574867"  # TEST application form
    
    # Use PROD form
    form_id = form_id_prod          
    
    try:
        # Get JotForm data
        print("Fetching JotForm data...")
        data = get_jotform_data(api_key, team_id, form_id, base_url)
        
        # Get first submission
        submissions = data['submissions'].get('content', [])
        
        if not submissions:
            print("No submissions found")
            return
        
        print(f"\nFound {len(submissions)} submission(s)")
        print("\nProcessing first submission...")
        
        submission = submissions[0]
        sub_list = parse_submission(submission)
        
        print(f"\nSubmission ID: {submission.get('id', 'N/A')}")
        print(f"Submission Date: {submission.get('created_at', 'N/A')}")
        print(f"\nParsed Fields ({len(sub_list)}):\n")
        
        result = print_submission_table(sub_list)
        for r in result:
            print(r)
        
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from JotForm API: {e}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
