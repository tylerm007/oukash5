"""
Company/Plant Fuzzy Matching Service
=====================================

A robust matching solution for finding duplicate companies and plants
in kosher certification applications.

Features:
- Multi-algorithm name similarity (token sort, partial ratio, phonetic)
- Address component matching with standardization
- Configurable scoring weights
- Optional LLM verification for edge cases
- Detailed match explanations for audit trails

Author: AIMicroservice Consulting
"""

import re
import logging
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from datetime import datetime

# Third-party imports (install via: pip install rapidfuzz phonetics)
from rapidfuzz import fuzz, process
from rapidfuzz.distance import Levenshtein

# Optional: phonetics for SOUNDEX/Metaphone
try:
    import phonetics
    HAS_PHONETICS = True
except ImportError:
    HAS_PHONETICS = False
    logging.warning("phonetics library not installed. Phonetic matching disabled.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MatchTier(Enum):
    """Classification tiers for match confidence"""
    HIGH = "HIGH"           # Auto-link candidate (≥85)
    MEDIUM = "MEDIUM"       # Human review recommended (65-84)
    LOW = "LOW"             # Possible match, flag for later (50-64)
    NO_MATCH = "NO_MATCH"   # Below threshold (<50)


@dataclass
class MatchSignals:
    """Detailed breakdown of match scoring signals"""
    name_similarity: float = 0.0
    name_token_sort: float = 0.0
    name_partial: float = 0.0
    name_phonetic_match: bool = False
    
    postal_score: float = 0.0
    postal_exact: bool = False
    postal_zone_match: bool = False  # First 3 digits match
    
    city_score: float = 0.0
    city_exact: bool = False
    
    state_match: bool = False
    
    street_similarity: float = 0.0
    
    phone_match: bool = False
    phone_score: float = 0.0
    
    domain_match: bool = False  # Website domain matches
    
    # LLM verification (if used)
    llm_verified: bool = False
    llm_confidence: Optional[float] = None
    llm_reasoning: Optional[str] = None


@dataclass
class MatchResult:
    """Complete match result with all details"""
    existing_id: Any
    existing_name: str
    existing_data: Dict
    
    confidence: float
    match_tier: MatchTier
    signals: MatchSignals
    
    # Metadata
    matched_at: datetime = field(default_factory=lambda: datetime.now().strftime('%Y%m%d_%H%M%S'))
    matcher_version: str = "1.0.0"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'existing_id': self.existing_id,
            'existing_name': self.existing_name,
            'confidence': round(self.confidence, 2),
            'match_tier': self.match_tier.value,
            'signals': {
                'name_similarity': round(self.signals.name_similarity, 2),
                'postal_score': round(self.signals.postal_score, 2),
                'city_score': round(self.signals.city_score, 2),
                'street_similarity': round(self.signals.street_similarity, 2),
                'phone_match': self.signals.phone_match,
                'llm_verified': self.signals.llm_verified,
                'llm_confidence': self.signals.llm_confidence,
            },
            'matched_at': self.matched_at.isoformat(),
        }


@dataclass
class MatchConfig:
    """Configuration for matching behavior"""
    # Score thresholds
    high_threshold: float = 85.0
    medium_threshold: float = 65.0
    low_threshold: float = 50.0
    
    # Scoring weights (should sum to ~1.0 before phone bonus)
    name_weight: float = 0.45
    postal_weight: float = 0.25
    city_weight: float = 0.10
    street_weight: float = 0.15
    state_weight: float = 0.05
    
    # Bonus scores
    phone_match_bonus: float = 10.0
    domain_match_bonus: float = 5.0
    
    # LLM verification settings
    use_llm_verification: bool = False
    llm_verify_min_score: float = 55.0  # Only verify scores between this...
    llm_verify_max_score: float = 80.0  # ...and this
    llm_weight: float = 0.3  # How much LLM affects final score
    
    # Blocking/filtering
    max_candidates: int = 50  # Max candidates to score per query
    min_name_similarity_block: float = 35.0  # Pre-filter threshold


class CompanyNameStandardizer:
    """Standardizes company names for comparison"""
    
    # Common suffixes to remove (order matters - longer first)
    SUFFIXES = [
        r'\s+incorporated$',
        r'\s+corporation$',
        r'\s+limited$',
        r'\s+company$',
        r'\s+l\.?l\.?c\.?$',
        r'\s+inc\.?$',
        r'\s+llc\.?$',
        r'\s+ltd\.?$',
        r'\s+corp\.?$',
        r'\s+co\.?$',
        r'\s+plc\.?$',
        r'\s+gmbh$',
        r'\s+sa$',
        r'\s+nv$',
        r'\s+bv$',
        r'\s+ag$',
    ]
    
    # Common word standardizations
    WORD_MAP = {
        'manufacturing': 'mfg',
        'international': 'intl',
        'industries': 'ind',
        'enterprises': 'ent',
        'solutions': 'sol',
        'services': 'svc',
        'products': 'prod',
        'technologies': 'tech',
        'systems': 'sys',
        'associates': 'assoc',
        'brothers': 'bros',
        'national': 'natl',
        'american': 'amer',
        '&': 'and',
    }
    
    @classmethod
    def standardize(cls, name: str) -> str:
        """
        Standardize a company name for comparison.
        
        Args:
            name: Raw company name
            
        Returns:
            Standardized name (lowercase, no suffixes, normalized terms)
        """
        if not name:
            return ''
        
        # Lowercase and strip
        result = name.lower().strip()
        
        # Remove suffixes
        for pattern in cls.SUFFIXES:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)
        
        # Apply word standardizations
        for word, replacement in cls.WORD_MAP.items():
            result = re.sub(rf'\b{word}\b', replacement, result, flags=re.IGNORECASE)
        
        # Remove punctuation except apostrophes in names
        result = re.sub(r"[^\w\s']", ' ', result)
        
        # Normalize whitespace
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()


class AddressStandardizer:
    """Standardizes address components for comparison"""
    
    # Street type abbreviations
    STREET_TYPES = {
        'street': 'st',
        'avenue': 'ave',
        'boulevard': 'blvd',
        'drive': 'dr',
        'road': 'rd',
        'lane': 'ln',
        'court': 'ct',
        'circle': 'cir',
        'place': 'pl',
        'terrace': 'ter',
        'highway': 'hwy',
        'parkway': 'pkwy',
        'expressway': 'expy',
        'freeway': 'fwy',
        'turnpike': 'tpke',
        'trail': 'trl',
        'way': 'way',
        'alley': 'aly',
        'loop': 'loop',
    }
    
    # Directional abbreviations
    DIRECTIONS = {
        'north': 'n',
        'south': 's',
        'east': 'e',
        'west': 'w',
        'northeast': 'ne',
        'northwest': 'nw',
        'southeast': 'se',
        'southwest': 'sw',
    }
    
    # Unit type abbreviations
    UNIT_TYPES = {
        'suite': 'ste',
        'apartment': 'apt',
        'unit': 'unit',
        'floor': 'fl',
        'building': 'bldg',
        'room': 'rm',
        'department': 'dept',
        '#': 'ste',
    }
    
    @classmethod
    def standardize_street(cls, street: str) -> str:
        """Standardize street address"""
        if not street:
            return ''
        
        result = street.lower().strip()
        
        # Apply street type abbreviations
        for full, abbrev in cls.STREET_TYPES.items():
            result = re.sub(rf'\b{full}\.?\b', abbrev, result)
        
        # Apply directional abbreviations
        for full, abbrev in cls.DIRECTIONS.items():
            result = re.sub(rf'\b{full}\.?\b', abbrev, result)
        
        # Apply unit type abbreviations
        for full, abbrev in cls.UNIT_TYPES.items():
            result = re.sub(rf'\b{re.escape(full)}\.?\b', abbrev, result)
        
        # Remove punctuation
        result = re.sub(r'[^\w\s]', ' ', result)
        
        # Normalize whitespace
        result = re.sub(r'\s+', ' ', result)
        
        return result.strip()
    
    @classmethod
    def standardize_city(cls, city: str) -> str:
        """Standardize city name"""
        if not city:
            return ''
        
        result = city.lower().strip()
        
        # Common city name variations
        result = re.sub(r'\bsaint\b', 'st', result)
        result = re.sub(r'\bfort\b', 'ft', result)
        result = re.sub(r'\bmount\b', 'mt', result)
        
        # Remove punctuation
        result = re.sub(r'[^\w\s]', '', result)
        
        return result.strip()
    
    @classmethod
    def normalize_postal(cls, postal: str) -> str:
        """Normalize postal/zip code"""
        if not postal:
            return ''
        
        # Remove all non-alphanumeric characters
        result = re.sub(r'[^\w]', '', str(postal).upper())
        
        return result
    
    @classmethod
    def normalize_phone(cls, phone: str) -> str:
        """Normalize phone number to digits only"""
        if not phone:
            return ''
        
        # Extract digits only
        digits = re.sub(r'\D', '', str(phone))
        
        # Handle country codes (if starts with 1 and has 11 digits, remove leading 1)
        if len(digits) == 11 and digits.startswith('1'):
            digits = digits[1:]
        
        return digits


class CompanyMatcher:
    """
    Main matching engine for company/plant deduplication.
    
    Usage:
        matcher = CompanyMatcher(config=MatchConfig())
        matcher.index_companies(existing_companies)
        results = matcher.find_matches(incoming_record)
    """
    
    def __init__(self, config: Optional[MatchConfig] = None, llm_client: Optional[Any] = None):
        """
        Initialize the matcher.
        
        Args:
            config: Matching configuration
            llm_client: Optional Anthropic client for LLM verification
        """
        self.config = config or MatchConfig()
        self.llm_client = llm_client
        
        # Indexed data
        self.companies: Dict[Any, Dict] = {}
        self.standardized_names: Dict[Any, str] = {}
        self.postal_index: Dict[str, List[Any]] = {}  # postal -> [company_ids]
        self.city_state_index: Dict[str, List[Any]] = {}  # "city|state" -> [company_ids]
        
        # Name standardizer
        self.name_std = CompanyNameStandardizer()
        self.addr_std = AddressStandardizer()
    
    def index_companies(self, companies: List[Dict]) -> None:
        """
        Build search index from existing companies.
        
        Args:
            companies: List of company dicts with keys:
                - id (required): Unique identifier
                - name (required): Company name
                - street: Street address
                - city: City
                - state: State/province
                - postal: Postal/zip code
                - phone: Phone number
                - website: Website URL
        """
        logger.info(f"Indexing {len(companies)} companies...")
        
        self.companies.clear()
        self.standardized_names.clear()
        self.postal_index.clear()
        self.city_state_index.clear()
        
        for company in companies:
            company_id = company['id']
            self.companies[company_id] = company
            
            # Index standardized name
            std_name = self.name_std.standardize(company.get('name', ''))
            self.standardized_names[company_id] = std_name
            
            # Index by postal code (first 5 chars)
            postal = self.addr_std.normalize_postal(company.get('postal', ''))[:5]
            if postal:
                if postal not in self.postal_index:
                    self.postal_index[postal] = []
                self.postal_index[postal].append(company_id)
            
            # Index by city + state
            city = self.addr_std.standardize_city(company.get('city', ''))
            state = (company.get('state', '') or '').lower().strip()
            if city and state:
                key = f"{city}|{state}"
                if key not in self.city_state_index:
                    self.city_state_index[key] = []
                self.city_state_index[key].append(company_id)
        
        logger.info(f"Indexed {len(self.companies)} company/plants, "
                   f"{len(self.postal_index)} postal codes, "
                   f"{len(self.city_state_index)} city/state combinations")
    
    def _get_blocking_candidates(self, incoming: Dict) -> set:
        """
        Get candidate company IDs using blocking strategy.
        Reduces comparison space dramatically.
        """
        candidates = set()
        
        # Block 1: Same postal code
        postal = self.addr_std.normalize_postal(incoming.get('postal', ''))[:5]
        if postal in self.postal_index:
            candidates.update(self.postal_index[postal])
        
        # Block 2: Same postal zone (first 3 digits)
        postal_zone = postal[:3] if postal else ''
        for indexed_postal, company_ids in self.postal_index.items():
            if indexed_postal.startswith(postal_zone):
                candidates.update(company_ids)
        
        # Block 3: Same city + state
        city = self.addr_std.standardize_city(incoming.get('city', ''))
        state = (incoming.get('state', '') or '').lower().strip()
        if city and state:
            key = f"{city}|{state}"
            if key in self.city_state_index:
                candidates.update(self.city_state_index[key])
        
        # Block 4: Name similarity using rapidfuzz process.extract
        std_incoming_name = self.name_std.standardize(incoming.get('name', ''))
        if std_incoming_name and self.standardized_names:
            name_matches = process.extract(
                std_incoming_name,
                self.standardized_names,
                scorer=fuzz.token_sort_ratio,
                limit=self.config.max_candidates,
                score_cutoff=self.config.min_name_similarity_block
            )
            for match in name_matches:
                # match is (matched_string, score, key)
                candidates.add(match[2])
        
        return candidates
    
    def _calculate_name_similarity(self, name1: str, name2: str) -> Tuple[float, float, float]:
        """
        Calculate name similarity using multiple algorithms.
        
        Returns:
            Tuple of (combined_score, token_sort_score, partial_score)
        """
        std1 = self.name_std.standardize(name1)
        std2 = self.name_std.standardize(name2)
        
        if not std1 or not std2:
            return (0.0, 0.0, 0.0)
        
        # Token sort ratio - handles word order differences
        # "Acme Food Company" vs "Company Food Acme" -> high score
        token_sort = fuzz.token_sort_ratio(std1, std2)
        
        # Partial ratio - handles substring matches
        # "Acme" vs "Acme Foods International" -> high score
        partial = fuzz.partial_ratio(std1, std2)
        
        # Standard ratio
        ratio = fuzz.ratio(std1, std2)
        
        # Token set ratio - handles duplicates and subsets
        token_set = fuzz.token_set_ratio(std1, std2)
        
        # Weighted combination
        combined = (
            token_sort * 0.35 +
            partial * 0.25 +
            ratio * 0.20 +
            token_set * 0.20
        )
        
        return (combined, token_sort, partial)
    
    def _check_phonetic_match(self, name1: str, name2: str) -> bool:
        """Check if names match phonetically (SOUNDEX)"""
        if not HAS_PHONETICS:
            return False
        
        std1 = self.name_std.standardize(name1)
        std2 = self.name_std.standardize(name2)
        
        if not std1 or not std2:
            return False
        
        try:
            # Compare first word SOUNDEX codes
            word1 = std1.split()[0] if std1 else ''
            word2 = std2.split()[0] if std2 else ''
            
            return phonetics.soundex(word1) == phonetics.soundex(word2)
        except:
            return False
    
    def _calculate_address_score(self, incoming: Dict, existing: Dict) -> Tuple[MatchSignals, float]:
        """
        Calculate address similarity score and populate signals.
        
        Returns:
            Tuple of (signals, address_score)
        """
        signals = MatchSignals()
        
        # Postal code scoring
        in_postal = self.addr_std.normalize_postal(incoming.get('postal', ''))
        ex_postal = self.addr_std.normalize_postal(existing.get('postal', ''))
        
        if in_postal and ex_postal:
            if in_postal[:5] == ex_postal[:5]:
                signals.postal_exact = True
                signals.postal_score = 100.0
            elif in_postal[:3] == ex_postal[:3]:
                signals.postal_zone_match = True
                signals.postal_score = 60.0
        
        # City scoring
        in_city = self.addr_std.standardize_city(incoming.get('city', ''))
        ex_city = self.addr_std.standardize_city(existing.get('city', ''))
        
        if in_city and ex_city:
            if in_city == ex_city:
                signals.city_exact = True
                signals.city_score = 100.0
            else:
                # Fuzzy city match (handles typos)
                city_sim = fuzz.ratio(in_city, ex_city)
                if city_sim > 80:
                    signals.city_score = city_sim
        
        # State matching
        in_state = (incoming.get('state', '') or '').lower().strip()
        ex_state = (existing.get('state', '') or '').lower().strip()
        signals.state_match = (in_state == ex_state) if (in_state and ex_state) else False
        
        # Street similarity
        in_street = self.addr_std.standardize_street(incoming.get('street', ''))
        ex_street = self.addr_std.standardize_street(existing.get('street', ''))
        
        if in_street and ex_street:
            signals.street_similarity = fuzz.token_sort_ratio(in_street, ex_street)

         # Street similarity
        in_street2 = self.addr_std.standardize_street(incoming.get('street2', ''))
        ex_street2 = self.addr_std.standardize_street(existing.get('street2', ''))
        
        if in_street2 and ex_street2:
            s = fuzz.token_sort_ratio(in_street2, ex_street2)
            signals.street_similarity = max(signals.street_similarity, s)
        
        # Phone matching
        in_phone = self.addr_std.normalize_phone(incoming.get('phone', ''))
        ex_phone = self.addr_std.normalize_phone(existing.get('phone', ''))
        
        if in_phone and ex_phone and len(in_phone) >= 10 and len(ex_phone) >= 10:
            if in_phone == ex_phone:
                signals.phone_match = True
                signals.phone_score = 100.0
            elif in_phone[-10:] == ex_phone[-10:]:  # Last 10 digits match
                signals.phone_match = True
                signals.phone_score = 90.0
        
        # Domain matching (extract domain from website)
        in_website = (incoming.get('website', '') or '').lower()
        ex_website = (existing.get('website', '') or '').lower()
        
        if in_website and ex_website:
            in_domain = re.sub(r'^https?://(www\.)?', '', in_website).split('/')[0]
            ex_domain = re.sub(r'^https?://(www\.)?', '', ex_website).split('/')[0]
            signals.domain_match = (in_domain == ex_domain) if (in_domain and ex_domain) else False
        
        # Calculate weighted address score
        address_score = (
            signals.postal_score * (self.config.postal_weight / 
                (self.config.postal_weight + self.config.city_weight + 
                 self.config.street_weight + self.config.state_weight)) +
            signals.city_score * (self.config.city_weight /
                (self.config.postal_weight + self.config.city_weight + 
                 self.config.street_weight + self.config.state_weight)) +
            signals.street_similarity * (self.config.street_weight /
                (self.config.postal_weight + self.config.city_weight + 
                 self.config.street_weight + self.config.state_weight)) +
            (100.0 if signals.state_match else 0.0) * (self.config.state_weight /
                (self.config.postal_weight + self.config.city_weight + 
                 self.config.street_weight + self.config.state_weight))
        )
        
        return signals, address_score
    
    def _calculate_composite_score(self, signals: MatchSignals) -> float:
        """Calculate final composite confidence score"""
        # Base score from name and address
        score = (
            signals.name_similarity * self.config.name_weight +
            signals.postal_score * self.config.postal_weight +
            signals.city_score * self.config.city_weight +
            signals.street_similarity * self.config.street_weight +
            (100.0 if signals.state_match else 0.0) * self.config.state_weight
        )
        
        # Bonus for phone match
        if signals.phone_match:
            score += self.config.phone_match_bonus
        
        # Bonus for domain match
        if signals.domain_match:
            score += self.config.domain_match_bonus
        
        # Cap at 100
        return min(score, 100.0)
    
    def _determine_tier(self, score: float) -> MatchTier:
        """Determine match tier from score"""
        if score >= self.config.high_threshold:
            return MatchTier.HIGH
        elif score >= self.config.medium_threshold:
            return MatchTier.MEDIUM
        elif score >= self.config.low_threshold:
            return MatchTier.LOW
        else:
            return MatchTier.NO_MATCH
    
    def _verify_with_llm(self, incoming: Dict, existing: Dict, signals: MatchSignals) -> Tuple[float, str]:
        """
        Use Claude to verify ambiguous matches.
        
        Returns:
            Tuple of (confidence_0_100, reasoning)
        """
        if not self.llm_client:
            return (50.0, "LLM client not configured")
        
        prompt = f"""Determine if these two records likely represent the same company or business location.

Record A (New Application):
- Company Name: {incoming.get('name', 'N/A')}
- Address: {incoming.get('street', 'N/A')}, {incoming.get('city', 'N/A')}, {incoming.get('state', 'N/A')} {incoming.get('postal', 'N/A')}
- Phone: {incoming.get('phone', 'N/A')}
- Website: {incoming.get('website', 'N/A')}

Record B (Existing Record):
- Company Name: {existing.get('name', 'N/A')}
- Address: {existing.get('street', 'N/A')}, {existing.get('city', 'N/A')}, {existing.get('state', 'N/A')} {existing.get('postal', 'N/A')}
- Phone: {existing.get('phone', 'N/A')}
- Website: {existing.get('website', 'N/A')}

Consider:
1. Name variations (Inc/LLC/Corp suffixes, abbreviations, DBA names, typos)
2. Address formatting differences (St vs Street, Ste vs Suite, different unit numbers)
3. Whether these could reasonably be the same physical business or company
4. Phone numbers with different formatting
5. Parent company / subsidiary relationships

Respond in this exact format:
CONFIDENCE: [number 0-100]
REASONING: [one sentence explanation]

Where:
- 0-30: Definitely different companies
- 31-50: Probably different, some superficial similarities
- 51-70: Uncertain, could be same or different
- 71-90: Probably the same company
- 91-100: Definitely the same company"""

        try:
            response = self.llm_client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=150,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text.strip()
            
            # Parse response
            confidence_match = re.search(r'CONFIDENCE:\s*(\d+)', response_text)
            reasoning_match = re.search(r'REASONING:\s*(.+)', response_text, re.DOTALL)
            
            confidence = float(confidence_match.group(1)) if confidence_match else 50.0
            reasoning = reasoning_match.group(1).strip() if reasoning_match else "Unable to parse reasoning"
            
            return (confidence, reasoning)
            
        except Exception as e:
            logger.error(f"LLM verification failed: {e}")
            return (50.0, f"LLM verification error: {str(e)}")
    
    def find_matches(
        self, 
        incoming: Dict, 
        threshold: Optional[float] = None,
        max_results: int = 10
    ) -> List[MatchResult]:
        """
        Find matching companies for an incoming record.
        
        Args:
            incoming: Dict with keys: name, street, city, state, postal, phone, website
            threshold: Minimum score threshold (default: config.low_threshold)
            max_results: Maximum results to return
            
        Returns:
            List of MatchResult sorted by confidence (descending)
        """
        threshold = threshold or self.config.low_threshold
        results = []
        
        # Get blocking candidates
        candidates = self._get_blocking_candidates(incoming)
        logger.debug(f"Found {len(candidates)} blocking candidates")
        
        # Score each candidate
        for company_id in candidates:
            existing = self.companies[company_id]
            
            # Calculate name similarity
            name_combined, name_token_sort, name_partial = self._calculate_name_similarity(
                incoming.get('name', ''),
                existing.get('name', '')
            )
            
            # Calculate address score and get signals
            signals, address_score = self._calculate_address_score(incoming, existing)
            
            # Populate name signals
            signals.name_similarity = name_combined
            signals.name_token_sort = name_token_sort
            signals.name_partial = name_partial
            signals.name_phonetic_match = self._check_phonetic_match(
                incoming.get('name', ''),
                existing.get('name', '')
            )
            
            # Calculate composite score
            confidence = self._calculate_composite_score(signals)
            
            # Skip if below threshold
            if confidence < threshold:
                continue
            
            # LLM verification for ambiguous cases
            if (self.config.use_llm_verification and 
                self.llm_client and
                self.config.llm_verify_min_score <= confidence <= self.config.llm_verify_max_score):
                
                logger.debug(f"Running LLM verification for {existing.get('name')} (score: {confidence:.1f})")
                llm_confidence, llm_reasoning = self._verify_with_llm(incoming, existing, signals)
                
                signals.llm_verified = True
                signals.llm_confidence = llm_confidence
                signals.llm_reasoning = llm_reasoning
                
                # Blend LLM score with traditional score
                confidence = (
                    confidence * (1 - self.config.llm_weight) +
                    llm_confidence * self.config.llm_weight
                )
            
            # Determine tier
            tier = self._determine_tier(confidence)
            
            if tier != MatchTier.NO_MATCH:
                results.append(MatchResult(
                    existing_id=company_id,
                    existing_name=existing.get('name', ''),
                    existing_data=existing,
                    confidence=confidence,
                    match_tier=tier,
                    signals=signals
                ))
        
        # Sort by confidence and limit results
        results.sort(key=lambda x: x.confidence, reverse=True)
        return results[:max_results]
    
    def find_best_match(self, incoming: Dict) -> Optional[MatchResult]:
        """
        Find the single best match for an incoming record.
        
        Returns:
            Best MatchResult or None if no matches above threshold
        """
        matches = self.find_matches(incoming, max_results=1)
        return matches[0] if matches else None


# Convenience function for simple usage
def match_company(
    incoming: Dict,
    existing_companies: List[Dict],
    config: Optional[MatchConfig] = None
) -> List[MatchResult]:
    """
    One-shot matching function for simple use cases.
    
    Args:
        incoming: Company to match (dict with name, address fields)
        existing_companies: List of existing companies
        config: Optional matching configuration
        
    Returns:
        List of matches sorted by confidence
    """
    matcher = CompanyMatcher(config=config)
    matcher.index_companies(existing_companies)
    return matcher.find_matches(incoming)


# Convenience function for simple usage
def match_plant(
    incoming: Dict,
    existing_plants: List[Dict],
    config: Optional[MatchConfig] = None
) -> List[MatchResult]:
    """
    One-shot matching function for simple use cases.
    
    Args:
        incoming: Plants to match (dict with name, address fields)
        existing_plants: List of existing plants
        config: Optional matching configuration
        
    Returns:
        List of matches sorted by confidence
    """
    matcher = CompanyMatcher(config=config)
    matcher.index_companies(existing_plants)
    return matcher.find_matches(incoming)


def get_company_sql():
    # Use owns to limit it to existing companies with plants
    return """
        SELECT 
            --TOP (1000) 
            -- [ID] as 'id'
            a.[COMPANY_ID] as 'id'
            , c.[NAME] as 'name'
            -- ,[ADDRESS_SEQ_NUM]
            --,[TYPE]
            --,[ATTN]
            ,[STREET1] as 'street'
            ,[STREET2] as 'street2'
            ,[STREET3] as 'street3'
            ,[CITY] as 'city'
            ,[STATE] as 'state'
            ,[ZIP] as 'postal'
            ,[Voice] as 'phone'
            , null as 'website'
        FROM [ou_kash].[dbo].[COMPANY_ADDRESS] a
        JOIN [ou_kash].[dbo].[COMPANY_TB] c on c.COMPANY_ID = a.COMPANY_ID
        JOIN [ou_kash].[dbo].companycontacts cc ON c.company_id = cc.company_id
                                     AND cc.active = 1
                                     AND cc.PrimaryCT = 'Y'
        WHERE TYPE = 'Physical' and c.COMPANY_ID in
            (select o.COMPANY_ID
            FROM [ou_kash].[dbo].[OWNS_TB] o
            JOIN [ou_kash].[dbo].COMPANY_TB c
            on c.COMPANY_ID = o.COMPANY_ID)
        FOR JSON AUTO

    """

def get_plant_sql():
    return """
       SELECT 
        -- TOP (1000) 
        -- [ID] as 'id'
        p.[PLANT_ID] as 'id'
        ,[NAME] as 'name'
        --,[ADDRESS_SEQ_NUM]
        --,[TYPE]
        --,[ATTN]
        ,[STREET1] as 'street'
        ,[STREET2] as 'street2'
        ,[STREET3] as 'street3'
        ,[CITY] as 'city'
        ,[STATE] as 'state'
        ,[ZIP] as 'postal'
        , null as 'phone'
        , null as 'website'
    FROM [ou_kash].[dbo].[PLANT_ADDRESS_TB] c
    JOIN [ou_kash].[dbo].[PLANT_TB] p on p.PLANT_ID = c.PLANT_ID
    --JOIN [ou_kash].[dbo].[PlantContacts] pc on pc.owns_ID in 
    --(select o.PLANT_ID
                --FROM [ou_kash].[dbo].[OWNS_TB] o
                --JOIN [ou_kash].[dbo].COMPANY_TB c
                --on c.COMPANY_ID = o.COMPANY_ID)
    where c.STREET1 != '' and c.ACTIVE = 1
    and c.PLANT_ID in
                (select o.PLANT_ID
                FROM [ou_kash].[dbo].[OWNS_TB] o
                JOIN [ou_kash].[dbo].[PLANT_TB] p
                on p.PLANT_ID = o.PLANT_ID)
    FOR JSON AUTO
    """