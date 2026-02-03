"""
Convert JotFormMapping.csv to JSON format using row 1 as header names
"""
import csv
import json

# Read CSV and convert to JSON
csv_file = 'JotFormMapping.csv'
json_file = 'JotFormMapping.json'

data = []

with open(csv_file, 'r', encoding='utf-8') as f:
    csv_reader = csv.DictReader(f)
    for row in csv_reader:
        data.append(row)

# Write to JSON file
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"✓ Converted {len(data)} rows from {csv_file} to {json_file}")

# Also create a structured mapping by prompt
mapping_by_prompt = {}
for row in data:
    prompt = row.get('prompt', '')
    if prompt:
        jot_field = row.get('jot_field', '')
        target = row.get('target', '')
        field_name = row.get('field_name', '')
        
        if prompt not in mapping_by_prompt:
            mapping_by_prompt[prompt] = []
        
        mapping_by_prompt[prompt].append({
            'jot_field': jot_field,
            'target': target,
            'field_name': field_name,
            'order': row.get('order', ''),
            'plant_number': row.get('plant_num', '')
        })

# Write structured mapping
with open('JotFormMapping_structured.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_by_prompt, f, indent=2, ensure_ascii=False)

print(f"✓ Created structured mapping with {len(mapping_by_prompt)} unique prompts")

# Create mapping by target entity
mapping_by_target = {
    'main': [],
    'contact': [],
    'plant': [],
    'plantContact': [],
    'product': [],
    'ingredient': [],
    'file': []
}

for row in data:
    target = row.get('target', '')
    if target in mapping_by_target:
        mapping_by_target[target].append({
            'prompt': row.get('prompt', ''),
            'jot_field': row.get('jot_field', ''),
            'field_name': row.get('field_name', ''),
            'order': row.get('order', ''),
            'plant_number': row.get('plant_num', '')
        })

with open('JotFormMapping_by_target.json', 'w', encoding='utf-8') as f:
    json.dump(mapping_by_target, f, indent=2, ensure_ascii=False)

print(f"✓ Created target-based mapping")
print("\nSummary by target:")
for target, items in mapping_by_target.items():
    if items:
        print(f"  {target}: {len(items)} fields")
