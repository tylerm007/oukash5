# Vector Store Stetup and Match
'''
from langchain_community.vectorstores import PGVector
from langchain_community.embeddings import HuggingFaceEmbeddings
-- Or for OpenAI:
-- from langchain_openai import OpenAIEmbeddings

--Initialize embeddings
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
--Or: embeddings = OpenAIEmbeddings()

CONNECTION_STRING = "postgresql+psycopg2://user:password@localhost:5432/your_db"
COLLECTION_NAME = "companies"


def match_to_text(match: dict) -> str:
    
   -- Convert company match dict to text for embedding
    parts = [
        match.get('name', ''),
        match.get('street', ''),
        match.get('city', ''),
        match.get('state', ''),
        match.get('postal', ''),
        match.get('phone', ''), 
        match.get('website', '')
    ]
    return ' '.join(p for p in parts if p)
'''

## Initialize Vector Store

'''
-- In your PostgreSQL database, run this once:
CREATE EXTENSION IF NOT EXISTS vector;

vectorstore = PGVector(
connection_string=CONNECTION_STRING,
embedding_function=embeddings,
collection_name=COLLECTION_NAME,
)
'''

## Add Companies to Vector Store
'''
from langchain.docstore.document import Document

def add_company_to_vectorstore(company_data: dict):
    --Add a company record to the vector store
    text = match_to_text(company_data)
    
    # Store original data as metadata for retrieval
    doc = Document(
        page_content=text,
        metadata=company_data
    )
    
    vectorstore.add_documents([doc])

# Example: Add companies
'''
companies = [
    {'name': 'Acme Corp', 'street': '123 Main St', 'city': 'Denver', 'state': 'CO', 'postal': '80202', 'phone': '303-555-1234', 'website': 'acme.com'},
    {'name': 'TechStart Inc', 'street': '456 Tech Blvd', 'city': 'Austin', 'state': 'TX', 'postal': '78701', 'phone': '512-555-5678', 'website': 'techstart.io'},
]
''''
## SQL = 'Select * from V_Companies_For_Vector'
'''
for company in companies:
    add_company_to_vectorstore(company)
'''

## Search Matching
'''
def find_matching_companies(match: dict, k: int = 5, score_threshold: float = None):
    """
    Find companies matching the given criteria
    
    Args:
        match: Dict with company fields to match
        k: Number of results to return
        score_threshold: Optional minimum similarity score (0-1, higher is better)
    """
    search_text = match_to_text(match)
    
    if score_threshold:
        -- Only return results above threshold
        results = vectorstore.similarity_search_with_relevance_scores(
            search_text, 
            k=k,
            score_threshold=score_threshold
        )
        return [(doc.metadata, score) for doc, score in results]
    else:
        --Return top k with scores
        results = vectorstore.similarity_search_with_score(search_text, k=k)
        return [(doc.metadata, score) for doc, score in results]


# Example usage
'''
match = {
    'name': 'Acme Corporation',
    'street': '123 Main Street',
    'city': 'Denver',
    'state': 'CO',
    'postal': '80202',
    'phone': '303-555-1234',
    'website': 'www.acme.com'
}

results = find_matching_companies(match, k=3)

for company_data, score in results:
    print(f"Score: {score:.4f}")
    print(f"  Company: {company_data}")
'''

## Integration with ApiLogicServer
'''
from flask import request

@app.route('/api/company/match', methods=['POST'])
def match_company():
    match_data = request.json
    
    results = find_matching_companies(
        match=match_data,
        k=5,
        score_threshold=0.7  # Adjust based on your needs
    )
    
    return {
        'matches': [
            {'company': data, 'similarity_score': float(score)}
            for data, score in results
        ]
    }
'''

## Notes:

* Lower scores = better match with similarity_search_with_score (distance)
* Higher scores = better match with similarity_search_with_relevance_scores (similarity)
You may need to tune the score_threshold based on your data