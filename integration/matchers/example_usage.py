"""
Company Matcher - Example Usage and Tests
==========================================

Demonstrates how to use the matching system with sample data.
"""

from matcher import (
    CompanyMatcher, 
    MatchConfig, 
    MatchTier,
    match_company
)
from llm_verifier import LLMVerifier, BatchLLMVerifier

# =============================================================================
# SAMPLE DATA
# =============================================================================

EXISTING_COMPANIES = [
    {
        'id': 1,
        'name': 'Acme Foods Inc.',
        'street': '123 Main Street',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60601',
        'phone': '312-555-1234',
        'website': 'www.acmefoods.com'
    },
    {
        'id': 2,
        'name': 'Best Baking Company LLC',
        'street': '456 Oak Avenue, Suite 200',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60602',
        'phone': '312-555-5678',
        'website': 'bestbaking.com'
    },
    {
        'id': 3,
        'name': 'Chicago Kosher Foods',
        'street': '789 Devon Avenue',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60659',
        'phone': '773-555-9999',
        'website': 'chicagokosher.com'
    },
    {
        'id': 4,
        'name': 'Global Food Manufacturing International',
        'street': '100 Industrial Parkway',
        'city': 'Newark',
        'state': 'NJ',
        'postal': '07102',
        'phone': '973-555-1111',
        'website': 'globalfoodmfg.com'
    },
    {
        'id': 5,
        'name': "O'Brien's Dairy Products",
        'street': '222 Milk Street',
        'city': 'Boston',
        'state': 'MA',
        'postal': '02101',
        'phone': '617-555-2222',
        'website': 'obriensdairy.com'
    },
    {
        'id': 6,
        'name': 'Sunrise Bakery & Cafe',
        'street': '333 Morning Drive',
        'city': 'Los Angeles',
        'state': 'CA',
        'postal': '90001',
        'phone': '213-555-3333',
        'website': 'sunrisebakery.la'
    },
    {
        'id': 7,
        'name': 'Atlantic Seafood Processors Inc',
        'street': '444 Harbor Road',
        'city': 'Portland',
        'state': 'ME',
        'postal': '04101',
        'phone': '207-555-4444',
        'website': 'atlanticseafood.com'
    },
    {
        'id': 8,
        'name': 'Mountain Valley Snacks',
        'street': '555 Ridge Lane',
        'city': 'Denver',
        'state': 'CO',
        'postal': '80201',
        'phone': '303-555-5555',
        'website': 'mvsnacks.com'
    },
]

def get_sql():
    return """
        SELECT TOP (1000) [ID] as 'id'
            ,a.[COMPANY_ID]
            , c.[NAME] as 'name'
            ,[ADDRESS_SEQ_NUM]
            ,[TYPE]
            ,[ATTN]
            ,[STREET1] as 'street'
            ,[STREET2] as 'street2'
            ,[STREET3] as 'street3'
            ,[CITY] as 'city'
            ,[STATE] as 'state'
            ,[ZIP] as 'postal'
            , null as 'website'
            --, cp.[PHONE]
        FROM [ou_kash].[dbo].[COMPANY_ADDRESS] a
        JOIN [ou_kash].[dbo].[COMPANY_TB] c on c.COMPANY_ID = a.COMPANY_ID
        WHERE TYPE = 'Physical' and c.COMPANY_ID in
            (select o.COMPANY_ID
            FROM [ou_kash].[dbo].[OWNS_TB] o
            JOIN [ou_kash].[dbo].COMPANY_TB c
            on c.COMPANY_ID = o.COMPANY_ID)

    """

# =============================================================================
# TEST CASES
# =============================================================================

TEST_CASES = [
    # Test 1: Exact name match with formatting differences
    {
        'name': 'ACME FOODS',  # Missing Inc., uppercase
        'street': '123 Main St',  # Abbreviated
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60601',
        'phone': '(312) 555-1234',  # Different format
        'expected_match_id': 1,
        'expected_tier': MatchTier.HIGH,
        'description': 'Same company, different formatting'
    },
    
    # Test 2: Name variation with typo
    {
        'name': 'Acme Food Inc',  # Missing 's' in Foods
        'street': '123 Main Street',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60601',
        'expected_match_id': 1,
        'expected_tier': MatchTier.HIGH,
        'description': 'Minor typo in name'
    },
    
    # Test 3: Same address, different company name
    {
        'name': 'Midwest Distribution Corp',  # Different company
        'street': '123 Main Street',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60601',
        'expected_match_id': 1,  # Same address
        'expected_tier': MatchTier.MEDIUM,  # Should flag for review
        'description': 'Different name at same address'
    },
    
    # Test 4: Abbreviations and word order
    {
        'name': 'Global Food Mfg Intl',  # Abbreviated
        'street': '100 Industrial Pkwy',
        'city': 'Newark',
        'state': 'NJ',
        'postal': '07102',
        'expected_match_id': 4,
        'expected_tier': MatchTier.HIGH,
        'description': 'Abbreviated company name'
    },
    
    # Test 5: Completely new company
    {
        'name': 'Totally New Foods LLC',
        'street': '999 Innovation Blvd',
        'city': 'San Francisco',
        'state': 'CA',
        'postal': '94102',
        'expected_match_id': None,
        'expected_tier': MatchTier.NO_MATCH,
        'description': 'No matching company'
    },
    
    # Test 6: DBA / Trade name variation
    {
        'name': "O'Briens Dairy",  # Slight variation, missing Products
        'street': '222 Milk St',
        'city': 'Boston',
        'state': 'MA',
        'postal': '02101',
        'phone': '617-555-2222',
        'expected_match_id': 5,
        'expected_tier': MatchTier.HIGH,
        'description': 'DBA/trade name variation'
    },
    
    # Test 7: Similar name, different location
    {
        'name': 'Sunrise Bakery',
        'street': '100 Different Street',
        'city': 'San Diego',  # Different city
        'state': 'CA',
        'postal': '92101',  # Different postal
        'expected_match_id': 6,  # Name matches but location doesn't
        'expected_tier': MatchTier.LOW,  # Should be low confidence
        'description': 'Similar name, different location'
    },
    
    # Test 8: Postal code zone match only
    {
        'name': 'Chicago Foods Distribution',
        'street': '888 Devon Ave',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60650',  # Same zone (606xx) as Chicago Kosher Foods
        'expected_match_id': 3,
        'expected_tier': MatchTier.LOW,
        'description': 'Name similarity with postal zone match'
    },
]


# =============================================================================
# BASIC USAGE EXAMPLE
# =============================================================================

def basic_example():
    """Basic usage example"""
    print("=" * 70)
    print("BASIC USAGE EXAMPLE")
    print("=" * 70)
    
    # Create matcher and index existing companies
    matcher = CompanyMatcher()
    matcher.index_companies(EXISTING_COMPANIES)
    
    # Match an incoming company
    incoming = {
        'name': 'ACME FOODS',
        'street': '123 Main St',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60601',
        'phone': '(312) 555-1234'
    }
    
    print(f"\nSearching for: {incoming['name']}")
    print(f"Address: {incoming['street']}, {incoming['city']}, {incoming['state']} {incoming['postal']}")
    print("-" * 50)
    
    matches = matcher.find_matches(incoming)
    
    if matches:
        for i, match in enumerate(matches, 1):
            print(f"\nMatch #{i}:")
            print(f"  Company: {match.existing_name} (ID: {match.existing_id})")
            print(f"  Confidence: {match.confidence:.1f}%")
            print(f"  Tier: {match.match_tier.value}")
            print(f"  Signals:")
            print(f"    - Name similarity: {match.signals.name_similarity:.1f}%")
            print(f"    - Postal score: {match.signals.postal_score:.1f}%")
            print(f"    - City score: {match.signals.city_score:.1f}%")
            print(f"    - Phone match: {match.signals.phone_match}")
    else:
        print("No matches found")


# =============================================================================
# CUSTOM CONFIGURATION EXAMPLE
# =============================================================================

def custom_config_example():
    """Example with custom configuration"""
    print("\n" + "=" * 70)
    print("CUSTOM CONFIGURATION EXAMPLE")
    print("=" * 70)
    
    # Custom config: Higher thresholds, different weights
    config = MatchConfig(
        high_threshold=90.0,    # Stricter high threshold
        medium_threshold=70.0,  # Stricter medium threshold
        low_threshold=55.0,     # Stricter low threshold
        name_weight=0.50,       # More weight on name
        postal_weight=0.20,     # Less weight on postal
        city_weight=0.15,       # More weight on city
        street_weight=0.10,
        state_weight=0.05,
        phone_match_bonus=15.0  # Higher phone bonus
    )
    
    matcher = CompanyMatcher(config=config)
    matcher.index_companies(EXISTING_COMPANIES)
    
    incoming = {
        'name': 'Best Baking Co',
        'street': '456 Oak Ave',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60602'
    }
    
    print(f"\nSearching with stricter config for: {incoming['name']}")
    
    matches = matcher.find_matches(incoming)
    
    for match in matches:
        print(f"\n  {match.existing_name}: {match.confidence:.1f}% ({match.match_tier.value})")


# =============================================================================
# RUN ALL TEST CASES
# =============================================================================

def run_tests():
    """Run all test cases and show results"""
    print("\n" + "=" * 70)
    print("RUNNING TEST CASES")
    print("=" * 70)
    
    matcher = CompanyMatcher()
    matcher.index_companies(EXISTING_COMPANIES)
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(TEST_CASES, 1):
        incoming = {k: v for k, v in test.items() 
                   if k not in ['expected_match_id', 'expected_tier', 'description']}
        
        matches = matcher.find_matches(incoming, max_results=1)
        best_match = matches[0] if matches else None
        
        # Check results
        if test['expected_match_id'] is None:
            # Expected no match
            success = best_match is None or best_match.match_tier == MatchTier.NO_MATCH
        else:
            # Expected a match
            success = (
                best_match is not None and 
                best_match.existing_id == test['expected_match_id']
            )
        
        status = "✓ PASS" if success else "✗ FAIL"
        if success:
            passed += 1
        else:
            failed += 1
        
        print(f"\nTest {i}: {test['description']}")
        print(f"  Input: {incoming.get('name', 'N/A')}")
        print(f"  Expected: ID={test['expected_match_id']}, Tier={test['expected_tier'].value if test['expected_tier'] else 'None'}")
        if best_match:
            print(f"  Got: ID={best_match.existing_id}, Tier={best_match.match_tier.value}, Score={best_match.confidence:.1f}%")
        else:
            print(f"  Got: No match")
        print(f"  {status}")
    
    print("\n" + "-" * 50)
    print(f"Results: {passed} passed, {failed} failed out of {len(TEST_CASES)} tests")


# =============================================================================
# ONE-SHOT MATCHING (SIMPLE API)
# =============================================================================

def one_shot_example():
    """Example using the simple one-shot function"""
    print("\n" + "=" * 70)
    print("ONE-SHOT MATCHING EXAMPLE")
    print("=" * 70)
    
    incoming = {
        'name': 'Atlantic Seafood Inc',
        'city': 'Portland',
        'state': 'ME',
        'postal': '04101'
    }
    
    # Simple one-liner
    matches = match_company(incoming, EXISTING_COMPANIES)
    
    print(f"\nSearching for: {incoming['name']}")
    
    if matches:
        best = matches[0]
        print(f"Best match: {best.existing_name} ({best.confidence:.1f}%)")
    else:
        print("No matches found")


# =============================================================================
# LLM VERIFICATION EXAMPLE (Requires anthropic package)
# =============================================================================

def llm_verification_example():
    """Example with LLM verification for edge cases"""
    print("\n" + "=" * 70)
    print("LLM VERIFICATION EXAMPLE")
    print("=" * 70)
    
    try:
        import anthropic
        
        # Setup
        client = anthropic.Anthropic()
        verifier = LLMVerifier(client=client)
        
        config = MatchConfig(
            use_llm_verification=True,
            llm_verify_min_score=55.0,
            llm_verify_max_score=80.0,
            llm_weight=0.3
        )
        
        matcher = CompanyMatcher(config=config, llm_client=client)
        matcher.index_companies(EXISTING_COMPANIES)
        
        # Ambiguous case that should trigger LLM verification
        incoming = {
            'name': 'Chicago Kosher',  # Similar to "Chicago Kosher Foods"
            'street': '800 Devon Ave',  # Similar address
            'city': 'Chicago',
            'state': 'IL',
            'postal': '60659'
        }
        
        print(f"\nSearching for: {incoming['name']}")
        print("(This case is ambiguous and will trigger LLM verification)")
        print("-" * 50)
        
        matches = matcher.find_matches(incoming)
        
        for match in matches:
            print(f"\nMatch: {match.existing_name}")
            print(f"  Final confidence: {match.confidence:.1f}%")
            print(f"  Tier: {match.match_tier.value}")
            if match.signals.llm_verified:
                print(f"  LLM verified: Yes")
                print(f"  LLM confidence: {match.signals.llm_confidence:.1f}%")
                print(f"  LLM reasoning: {match.signals.llm_reasoning}")
            else:
                print(f"  LLM verified: No (outside verification range)")
                
    except ImportError:
        print("\nSkipping LLM example - anthropic package not installed")
        print("Install with: pip install anthropic")
    except Exception as e:
        print(f"\nLLM example error: {e}")


# =============================================================================
# BATCH PROCESSING EXAMPLE
# =============================================================================

def batch_processing_example():
    """Example of processing multiple incoming companies"""
    print("\n" + "=" * 70)
    print("BATCH PROCESSING EXAMPLE")
    print("=" * 70)
    
    matcher = CompanyMatcher()
    matcher.index_companies(EXISTING_COMPANIES)
    
    # Batch of incoming companies to match
    incoming_batch = [
        {'name': 'Acme Foods', 'city': 'Chicago', 'state': 'IL', 'postal': '60601'},
        {'name': 'Best Baking', 'city': 'Chicago', 'state': 'IL', 'postal': '60602'},
        {'name': 'New Company LLC', 'city': 'Miami', 'state': 'FL', 'postal': '33101'},
        {'name': 'Global Food Mfg', 'city': 'Newark', 'state': 'NJ', 'postal': '07102'},
        {'name': 'Sunrise Bakery', 'city': 'Los Angeles', 'state': 'CA', 'postal': '90001'},
    ]
    
    print(f"\nProcessing {len(incoming_batch)} incoming companies...")
    print("-" * 50)
    
    results_summary = {
        'HIGH': [],
        'MEDIUM': [],
        'LOW': [],
        'NO_MATCH': []
    }
    
    for incoming in incoming_batch:
        best_match = matcher.find_best_match(incoming)
        
        if best_match:
            tier = best_match.match_tier.value
            results_summary[tier].append({
                'incoming': incoming['name'],
                'matched': best_match.existing_name,
                'score': best_match.confidence
            })
        else:
            results_summary['NO_MATCH'].append({
                'incoming': incoming['name'],
                'matched': None,
                'score': 0
            })
    
    # Print summary
    print("\n--- BATCH RESULTS SUMMARY ---\n")
    
    print(f"HIGH confidence (auto-link candidates): {len(results_summary['HIGH'])}")
    for r in results_summary['HIGH']:
        print(f"  • {r['incoming']} → {r['matched']} ({r['score']:.1f}%)")
    
    print(f"\nMEDIUM confidence (review required): {len(results_summary['MEDIUM'])}")
    for r in results_summary['MEDIUM']:
        print(f"  • {r['incoming']} → {r['matched']} ({r['score']:.1f}%)")
    
    print(f"\nLOW confidence (possible matches): {len(results_summary['LOW'])}")
    for r in results_summary['LOW']:
        print(f"  • {r['incoming']} → {r['matched']} ({r['score']:.1f}%)")
    
    print(f"\nNO MATCH (new records): {len(results_summary['NO_MATCH'])}")
    for r in results_summary['NO_MATCH']:
        print(f"  • {r['incoming']}")


# =============================================================================
# EXPORT MATCH RESULTS TO JSON
# =============================================================================

def export_results_example():
    """Example of exporting match results to JSON"""
    print("\n" + "=" * 70)
    print("EXPORT RESULTS EXAMPLE")
    print("=" * 70)
    
    import json
    
    matcher = CompanyMatcher()
    matcher.index_companies(EXISTING_COMPANIES)
    
    incoming = {
        'name': 'Acme Foods',
        'street': '123 Main St',
        'city': 'Chicago',
        'state': 'IL',
        'postal': '60601'
    }
    
    matches = matcher.find_matches(incoming, max_results=3)
    
    # Convert to JSON-serializable format
    export_data = {
        'query': incoming,
        'matches': [match.to_dict() for match in matches],
        'match_count': len(matches)
    }
    
    print("\nJSON Export:")
    print(json.dumps(export_data, indent=2, default=str))


# =============================================================================
# MAIN
# =============================================================================

if __name__ == '__main__':
    # Run all examples
    basic_example()
    custom_config_example()
    run_tests()
    one_shot_example()
    batch_processing_example()
    export_results_example()
    
    # LLM verification (optional - requires API key)
    # Uncomment to test:
    # llm_verification_example()
