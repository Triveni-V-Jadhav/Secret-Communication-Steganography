# Security and Threat Model Document

## 1. Cryptographic Standards
- **Cipher:** AES-256 in Galois/Counter Mode (GCM)
- **Key Derivation:** PBKDF2-HMAC-SHA256 with 100,000 rounds and unique 16-byte random salt per encryption operation.
- **Nonce:** Cryptographically secure 12-byte random IV (`os.urandom`) generated per transmission.
- **Authentication:** 16-byte GCM authentication tag verifies ciphertext integrity prior to decryption.

## 2. Biometric Privacy Protection
- **No Raw Image Storage:** Uploaded facial enrollment photos are processed strictly in RAM; raw face images are discarded immediately after feature extraction.
- **Irreversible Feature Templates:** Stores 128-dimensional spatial-gradient feature vectors.
- **Voluntary Consent:** Explicit opt-in consent is enforced before template creation.
- **Template Revocation:** One-click biometric profile deletion permanently purges templates from database storage.
- **Secondary Factor:** Biometric matching operates as a probabilistic secondary identity assertion and is never the sole factor for authentication.

## 3. Web & SSRF Defense
- **Crawler Guard:** Rejects requests to `localhost`, `127.0.0.1`, loopbacks, RFC-1918 private subnets (`10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`), link-local IPs (`169.254.169.254`), and non-allowlisted domains.
- **Decompression Bomb Defense:** Limits cover image dimensions to $8000 \times 8000$ and max file size to 16 MB.
- **Session Protections:** Cookies flagged with `HttpOnly`, `SameSite=Lax`, and configurable `Secure`.
