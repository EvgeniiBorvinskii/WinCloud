"""
Cryptography module for WinCloud
Handles encryption/decryption of cloud data
"""
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
import secrets

from common.logger import get_logger

logger = get_logger('CryptoManager')


class CryptoManager:
    """
    Manages encryption and decryption of data
    Uses AES-256-GCM for authenticated encryption
    """
    
    def __init__(self, master_key: bytes = None):
        """
        Initialize crypto manager
        
        Args:
            master_key: Master encryption key (generated if not provided)
        """
        if master_key is None:
            # In production, this should be securely stored/derived
            # For now, generate from machine-specific data
            master_key = self._generate_master_key()
        
        self.master_key = master_key
    
    def _generate_master_key(self) -> bytes:
        """Generate or retrieve master encryption key"""
        key_file = os.path.join(
            os.path.expanduser('~'),
            '.wincloud',
            '.key'
        )
        
        # Try to load existing key
        if os.path.exists(key_file):
            try:
                with open(key_file, 'rb') as f:
                    return f.read()
            except Exception:
                pass
        
        # Generate new key
        key = secrets.token_bytes(32)  # 256 bits
        
        # Save key (in production, use secure key storage)
        try:
            os.makedirs(os.path.dirname(key_file), exist_ok=True)
            with open(key_file, 'wb') as f:
                f.write(key)
            
            # Make file read-only for owner
            if os.name != 'nt':  # Unix-like systems
                os.chmod(key_file, 0o600)
        except Exception as e:
            logger.warning(f"Could not save key to file: {e}")
        
        return key
    
    def encrypt_data(self, data: bytes) -> bytes:
        """
        Encrypt data using AES-256-GCM
        
        Args:
            data: Data to encrypt
        
        Returns:
            Encrypted data with IV and tag prepended
        """
        try:
            # Generate random IV (12 bytes for GCM)
            iv = secrets.token_bytes(12)
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.master_key),
                modes.GCM(iv),
                backend=default_backend()
            )
            
            # Encrypt
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(data) + encryptor.finalize()
            
            # Return: IV (12) + Tag (16) + Ciphertext
            return iv + encryptor.tag + ciphertext
            
        except Exception as e:
            logger.error(f"Encryption failed: {e}", exc_info=True)
            raise
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """
        Decrypt data using AES-256-GCM
        
        Args:
            encrypted_data: Encrypted data with IV and tag
        
        Returns:
            Decrypted data
        """
        try:
            # Extract IV, tag, and ciphertext
            iv = encrypted_data[:12]
            tag = encrypted_data[12:28]
            ciphertext = encrypted_data[28:]
            
            # Create cipher
            cipher = Cipher(
                algorithms.AES(self.master_key),
                modes.GCM(iv, tag),
                backend=default_backend()
            )
            
            # Decrypt
            decryptor = cipher.decryptor()
            plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            return plaintext
            
        except Exception as e:
            logger.error(f"Decryption failed: {e}", exc_info=True)
            raise
    
    def derive_key_from_password(self, password: str, salt: bytes = None) -> tuple:
        """
        Derive encryption key from password using PBKDF2
        
        Args:
            password: User password
            salt: Salt (generated if not provided)
        
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        
        key = kdf.derive(password.encode('utf-8'))
        
        return key, salt
    
    def hash_data(self, data: bytes) -> str:
        """
        Calculate SHA-256 hash of data
        
        Args:
            data: Data to hash
        
        Returns:
            Hex string of hash
        """
        digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
        digest.update(data)
        return digest.finalize().hex()
