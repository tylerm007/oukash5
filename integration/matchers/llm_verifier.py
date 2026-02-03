"""
LLM Verification Module for Company Matching
=============================================

Provides Claude-based verification for ambiguous match cases.
Only called for MEDIUM-tier matches to reduce API costs.

Usage:
    verifier = LLMVerifier(client=anthropic.Anthropic())
    result = verifier.verify_match(incoming, existing, traditional_score)
"""

import re
import logging
from dataclasses import dataclass
from typing import Optional, Tuple, Dict, Any
from enum import Enum

logger = logging.getLogger(__name__)


class VerificationResult(Enum):
    """LLM verification outcomes"""
    SAME_COMPANY = "same_company"
    DIFFERENT_COMPANY = "different_company"
    UNCERTAIN = "uncertain"
    ERROR = "error"


@dataclass
class LLMVerificationResponse:
    """Structured response from LLM verification"""
    confidence: float  # 0-100
    result: VerificationResult
    reasoning: str
    raw_response: str
    tokens_used: int = 0
    

class LLMVerifier:
    """
    Uses Claude to verify ambiguous company matches.
    
    This is designed to be called sparingly - only for matches in the
    "uncertain" range (typically 55-80 confidence) where human-like
    judgment adds value.
    """
    
    # Verification prompt template
    PROMPT_TEMPLATE = """You are a data quality analyst specializing in company record matching. Determine if these two records represent the same company or business entity.

## Record A (New Application)
- **Company Name:** {incoming_name}
- **Address:** {incoming_street}, {incoming_city}, {incoming_state} {incoming_postal}
- **Phone:** {incoming_phone}
- **Website:** {incoming_website}

## Record B (Existing Database Record)
- **Company Name:** {existing_name}
- **Address:** {existing_street}, {existing_city}, {existing_state} {existing_postal}
- **Phone:** {existing_phone}
- **Website:** {existing_website}

## Traditional Match Score
The algorithmic matcher scored this as **{traditional_score:.1f}%** confidence.

## Your Analysis
Consider these factors:
1. **Name variations:** Inc/LLC/Corp suffixes, abbreviations (Mfg=Manufacturing), DBA names, typos
2. **Address variations:** St vs Street, Ste vs Suite, different unit/suite numbers at same building
3. **Business relationships:** Parent/subsidiary, same company different locations, franchises
4. **Contact info:** Different formatting of same phone, related domains

## Response Format
Provide your assessment in exactly this format:

CONFIDENCE: [0-100]
RESULT: [SAME | DIFFERENT | UNCERTAIN]
REASONING: [One sentence explanation]

Where confidence means:
- 0-25: Definitely different companies
- 26-45: Probably different, coincidental similarities
- 46-55: Uncertain, could go either way
- 56-75: Probably the same company
- 76-100: Definitely the same company"""

    def __init__(
        self, 
        client: Any,  # anthropic.Anthropic client
        model: str = "claude-sonnet-4-20250514",
        max_tokens: int = 200,
        temperature: float = 0.0  # Deterministic for consistency
    ):
        """
        Initialize the LLM verifier.
        
        Args:
            client: Anthropic client instance
            model: Model to use for verification
            max_tokens: Max response tokens
            temperature: Sampling temperature (0 = deterministic)
        """
        self.client = client
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
    
    def _format_value(self, value: Any, default: str = "N/A") -> str:
        """Format a value for the prompt, handling None/empty"""
        if value is None or str(value).strip() == '':
            return default
        return str(value).strip()
    
    def _build_prompt(
        self, 
        incoming: Dict, 
        existing: Dict, 
        traditional_score: float
    ) -> str:
        """Build the verification prompt"""
        return self.PROMPT_TEMPLATE.format(
            incoming_name=self._format_value(incoming.get('name')),
            incoming_street=self._format_value(incoming.get('street')),
            incoming_city=self._format_value(incoming.get('city')),
            incoming_state=self._format_value(incoming.get('state')),
            incoming_postal=self._format_value(incoming.get('postal')),
            incoming_phone=self._format_value(incoming.get('phone')),
            incoming_website=self._format_value(incoming.get('website')),
            
            existing_name=self._format_value(existing.get('name')),
            existing_street=self._format_value(existing.get('street')),
            existing_city=self._format_value(existing.get('city')),
            existing_state=self._format_value(existing.get('state')),
            existing_postal=self._format_value(existing.get('postal')),
            existing_phone=self._format_value(existing.get('phone')),
            existing_website=self._format_value(existing.get('website')),
            
            traditional_score=traditional_score
        )
    
    def _parse_response(self, response_text: str) -> Tuple[float, VerificationResult, str]:
        """
        Parse the structured response from Claude.
        
        Returns:
            Tuple of (confidence, result, reasoning)
        """
        # Extract confidence
        confidence_match = re.search(r'CONFIDENCE:\s*(\d+(?:\.\d+)?)', response_text, re.IGNORECASE)
        confidence = float(confidence_match.group(1)) if confidence_match else 50.0
        
        # Clamp confidence to 0-100
        confidence = max(0.0, min(100.0, confidence))
        
        # Extract result
        result_match = re.search(r'RESULT:\s*(SAME|DIFFERENT|UNCERTAIN)', response_text, re.IGNORECASE)
        if result_match:
            result_str = result_match.group(1).upper()
            if result_str == 'SAME':
                result = VerificationResult.SAME_COMPANY
            elif result_str == 'DIFFERENT':
                result = VerificationResult.DIFFERENT_COMPANY
            else:
                result = VerificationResult.UNCERTAIN
        else:
            # Infer from confidence if RESULT not found
            if confidence >= 56:
                result = VerificationResult.SAME_COMPANY
            elif confidence <= 45:
                result = VerificationResult.DIFFERENT_COMPANY
            else:
                result = VerificationResult.UNCERTAIN
        
        # Extract reasoning
        reasoning_match = re.search(r'REASONING:\s*(.+?)(?:\n|$)', response_text, re.IGNORECASE | re.DOTALL)
        reasoning = reasoning_match.group(1).strip() if reasoning_match else "No reasoning provided"
        
        return (confidence, result, reasoning)
    
    def verify_match(
        self,
        incoming: Dict,
        existing: Dict,
        traditional_score: float
    ) -> LLMVerificationResponse:
        """
        Verify a potential match using Claude.
        
        Args:
            incoming: Incoming company data
            existing: Existing company data from database
            traditional_score: Score from traditional matching (0-100)
            
        Returns:
            LLMVerificationResponse with confidence, result, and reasoning
        """
        prompt = self._build_prompt(incoming, existing, traditional_score)
        
        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            
            response_text = response.content[0].text.strip()
            tokens_used = response.usage.input_tokens + response.usage.output_tokens
            
            confidence, result, reasoning = self._parse_response(response_text)
            
            return LLMVerificationResponse(
                confidence=confidence,
                result=result,
                reasoning=reasoning,
                raw_response=response_text,
                tokens_used=tokens_used
            )
            
        except Exception as e:
            logger.error(f"LLM verification failed: {e}")
            return LLMVerificationResponse(
                confidence=50.0,
                result=VerificationResult.ERROR,
                reasoning=f"Verification error: {str(e)}",
                raw_response="",
                tokens_used=0
            )
    
    def should_verify(
        self,
        traditional_score: float,
        min_score: float = 55.0,
        max_score: float = 80.0
    ) -> bool:
        """
        Determine if a match should be sent for LLM verification.
        
        Only verify "uncertain" matches - don't waste API calls on
        obvious matches or non-matches.
        
        Args:
            traditional_score: Score from traditional matching
            min_score: Minimum score to verify (below = obvious non-match)
            max_score: Maximum score to verify (above = obvious match)
            
        Returns:
            True if this match should be verified by LLM
        """
        return min_score <= traditional_score <= max_score
    
    def blend_scores(
        self,
        traditional_score: float,
        llm_confidence: float,
        llm_weight: float = 0.3
    ) -> float:
        """
        Blend traditional and LLM scores into final confidence.
        
        Args:
            traditional_score: Score from traditional matching (0-100)
            llm_confidence: Confidence from LLM verification (0-100)
            llm_weight: Weight given to LLM score (0-1)
            
        Returns:
            Blended confidence score (0-100)
        """
        traditional_weight = 1.0 - llm_weight
        blended = (traditional_score * traditional_weight) + (llm_confidence * llm_weight)
        return min(100.0, max(0.0, blended))


class BatchLLMVerifier:
    """
    Handles batch verification with rate limiting and cost tracking.
    """
    
    def __init__(
        self,
        verifier: LLMVerifier,
        max_verifications_per_batch: int = 50,
        cost_per_1k_tokens: float = 0.003  # Sonnet pricing
    ):
        self.verifier = verifier
        self.max_per_batch = max_verifications_per_batch
        self.cost_per_1k_tokens = cost_per_1k_tokens
        
        # Tracking
        self.total_verifications = 0
        self.total_tokens = 0
    
    def verify_batch(
        self,
        matches: list,  # List of (incoming, existing, traditional_score) tuples
        min_score: float = 55.0,
        max_score: float = 80.0
    ) -> list:
        """
        Verify a batch of matches, respecting limits.
        
        Returns:
            List of (original_match, verification_response) tuples
        """
        results = []
        verified_count = 0
        
        for incoming, existing, score in matches:
            if verified_count >= self.max_per_batch:
                logger.warning(f"Batch limit reached ({self.max_per_batch})")
                break
            
            if self.verifier.should_verify(score, min_score, max_score):
                response = self.verifier.verify_match(incoming, existing, score)
                results.append(((incoming, existing, score), response))
                
                self.total_verifications += 1
                self.total_tokens += response.tokens_used
                verified_count += 1
            else:
                # Skip verification, return None response
                results.append(((incoming, existing, score), None))
        
        return results
    
    @property
    def estimated_cost(self) -> float:
        """Estimated cost of all verifications so far"""
        return (self.total_tokens / 1000) * self.cost_per_1k_tokens
    
    def get_stats(self) -> Dict:
        """Get verification statistics"""
        return {
            'total_verifications': self.total_verifications,
            'total_tokens': self.total_tokens,
            'estimated_cost_usd': round(self.estimated_cost, 4)
        }


# =============================================================================
# EXAMPLE USAGE
# =============================================================================

if __name__ == '__main__':
    # Example usage (requires anthropic package and API key)
    try:
        import anthropic
        
        client = anthropic.Anthropic()  # Uses $env:ANTHROPIC_API_KEY env var
        verifier = LLMVerifier(client=client)
        
        # Test case: Similar companies
        incoming = {
            'name': 'Acme Foods Inc.',
            'street': '123 Main Street',
            'city': 'Chicago',
            'state': 'IL',
            'postal': '60601',
            'phone': '312-555-1234',
            'website': 'www.acmefoods.com'
        }
        
        existing = {
            'name': 'ACME FOOD CORPORATION',
            'street': '123 Main St, Suite 100',
            'city': 'Chicago',
            'state': 'IL',
            'postal': '60601',
            'phone': '(312) 555-1234',
            'website': 'acmefoods.com'
        }
        
        traditional_score = 72.5  # From traditional matcher
        
        if verifier.should_verify(traditional_score):
            result = verifier.verify_match(incoming, existing, traditional_score)
            
            print(f"LLM Confidence: {result.confidence}%")
            print(f"Result: {result.result.value}")
            print(f"Reasoning: {result.reasoning}")
            print(f"Tokens used: {result.tokens_used}")
            
            # Blend scores
            final_score = verifier.blend_scores(traditional_score, result.confidence)
            print(f"Blended score: {final_score:.1f}%")
        else:
            print(f"Score {traditional_score}% outside verification range, skipping LLM")
            
    except ImportError:
        print("anthropic package not installed. Run: pip install anthropic")
    except Exception as e:
        print(f"Error: {e}")
