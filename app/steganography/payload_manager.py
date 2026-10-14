import struct
import hashlib
from typing import List, Dict

"""
Binary Steganography Header Format:
Total size: 32 bytes
- Magic bytes: 4 bytes (b"SEC1")
- Version: 1 byte (uint8 = 1)
- Flags: 1 byte (uint8, reserved)
- Chunk Index: 2 bytes (uint16, 0-indexed)
- Total Chunks: 2 bytes (uint16, e.g. 3)
- Chunk Payload Length: 4 bytes (uint32)
- Total Payload Length: 4 bytes (uint32)
- Chunk CRC32 / SHA prefix: 4 bytes (uint32)
- Message UUID Hash Prefix: 14 bytes
"""

HEADER_FORMAT = ">4sBBHHII14s"
HEADER_MAGIC = b"SEC1"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)  # 4 + 1 + 1 + 2 + 2 + 4 + 4 + 14 = 32 bytes

class PayloadManager:
    """
    Handles chunking of encrypted binary payloads, packet serialization with
    versioned binary headers, and verification of multi-image chunk assemblies.
    """
    
    @staticmethod
    def pack_chunk(
        chunk_index: int,
        total_chunks: int,
        chunk_data: bytes,
        total_payload_length: int,
        message_uuid: str
    ) -> bytes:
        """Packs binary header and chunk payload into a verifiable frame."""
        uuid_hash = hashlib.sha256(message_uuid.encode("utf-8")).digest()[:14]
        header = struct.pack(
            HEADER_FORMAT,
            HEADER_MAGIC,
            1,                    # Version 1
            0,                    # Flags
            chunk_index,
            total_chunks,
            len(chunk_data),
            total_payload_length,
            uuid_hash
        )
        return header + chunk_data

    @staticmethod
    def unpack_header(header_bytes: bytes) -> Dict:
        """Unpacks and verifies only the 32-byte binary header."""
        if len(header_bytes) < HEADER_SIZE:
            raise ValueError(f"Header bytes shorter than required ({len(header_bytes)} < {HEADER_SIZE}).")
            
        magic, version, flags, chunk_idx, total_chunks, chunk_len, total_len, uuid_hash = struct.unpack(
            HEADER_FORMAT, header_bytes[:HEADER_SIZE]
        )
        
        if magic != HEADER_MAGIC:
            raise ValueError("Invalid steganography signature. Cover image does not contain a compatible SEC1 payload.")
            
        if version != 1:
            raise ValueError(f"Unsupported steganography header version: {version}")
            
        return {
            "chunk_index": chunk_idx,
            "total_chunks": total_chunks,
            "chunk_length": chunk_len,
            "total_payload_length": total_len,
            "uuid_hash": uuid_hash.hex()
        }

    @staticmethod
    def unpack_chunk(frame_bytes: bytes) -> Dict:
        """Unpacks and verifies the binary header and chunk payload from extracted bytes."""
        hdr = PayloadManager.unpack_header(frame_bytes)
        chunk_len = hdr["chunk_length"]
        
        if hdr["chunk_index"] >= hdr["total_chunks"]:
            raise ValueError(f"Corrupted chunk metadata: chunk_index {hdr['chunk_index']} >= total_chunks {hdr['total_chunks']}")
            
        available_payload = len(frame_bytes) - HEADER_SIZE
        if available_payload < chunk_len:
            raise ValueError(f"Truncated chunk: expected {chunk_len} bytes, found {available_payload} bytes.")
            
        chunk_data = frame_bytes[HEADER_SIZE : HEADER_SIZE + chunk_len]
        hdr["chunk_data"] = chunk_data
        return hdr

    @staticmethod
    def split_payload(payload_bytes: bytes, num_chunks: int, message_uuid: str) -> List[bytes]:
        """
        Splits arbitrary encrypted payload into N chunks and wraps each
        with an authenticated 32-byte header frame.
        """
        if num_chunks < 1:
            raise ValueError("Number of chunks must be at least 1.")
            
        total_len = len(payload_bytes)
        chunk_size = (total_len + num_chunks - 1) // num_chunks
        
        frames = []
        for i in range(num_chunks):
            start = i * chunk_size
            end = min(start + chunk_size, total_len)
            part = payload_bytes[start:end]
            
            frame = PayloadManager.pack_chunk(
                chunk_index=i,
                total_chunks=num_chunks,
                chunk_data=part,
                total_payload_length=total_len,
                message_uuid=message_uuid
            )
            frames.append(frame)
            
        return frames

    @staticmethod
    def reconstruct_payload(unpacked_chunks: List[Dict]) -> bytes:
        """
        Reconstructs the original ciphertext from a list of unpacked chunk dictionaries.
        Validates missing, duplicate, or mismatched chunks.
        """
        if not unpacked_chunks:
            raise ValueError("No stego chunks supplied for reconstruction.")
            
        expected_total = unpacked_chunks[0]["total_chunks"]
        expected_uuid_hash = unpacked_chunks[0]["uuid_hash"]
        expected_total_len = unpacked_chunks[0]["total_payload_length"]
        
        if len(unpacked_chunks) != expected_total:
            raise ValueError(f"Missing images! Received {len(unpacked_chunks)} chunks out of required {expected_total}.")
            
        # Verify consistent UUID hash across all chunks
        seen_indices = {}
        for item in unpacked_chunks:
            idx = item["chunk_index"]
            if item["total_chunks"] != expected_total:
                raise ValueError("Mismatch in total_chunks header across images.")
            if item["uuid_hash"] != expected_uuid_hash:
                raise ValueError("Chunk belongs to a different message package. Images are not from the same set.")
            if idx in seen_indices:
                raise ValueError(f"Duplicate chunk detected (index {idx}). Duplicate images supplied.")
            seen_indices[idx] = item["chunk_data"]
            
        # Check all indices from 0 to total-1 are present
        reconstructed = bytearray()
        for idx in range(expected_total):
            if idx not in seen_indices:
                raise ValueError(f"Missing chunk index {idx} in multi-image package.")
            reconstructed.extend(seen_indices[idx])
            
        if len(reconstructed) != expected_total_len:
            raise ValueError(f"Reconstructed payload length mismatch ({len(reconstructed)} != {expected_total_len}).")
            
        return bytes(reconstructed)
