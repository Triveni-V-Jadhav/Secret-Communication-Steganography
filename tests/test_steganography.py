import os
import tempfile
import pytest
from PIL import Image
from app.steganography.encoder import StegoEncoder
from app.steganography.decoder import StegoDecoder
from app.steganography.payload_manager import PayloadManager
from app.steganography.image_validation import ImageValidator
from app.cryptography.encryption import CryptoService

@pytest.fixture
def sample_covers():
    temp_dir = tempfile.mkdtemp()
    covers = []
    for i in range(2):
        img_path = os.path.join(temp_dir, f"cover_{i}.png")
        img = Image.new("RGB", (100, 100), color=(50 * (i+1), 80, 120))
        img.save(img_path, format="PNG")
        covers.append(img_path)
    yield covers
    # Cleanup
    for c in covers:
        if os.path.exists(c):
            os.remove(c)

def test_multi_image_encoding_and_decoding(sample_covers):
    secret_text = b"Secret multi-image chunk transmission payload test!"
    passphrase = "StegoPassphrase2026!"
    msg_uuid = "test-uuid-12345678"
    
    # 1. Encrypt
    encrypted_blob = CryptoService.encrypt_payload(secret_text, passphrase)
    
    # 2. Split into 2 chunks
    num_chunks = len(sample_covers)
    frames = PayloadManager.split_payload(encrypted_blob, num_chunks, msg_uuid)
    assert len(frames) == 2
    
    # 3. Embed into 2 images
    stego_paths = []
    for i, (cover_path, frame) in enumerate(zip(sample_covers, frames)):
        stego_path = cover_path.replace(".png", "_stego.png")
        metrics = StegoEncoder.embed_frame_into_image(cover_path, stego_path, frame)
        assert metrics["bytes_embedded"] == len(frame)
        stego_paths.append(stego_path)
        
    # 4. Extract from each stego image
    extracted_chunks = []
    for s_path in stego_paths:
        chunk_dict = StegoDecoder.extract_frame_from_image(s_path)
        extracted_chunks.append(chunk_dict)
        os.remove(s_path)
        
    # 5. Reconstruct ciphertext
    reconstructed_blob = PayloadManager.reconstruct_payload(extracted_chunks)
    assert reconstructed_blob == encrypted_blob
    
    # 6. Decrypt
    decrypted_text = CryptoService.decrypt_payload(reconstructed_blob, passphrase)
    assert decrypted_text == secret_text

def test_missing_image_detection():
    # Only 1 chunk out of 2 passed to reconstructor
    fake_chunk = {
        "chunk_index": 0,
        "total_chunks": 2,
        "chunk_length": 10,
        "total_payload_length": 20,
        "uuid_hash": "abcd",
        "chunk_data": b"1234567890"
    }
    with pytest.raises(ValueError, match="Missing images"):
        PayloadManager.reconstruct_payload([fake_chunk])
