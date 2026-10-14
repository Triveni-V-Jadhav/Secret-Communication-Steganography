import os
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

class CryptoService:
    """
    Cryptographic Service implementing Authenticated AES-GCM-256
    with PBKDF2-HMAC-SHA256 key derivation.
    Guarantees confidentiality, integrity, and authenticity.
    """
    
    SALT_LENGTH = 16    # 128-bit salt
    NONCE_LENGTH = 12   # 96-bit standard AES-GCM nonce
    KEY_LENGTH = 32     # 256-bit AES key
    ITERATIONS = 100_000  # OWASP recommendation for PBKDF2-HMAC-SHA256
    
    @staticmethod
    def derive_key(passphrase: str, salt: bytes) -> bytes:
        """Derives a high-entropy 256-bit symmetric key from a passphrase using PBKDF2."""
        if not passphrase:
            raise ValueError("Passphrase cannot be empty.")
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=CryptoService.KEY_LENGTH,
            salt=salt,
            iterations=CryptoService.ITERATIONS,
        )
        return kdf.derive(passphrase.encode("utf-8"))
        
    @staticmethod
    def encrypt_payload(plaintext_bytes: bytes, passphrase: str, associated_data: bytes = b"") -> bytes:
        """
        Encrypts plaintext bytes using AES-256-GCM.
        Output binary structure:
        [16 bytes SALT] + [12 bytes NONCE] + [Ciphertext + 16 bytes GCM Auth Tag]
        """
        if not plaintext_bytes:
            raise ValueError("Plaintext cannot be empty.")
            
        salt = os.urandom(CryptoService.SALT_LENGTH)
        nonce = os.urandom(CryptoService.NONCE_LENGTH)
        key = CryptoService.derive_key(passphrase, salt)
        
        aesgcm = AESGCM(key)
        # AESGCM automatically appends the 16-byte authentication tag
        ciphertext_and_tag = aesgcm.encrypt(nonce, plaintext_bytes, associated_data)
        
        return salt + nonce + ciphertext_and_tag
        
    @staticmethod
    def decrypt_payload(encrypted_blob: bytes, passphrase: str, associated_data: bytes = b"") -> bytes:
        """
        Decrypts an AES-256-GCM package.
        Validates the authentication tag. If ciphertext, salt, or nonce was tampered with,
        or if the passphrase is incorrect, raises an exception and rejects decryption.
        """
        min_length = CryptoService.SALT_LENGTH + CryptoService.NONCE_LENGTH + 16
        if len(encrypted_blob) < min_length:
            raise ValueError("Invalid encrypted payload: blob length is shorter than cryptographic headers.")
            
        salt = encrypted_blob[:CryptoService.SALT_LENGTH]
        nonce = encrypted_blob[CryptoService.SALT_LENGTH : CryptoService.SALT_LENGTH + CryptoService.NONCE_LENGTH]
        ciphertext_and_tag = encrypted_blob[CryptoService.SALT_LENGTH + CryptoService.NONCE_LENGTH:]
        
        key = CryptoService.derive_key(passphrase, salt)
        aesgcm = AESGCM(key)
        
        try:
            plaintext = aesgcm.decrypt(nonce, ciphertext_and_tag, associated_data)
            return plaintext
        except Exception as e:
            raise ValueError("Decryption failed. Incorrect passphrase or payload has been tampered with.") from e

    @staticmethod
    def compute_sha256(data_bytes: bytes) -> str:
        """Computes the hex SHA-256 digest of arbitrary bytes."""
        return hashlib.sha256(data_bytes).hexdigest()
