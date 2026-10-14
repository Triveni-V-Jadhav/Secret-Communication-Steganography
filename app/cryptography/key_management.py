import os
import secrets
from app.cryptography.encryption import CryptoService

class KeyManagementService:
    """
    Manages session ephemeral keys and cryptographic tokens.
    Guarantees secret keys are never persisted unencrypted in databases.
    """
    
    @staticmethod
    def generate_secure_passphrase(length: int = 16) -> str:
        """Generates a cryptographically secure random alphanumeric passphrase."""
        return secrets.token_urlsafe(length)
        
    @staticmethod
    def generate_random_token(nbytes: int = 32) -> str:
        """Generates a secure hex token for ephemeral validation tokens."""
        return secrets.token_hex(nbytes)
