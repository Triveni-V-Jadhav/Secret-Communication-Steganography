import pytest
from app.cryptography.encryption import CryptoService

def test_aes_gcm_encryption_roundtrip():
    secret_text = b"Highly confidential payload that must be protected with AES-256-GCM."
    passphrase = "UltraSecurePassphrase2026!"
    
    # Encrypt
    encrypted_blob = CryptoService.encrypt_payload(secret_text, passphrase)
    assert len(encrypted_blob) > len(secret_text)
    
    # Decrypt with correct passphrase
    decrypted = CryptoService.decrypt_payload(encrypted_blob, passphrase)
    assert decrypted == secret_text

def test_aes_gcm_wrong_passphrase_fails():
    secret_text = b"Secret defense communication."
    passphrase = "CorrectKey123"
    wrong_passphrase = "WrongKey456"
    
    encrypted_blob = CryptoService.encrypt_payload(secret_text, passphrase)
    
    with pytest.raises(ValueError, match="Decryption failed"):
        CryptoService.decrypt_payload(encrypted_blob, wrong_passphrase)

def test_aes_gcm_tamper_detection():
    secret_text = b"Tamper-proof payload verification test."
    passphrase = "IntegrityPassphrase99"
    
    encrypted_blob = bytearray(CryptoService.encrypt_payload(secret_text, passphrase))
    # Flip a single bit in ciphertext
    encrypted_blob[-1] ^= 0x01
    
    with pytest.raises(ValueError, match="Decryption failed"):
        CryptoService.decrypt_payload(bytes(encrypted_blob), passphrase)
