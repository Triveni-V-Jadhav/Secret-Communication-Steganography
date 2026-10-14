import os
import hashlib
from typing import List, Dict

class IntegrityService:
    """Verifies file hashes and package consistency."""
    
    @staticmethod
    def get_file_sha256(filepath: str) -> str:
        h = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return h.hexdigest()
        
    @staticmethod
    def verify_chunk_integrity(unpacked_chunk: Dict) -> bool:
        """Verifies that chunk_data length matches header declarations."""
        return len(unpacked_chunk["chunk_data"]) == unpacked_chunk["chunk_length"]
