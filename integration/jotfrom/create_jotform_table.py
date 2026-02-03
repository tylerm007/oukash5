"""
Extract JotForm field names and create database table definition
"""
import json

# Read the JotForm data
with open('jotform.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Extract unique field names
field_names = set()
for item in data:
    for question, field_data in item.items():
        if isinstance(field_data, dict) and 'name' in field_data:
            field_names.add(field_data['name'])

# Sort for consistent output
sorted_fields = sorted(field_names)

print("="*70)
print(f"Found {len(sorted_fields)} unique field names")
print("="*70)
print("\nField Names:")
for field in sorted_fields:
    print(f"  - {field}")

# Generate SQL CREATE TABLE statement
print("\n" + "="*70)
print("SQL CREATE TABLE Statement")
print("="*70 + "\n")

sql = """CREATE TABLE JotFormData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    submission_id VARCHAR(50),
    submission_date DATETIME,
"""

# Add all fields as VARCHAR(250)
for field in sorted_fields:
    sql += f"    {field} VARCHAR(250),\n"

# Remove last comma and close
sql = sql.rstrip(',\n') + "\n);"

print(sql)

# Also generate SQLAlchemy model
print("\n" + "="*70)
print("SQLAlchemy Model")
print("="*70 + "\n")

model = """from sqlalchemy import Column, Integer, String, DateTime
from database.models import Base

class JotFormData(Base):
    __tablename__ = 'jot_form_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    submission_id = Column(String(50))
    submission_date = Column(DateTime)
"""

for field in sorted_fields:
    model += f"    {field} = Column(String(250))\n"

print(model)

# Save to file
with open('jotform_table_schema.sql', 'w', encoding='utf-8') as f:
    f.write(sql)
    
with open('jotform_model.py', 'w', encoding='utf-8') as f:
    f.write(model)

print("\n" + "="*70)
print("Files created:")
print("  - jotform_table_schema.sql (SQL CREATE TABLE)")
print("  - jotform_model.py (SQLAlchemy model)")
print("="*70)
