# Mybizz CS — Encryption Service
# Phase 0 Implementation — TODO 1

import base64
import hashlib
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import anvil

def encrypt(plaintext):
    """
    Encrypt plaintext using AES-CBC with key from Anvil Secrets.
    
    Args:
        plaintext: The plaintext string to encrypt
    
    Returns:
        str: Base64-encoded encrypted string (IV + ciphertext)
    """
    # Get encryption key from Anvil Secrets
    key = anvil.server.secret('encryption_key')
    key_bytes = hashlib.sha256(key.encode()).digest()
    
    # Generate random IV
    iv = os.urandom(16)
    
    # Pad plaintext to 16-byte boundary
    pad_len = 16 - (len(plaintext) % 16)
    padded = plaintext + (chr(pad_len) * pad_len)
    
    # Encrypt
    cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded.encode()) + encryptor.finalize()
    
    # Encode IV + ciphertext as base64
    encrypted = base64.b64encode(iv + ciphertext).decode()
    
    return encrypted

def decrypt(encrypted):
    """
    Decrypt a base64-encoded encrypted string.
    
    Args:
        encrypted: Base64-encoded encrypted string (IV + ciphertext)
    
    Returns:
        str: Decrypted plaintext
    
    Raises:
        VaultDecryptionError: If decryption fails
    """
    try:
        # Get encryption key from Anvil Secrets
        key = anvil.server.secret('encryption_key')
        key_bytes = hashlib.sha256(key.encode()).digest()
        
        # Decode base64
        encrypted_bytes = base64.b64decode(encrypted)
        
        # Extract IV and ciphertext
        iv = encrypted_bytes[:16]
        ciphertext = encrypted_bytes[16:]
        
        # Decrypt
        cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove padding
        pad_len = padded[-1]
        plaintext = padded[:-pad_len].decode()
        
        return plaintext
        
    except Exception as e:
        raise VaultDecryptionError(f"Failed to decrypt: {str(e)}")
