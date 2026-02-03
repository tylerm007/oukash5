# Company/Plant Fuzzy Matching System

A robust solution for matching company and plant records in kosher certification applications. Combines traditional fuzzy matching algorithms with optional LLM verification for edge cases.

## Features

- **Multi-algorithm name matching**: Token sort ratio, partial matching, phonetic (SOUNDEX)
- **Address component scoring**: Postal code, city, street, state
- **Configurable weights and thresholds**: Tune for your data characteristics
- **Tiered confidence levels**: HIGH (auto-link), MEDIUM (review), LOW (possible), NO_MATCH
- **Optional LLM verification**: Claude-based verification for ambiguous cases
- **SQL Server implementation**: Pure T-SQL for database-side matching
- **Batch processing support**: Process import files efficiently
- **Audit trail**: Detailed signals for every match decision

## Quick Start

### Python

```python
from matcher import CompanyMatcher, match_company

# Simple one-shot matching
incoming = {
    'name': 'Acme Foods Inc',
    'street': '123 Main St',
    'city': 'Chicago',
    'state': 'IL',
    'postal': '60601'
}

existing_companies = [
    {'id': 1, 'name': 'ACME FOODS', 'city': 'Chicago', 'postal': '60601'},
    {'id': 2, 'name': 'Best Baking LLC', 'city': 'Chicago', 'postal': '60602'},
]

matches = match_company(incoming, existing_companies)

for match in matches:
    print(f"{match.existing_name}: {match.confidence:.1f}% ({match.match_tier.value})")
```

### SQL Server

```sql
EXEC dbo.sp_FindMatchingCompanies
    @incoming_name = 'Acme Foods Inc',
    @incoming_street = '123 Main St',
    @incoming_city = 'Chicago',
    @incoming_state = 'IL',
    @incoming_postal = '60601'
```

## Installation

```bash
pip install rapidfuzz phonetics

# Optional: For LLM verification
pip install anthropic
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                       MATCHING PIPELINE                              │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  1. STANDARDIZATION                                                  │
│     ├── Strip suffixes (Inc, LLC, Corp)                             │
│     ├── Normalize case, whitespace, punctuation                     │
│     └── Abbreviate common terms (Street→St, Manufacturing→Mfg)      │
│                                                                      │
│  2. BLOCKING (Reduce Comparison Space)                               │
│     ├── Same postal code                                            │
│     ├── Same city + state                                           │
│     ├── Same first 3 chars of standardized name                     │
│     └── Phonetic (SOUNDEX) match                                    │
│                                                                      │
│  3. SCORING                                                          │
│     ├── Name: 45% (token sort, partial ratio, phonetic)             │
│     ├── Postal: 25% (exact match or zone match)                     │
│     ├── City: 10%                                                   │
│     ├── Street: 15%                                                 │
│     ├── State: 5%                                                   │
│     └── Bonus: Phone (+10), Domain (+5)                             │
│                                                                      │
│  4. CLASSIFICATION                                                   │
│     ├── HIGH (≥85): Auto-link candidate                             │
│     ├── MEDIUM (65-84): Human review required                       │
│     ├── LOW (50-64): Possible match, flag for later                 │
│     └── NO_MATCH (<50): Create new record                           │
│                                                                      │
│  5. LLM VERIFICATION (Optional, MEDIUM tier only)                    │
│     └── Claude verifies ambiguous cases, blends with score          │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Configuration

```python
from matcher import MatchConfig, CompanyMatcher

config = MatchConfig(
    # Thresholds
    high_threshold=85.0,
    medium_threshold=65.0,
    low_threshold=50.0,
    
    # Scoring weights (should sum to ~1.0)
    name_weight=0.45,
    postal_weight=0.25,
    city_weight=0.10,
    street_weight=0.15,
    state_weight=0.05,
    
    # Bonus scores
    phone_match_bonus=10.0,
    domain_match_bonus=5.0,
    
    # LLM verification
    use_llm_verification=True,
    llm_verify_min_score=55.0,
    llm_verify_max_score=80.0,
    llm_weight=0.3
)

matcher = CompanyMatcher(config=config)
```

## Match Result Structure

```python
@dataclass
class MatchResult:
    existing_id: Any           # Database ID
    existing_name: str         # Company name
    existing_data: Dict        # Full record
    confidence: float          # 0-100 score
    match_tier: MatchTier      # HIGH, MEDIUM, LOW, NO_MATCH
    signals: MatchSignals      # Detailed scoring breakdown
```

### Match Signals

```python
@dataclass
class MatchSignals:
    name_similarity: float     # Combined name score
    name_token_sort: float     # Token sort ratio
    name_partial: float        # Partial match ratio
    name_phonetic_match: bool  # SOUNDEX match
    
    postal_score: float        # Postal code score
    postal_exact: bool         # Exact 5-digit match
    postal_zone_match: bool    # First 3 digits match
    
    city_score: float
    city_exact: bool
    
    state_match: bool
    street_similarity: float
    phone_match: bool
    domain_match: bool
    
    # LLM verification
    llm_verified: bool
    llm_confidence: float
    llm_reasoning: str
```

## Files

| File | Description |
|------|-------------|
| `matcher.py` | Main Python matching engine |
| `llm_verifier.py` | Claude-based verification for edge cases |
| `sql_server_matching.sql` | T-SQL stored procedures |
| `example_usage.py` | Usage examples and test cases |
| `requirements.txt` | Python dependencies |

## SQL Server Functions

| Function | Description |
|----------|-------------|
| `fn_LevenshteinDistance` | Calculate edit distance between strings |
| `fn_StringSimilarity` | 0-100 similarity score |
| `fn_StandardizeCompanyName` | Normalize company names |
| `fn_StandardizeStreet` | Normalize street addresses |
| `fn_StandardizeCity` | Normalize city names |
| `fn_NormalizePhone` | Extract phone digits |
| `fn_NormalizePostal` | Normalize postal codes |

| Stored Procedure | Description |
|------------------|-------------|
| `sp_FindMatchingCompanies` | Match a single incoming company |
| `sp_FindMatchingFacilities` | Match a single facility/plant |
| `sp_BatchMatchCompanies` | Process import batch |

## Best Practices

### When to Auto-Link (HIGH tier)
- Score ≥85%
- Only one HIGH match (not ambiguous)
- Name similarity >80% AND postal code exact match

### When to Review (MEDIUM tier)
- Score 65-84%
- Multiple signals but not conclusive
- Good candidate for LLM verification

### When to Flag (LOW tier)
- Score 50-64%
- Some similarity but significant differences
- May be related company (parent/subsidiary)

### When to Create New (NO_MATCH)
- Score <50%
- No meaningful overlap
- Safe to create new record

## Integration with Kosher Certification System

This matching system is designed to integrate with the kosher certification application workflow:

1. **Application Intake**: When new application arrives, run matching
2. **Duplicate Detection**: Prevent duplicate company records
3. **Plant Matching**: Link facilities to existing companies
4. **Import Processing**: Batch match imported records
5. **Audit Trail**: Store match decisions for compliance

## License

Proprietary - AIMicroservice Consulting
