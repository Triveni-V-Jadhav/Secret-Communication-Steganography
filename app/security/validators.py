import os
import re
from werkzeug.utils import secure_filename

class SecurityValidator:
    """Security validation against path traversal, malicious filenames, and invalid patterns."""
    
    ALLOWED_EXTENSIONS = {"png", "bmp", "txt", "pdf"}
    
    @classmethod
    def sanitize_upload_filename(cls, filename: str) -> str:
        clean = secure_filename(filename)
        if not clean:
            clean = "upload.dat"
        return clean
        
    @classmethod
    def is_allowed_extension(cls, filename: str) -> bool:
        return "." in filename and filename.rsplit(".", 1)[1].lower() in cls.ALLOWED_EXTENSIONS
        
    @staticmethod
    def prevent_path_traversal(base_directory: str, filepath: str) -> bool:
        """Verifies that resolved filepath is strictly inside base_directory."""
        base = os.path.abspath(base_directory)
        target = os.path.abspath(filepath)
        return target.startswith(base)
