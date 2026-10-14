import os
import numpy as np
from PIL import Image
from app.steganography.payload_manager import PayloadManager, HEADER_SIZE
from app.steganography.image_validation import ImageValidator

class StegoDecoder:
    """
    LSB Steganography Decoder.
    Extracts binary bitstreams from RGB pixels, parses versioned headers,
    and isolates chunk payloads.
    """
    
    @staticmethod
    def extract_frame_from_image(image_path: str) -> dict:
        """
        Extracts and parses a stego frame from a PNG image file.
        Returns the parsed chunk dictionary.
        """
        ImageValidator.validate_image_file(image_path)
        
        img = Image.open(image_path).convert("RGB")
        img_array = np.array(img, dtype=np.uint8)
        flat_array = img_array.reshape(-1)
        
        # Extract LSBs for the initial HEADER_SIZE * 8 bits
        header_bits_count = HEADER_SIZE * 8
        if len(flat_array) < header_bits_count:
            raise ValueError("Image has fewer pixels than required for steganography header.")
            
        header_lsbs = (flat_array[:header_bits_count] & 1).astype(np.uint8)
        header_bytes = np.packbits(header_lsbs).tobytes()
        
        # Peek at header to discover chunk payload length
        try:
            # We unpack partial header to know exact chunk size
            partial_info = PayloadManager.unpack_header(header_bytes)
            chunk_length = partial_info["chunk_length"]
        except Exception as e:
            raise ValueError(f"No valid stego package found in image ({os.path.basename(image_path)}): {e}")
            
        total_frame_len = HEADER_SIZE + chunk_length
        total_bits_count = total_frame_len * 8
        
        if len(flat_array) < total_bits_count:
            raise ValueError(f"Image too small to contain declared chunk size of {chunk_length} bytes.")
            
        full_lsbs = (flat_array[:total_bits_count] & 1).astype(np.uint8)
        full_frame_bytes = np.packbits(full_lsbs).tobytes()
        
        unpacked = PayloadManager.unpack_chunk(full_frame_bytes)
        return unpacked
