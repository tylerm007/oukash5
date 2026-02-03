"""
Company/Plant Fuzzy Matching System
====================================

A robust solution for matching company and plant records.

Usage:
    from company_matcher import CompanyMatcher, match_company, MatchConfig
    
    # Simple matching
    matches = match_company(incoming, existing_companies)
    
    # With configuration
    matcher = CompanyMatcher(config=MatchConfig(high_threshold=90))
    matcher.index_companies(existing_companies)
    matches = matcher.find_matches(incoming)
"""

from .matcher import (
    CompanyMatcher,
    MatchConfig,
    MatchResult,
    MatchSignals,
    MatchTier,
    match_company,
    CompanyNameStandardizer,
    AddressStandardizer,
)

from .llm_verifier import (
    LLMVerifier,
    BatchLLMVerifier,
    LLMVerificationResponse,
    VerificationResult,
)

__version__ = '1.0.0'
__author__ = 'AIMicroservice Consulting'

__all__ = [
    # Main classes
    'CompanyMatcher',
    'MatchConfig',
    'MatchResult',
    'MatchSignals',
    'MatchTier',
    
    # Convenience function
    'match_company',
    
    # Standardizers
    'CompanyNameStandardizer',
    'AddressStandardizer',
    
    # LLM verification
    'LLMVerifier',
    'BatchLLMVerifier',
    'LLMVerificationResponse',
    'VerificationResult',
]
