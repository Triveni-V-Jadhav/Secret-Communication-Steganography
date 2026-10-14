import os
from PIL import Image

class ImageValidator:
    """Validates cover images for multi-image steganography."""
    
    ALLOWED_EXTENSIONS = {".png", ".bmp"}  # Lossless formats only
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB per cover image
    MIN_DIMENSION = 50   # Minimum 50x50 pixels
    MAX_DIMENSION = 8000  # Avoid decompression bomb attacks
    
    @classmethod
    def validate_image_file(cls, filepath: str) -> dict:
        """
        Validates file existence, format, dimensions, channels, and capacity.
        Returns a metadata dictionary or raises ValueError.
        """
        if not os.path.exists(filepath):
            raise ValueError(f"Image file does not exist: {filepath}")
            
        file_size = os.path.getsize(filepath)
        if file_size > cls.MAX_FILE_SIZE:
            raise ValueError(f"Image exceeds maximum allowable file size of {cls.MAX_FILE_SIZE // (1024*1024)}MB.")
            
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".jpg" or ext == ".jpeg":
            raise ValueError(
                "JPEG is a lossy compression format. Discrete Cosine Transform (DCT) and lossy quantization "
                "destroy LSB modifications upon re-encoding or saving. Please provide lossless PNG or BMP images."
            )
        if ext not in cls.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported format '{ext}'. Only lossless PNG or BMP files are accepted.")
            
        try:
            with Image.open(filepath) as img:
                img.verify()  # Check file integrity / corruption
        except Exception as e:
            raise ValueError(f"Image integrity verification failed. Corrupted file: {e}")
            
        # Re-open for inspection after verify() closes the file
        with Image.open(filepath) as img:
            width, height = img.size
            if width < cls.MIN_DIMENSION or height < cls.MIN_DIMENSION:
                raise ValueError(f"Image dimensions ({width}x{height}) are below minimum requirement ({cls.MIN_DIMENSION}x{cls.MIN_DIMENSION}).")
            if width > cls.MAX_DIMENSION or height > cls.MAX_DIMENSION:
                raise ValueError(f"Image dimensions ({width}x{height}) exceed maximum security limits.")
                
            # Convert to RGB mode if palletized or grayscale
            mode = img.mode
            channels = 3 if mode in ("RGB", "RGBA") else 1
            
            # LSB capacity: 1 bit per RGB channel = 3 bits per pixel = (width * height * 3) // 8 bytes
            raw_capacity_bytes = (width * height * 3) // 8
            
            return {
                "valid": True,
                "width": width,
                "height": height,
                "channels": 3,
                "mode": mode,
                "file_size": file_size,
                "capacity_bytes": raw_capacity_bytes
            }
