
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.pgvector import PGVector
# Or for OpenAI:
# from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
import threading


# Use standard PostgreSQL connection (not async)
CONNECTION_STRING = "postgresql+psycopg2://postgres:GENAILOGIC2026@devlinux01.nyc.ou.org:5432/rag_ou_kash"
COMPANY_COLLECTION_NAME = "companies"
PLANT_COLLECTION_NAME = "plants"
INGREDIENTS_COLLECTION_NAME = 'ingredients'
PRODUCT_COLLECTION_NAME = 'products'

# Lazy initialization - embeddings and vectorstore created on first use
_embeddings = None
_company_vectorstore = None
_plant_vectorstore = None
_embeddings_loading = False
_embeddings_lock = threading.Lock()

def preload_embeddings_async():
    """
    Pre-load embeddings model in background thread during server startup.
    Call this from server_setup.py or api_logic_server_run.py
    """
    def _load():
        print("⏳ Pre-loading embedding model in background...")
        get_embeddings()
        print("✓ Embedding model ready")
    
    thread = threading.Thread(target=_load, daemon=True)
    thread.start()
    return thread

def get_embeddings():
    """Get or create embeddings instance (lazy loading with thread safety)."""
    global _embeddings, _embeddings_loading
    
    # Thread-safe initialization
    with _embeddings_lock:
        if _embeddings is None and not _embeddings_loading:
            _embeddings_loading = True
            print("⏳ Loading embedding model (all-MiniLM-L6-v2)...")
            # Optimize loading with model kwargs for faster initialization
            _embeddings = HuggingFaceEmbeddings(
                model_name="all-MiniLM-L6-v2",
                model_kwargs={'device': 'cpu'},  # Explicit CPU (GPU would be 'cuda')
                encode_kwargs={'normalize_embeddings': True, 'batch_size': 32},
                cache_folder=".././.embedding_cache"  # Local cache instead of ~/.cache
            )
            print("✓ Embedding model loaded\n")
            _embeddings_loading = False
        elif _embeddings_loading:
            # Wait for other thread to finish loading
            print("⏳ Waiting for embedding model to finish loading...")
    
    return _embeddings

def get_company_vectorstore():
    """Get or create vectorstore instance (lazy loading)."""
    global _company_vectorstore
    if _company_vectorstore is None:
        _company_vectorstore = PGVector(
            connection_string=CONNECTION_STRING,
            embedding_function=get_embeddings(),
            collection_name=COMPANY_COLLECTION_NAME,
            use_jsonb=True
        )
    return _company_vectorstore

def get_plant_vectorstore():
    """Get or create vectorstore instance (lazy loading)."""
    global _plant_vectorstore
    if _plant_vectorstore is None:
        _plant_vectorstore = PGVector(
            connection_string=CONNECTION_STRING,
            embedding_function=get_embeddings(),
            collection_name=PLANT_COLLECTION_NAME,
            use_jsonb=True
        )
    return _plant_vectorstore

def match_company_to_text(match: dict) -> str:
    """
    Convert company match dict to text for embedding.
    Filters out None values and NUL characters.
    """
    # Get values and convert to strings, filtering None
    phone = match.get('phone', '') or ''
    phone = phone.replace('\x00', '').strip()
    phone = phone.replace('\u0000', '').strip()
    phone = phone.replace('-', '').strip()
    phone = phone.replace('(', '').strip()
    phone = phone.replace(')', '').strip()
    phone = phone.replace('+', '').strip()
    parts = [
        #str(match.get('id', '') or ''),
        str(match.get('name', '') or ''),
        str(match.get('street', '') or ''),
        str(match.get('street2', '') or ''),
        str(match.get('street3', '') or ''),
        str(match.get('city', '') or ''),
        str(match.get('state', '') or ''),
        str(match.get('postal', '') or ''),
        str(match.get('country', '') or ''),
        str(phone), 
        str(match.get('website', '') or '')
    ]
    
    # Filter out empty strings and remove NUL characters
    cleaned_parts = []
    for p in parts:
        # Remove NUL characters (0x00) and other control characters
        cleaned = p.replace('\x00', '').strip()
        cleaned = cleaned.replace('\u0000', '').strip()
        cleaned_parts.append(cleaned)
    
    return ' '.join(cleaned_parts)

def clean_metadata(data: dict) -> dict:
    """
    Clean metadata dictionary by removing NUL characters from all string values.
    """
    cleaned = {}
    for key, value in data.items():
        if value is None:
            cleaned[key] = None
        elif isinstance(value, str):
            # Remove NUL characters and other problematic Unicode escapes
            cleaned[key] = value.replace('\x00', '').replace('\u0000', '').strip()
        else:
            cleaned[key] = value
    return cleaned

def add_company_to_vectorstore(company_data: dict):
    # Add a company record to the vector store
    text = match_company_to_text(company_data)
    
    # Clean metadata to remove NUL characters
    clean_data = clean_metadata(company_data)
    
    # Store cleaned data as metadata for retrieval
    doc = Document(
        page_content=text,
        metadata=clean_data
    )
    
    get_company_vectorstore().add_documents([doc])


def add_plant_to_vectorstore(plant_data: dict):
    # Add a company record to the vector store
    text = match_company_to_text(plant_data)
    
    # Clean metadata to remove NUL characters
    clean_data = clean_metadata(plant_data)
    
    # Store cleaned data as metadata for retrieval
    doc = Document(
        page_content=text,
        metadata=clean_data
    )
    
    get_plant_vectorstore().add_documents([doc])


## Search Matching
def find_matching(match: dict, k: int = 5, score_threshold: float = 0.85, use_company_vectorstore: bool = True) -> list:
    """
    Find companies matching the given criteria using semantic similarity.
    
    Args:
        match: Dict with company fields to match
        k: Number of results to return (default: 5)
        score_threshold: Minimum similarity score 0-1, where 1.0 is perfect match (default: 0.85)
                        Set to None to return all top k results regardless of score
    
    Returns:
        List of tuples: (company_metadata_dict, similarity_percentage)
        Similarity percentage: 0-100%, where 100% is perfect match
    
    Scoring explanation:
        - Uses cosine similarity converted to percentage (0-100%)
        - 95-100%: Excellent match (likely same company)
        - 85-95%: Good match (similar company or minor differences)
        - 70-85%: Moderate match (some similarities)
        - <70%: Weak match (different companies)
    """
    search_text = match_company_to_text(match)

    # Always use relevance scores (0-1 scale, higher is better)
    if use_company_vectorstore:
        vectorstore = get_company_vectorstore()
    else:
        vectorstore = get_plant_vectorstore()
    
    if score_threshold:
        # Only return results above threshold
        results = vectorstore.similarity_search_with_relevance_scores(
            query=search_text,
            k=k,
            score_threshold=score_threshold
        )
    else:
        # Return top k results, convert distance to relevance
        results = vectorstore.similarity_search_with_score(search_text, k=k)
        # Convert L2 distance to relevance score (0-1)
        results = [(doc, 1 - min(distance / 4, 1.0)) for doc, distance in results]
    
    # Convert to percentage and return
    return [(doc.metadata, round(score * 100, 2)) for doc, score in results]

# Example usage
def main():
    """Example demonstrating vector store company matching with percentage scores."""
    print("\n" + "="*70)
    print("Vector Store Company Matching Demo")
    print("="*70 + "\n")
    
    # Example: Add a company
    print("Adding test company to vector store...")
    match = {
        "id": "ID_001",
        'name': 'Acme Corporation',
        'street': '123 Main Street',
        'city': 'Denver',
        'state': 'CO',
        'postal': '80202',
        'phone': '303-555-1234',
        'website': 'www.acme.com'
    }
    add_company_to_vectorstore(match)
    print("✓ Added: Acme Corporation\n")
    
    # Example: Search for matches
    print("-"*70)
    print("Searching for similar companies (85% threshold)...")
    print("-"*70 + "\n")
    
    results = find_matching(match, k=3, score_threshold=0.85)

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
        print("No matching companies found above 85% threshold.")

if __name__ == "__main__":
    main()