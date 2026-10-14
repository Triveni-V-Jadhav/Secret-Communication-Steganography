import hmac
import hashlib

class DigitalSignatureService:
    """Provides HMAC-SHA256 message authentication codes."""
    
    @staticmethod
    def sign_metadata(key_bytes: bytes, metadata_str: str) -> str:
        h = hmac.new(key_bytes, metadata_str.encode("utf-8"), hashlib.sha256)
        return h.hexdigest()
        
    @staticmethod
    def verify_metadata_signature(key_bytes: bytes, metadata_str: str, expected_signature: str) -> bool:
        computed = DigitalSignatureService.sign_metadata(key_bytes, metadata_str)
        return hmac.compare_digest(computed, expected_signature)
