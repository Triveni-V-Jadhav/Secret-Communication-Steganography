import numpy as np
from PIL import Image
from app.steganography.image_validation import ImageValidator
from app.steganography.payload_manager import HEADER_SIZE

class StegoEncoder:
    """
    LSB Steganography Encoder for RGB Lossless Images.
    Modifies the least significant bit (LSB) of RGB pixel channels
    to encode arbitrary binary frames.
    """
    
    @staticmethod
    def embed_frame_into_image(cover_image_path: str, output_image_path: str, frame_bytes: bytes) -> dict:
        """
        Embeds frame_bytes into the cover image and saves as lossless PNG.
        Returns a dict of metrics (capacity, embedded bytes, utilization).
        """
        validation = ImageValidator.validate_image_file(cover_image_path)
        required_bits = len(frame_bytes) * 8
        available_bits = validation["capacity_bytes"] * 8
        
        if required_bits > available_bits:
            raise ValueError(
                f"Insufficient capacity: Image can hold {validation['capacity_bytes']} bytes, "
                f"but frame requires {len(frame_bytes)} bytes."
            )
            
        img = Image.open(cover_image_path).convert("RGB")
        img_array = np.array(img, dtype=np.uint8)
        
        # Flatten image array
        flat_array = img_array.reshape(-1)
        
        # Convert frame_bytes to bit array
        # e.g., byte b'\x05' -> bits [0, 0, 0, 0, 0, 1, 0, 1]
        bits = np.unpackbits(np.frombuffer(frame_bytes, dtype=np.uint8))
        
        # Modify the least significant bit:
        # Clear LSB (flat_array & ~1), then bitwise OR with bit value
        flat_array[:len(bits)] = (flat_array[:len(bits)] & 0xFE) | bits
        
        # Reshape back to image format and save losslessly
        stego_array = flat_array.reshape(img_array.shape)
        stego_img = Image.fromarray(stego_array, mode="RGB")
        stego_img.save(output_image_path, format="PNG", compress_level=6)
        
        utilization = (len(frame_bytes) / validation["capacity_bytes"]) * 100.0
        
        return {
            "width": validation["width"],
            "height": validation["height"],
            "bytes_capacity": validation["capacity_bytes"],
            "bytes_embedded": len(frame_bytes),
            "utilization_percent": round(utilization, 2),
            "output_path": output_image_path
        }
