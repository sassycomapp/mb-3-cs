import anvil.users
import anvil.email
# Mybizz CS — Vault Service
# Phase 0 Implementation — TODO 1

import anvil
from anvil.tables import app_tables
from .exceptions import (
    VaultError,
    VaultSecretNotFoundError,
    VaultDecryptionError,
)
from .encryption_service import encrypt, decrypt

def get_vault_secret(secret_name):
    """
    Retrieve a secret from the Vault table.
    
    Args:
        secret_name: The name of the secret (e.g., 'stripe_secret_key')
    
    Returns:
        str: The decrypted secret value
    
    Raises:
        VaultSecretNotFoundError: If the secret is not configured
        VaultDecryptionError: If decryption fails
    """
    try:
        # Query the vault table
        secret_row = app_tables.vault.find_one(name=secret_name)
        
        if not secret_row:
            # User-friendly error for missing secrets
            raise VaultSecretNotFoundError(
                f"Vault secret '{secret_name}' not configured. "
                "Please contact the business owner."
            )
        
        encrypted_value = secret_row.value
        
        # Decrypt the secret
        decrypted_value = decrypt(encrypted_value)
        return decrypted_value
        
    except VaultSecretNotFoundError:
        # Re-raise our custom errors
        raise
    except VaultDecryptionError:
        # Re-raise our custom errors
        raise
    except Exception as e:
        # Catch-all for any other errors
        import logging
        logging.error(
            "Vault secret retrieval failed",
            secret_name=secret_name,
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise VaultSecretNotFoundError(
            f"Failed to retrieve vault secret. Contact support."
        ) from e

def save_vault_secret(secret_name, secret_value, updated_by_user_id=None):
    """
    Save or update a secret in the Vault table.
    
    Args:
        secret_name: The name of the secret (unique identifier)
        secret_value: The plaintext secret value
        updated_by_user_id: User ID of the person updating the secret
    
    Returns:
        dict: The created/updated vault row
    
    Raises:
        VaultDecryptionError: If encryption fails
    """
    try:
        # Encrypt the secret
        encrypted = encrypt(secret_value)
        
        # Save to vault table
        existing_row = app_tables.vault.find_one(name=secret_name)
        
        if existing_row:
            # Update existing row
            row = app_tables.vault.update_one(
                existing_row,
                value=encrypted,
                updated_by=anvil.users.get_user_by_id(updated_by_user_id) if updated_by_user_id else None
            )
        else:
            # Create new row
            row = app_tables.vault.add_row(
                name=secret_name,
                value=encrypted,
                updated_by=anvil.users.get_user_by_id(updated_by_user_id) if updated_by_user_id else None
            )
        
        return row
        
    except Exception as e:
        import logging
        logging.error(
            "Failed to save vault secret",
            secret_name=secret_name,
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise VaultDecryptionError(f"Failed to save vault secret: {str(e)}") from e

def delete_vault_secret(secret_name, deleted_by_user_id=None):
    """
    Delete a secret from the Vault table.
    
    Args:
        secret_name: The name of the secret to delete
        deleted_by_user_id: User ID of the person deleting the secret
    
    Returns:
        bool: True if deleted, False if not found
    """
    try:
        secret_row = app_tables.vault.find_one(name=secret_name)
        
        if not secret_row:
            return False
        
        app_tables.vault.delete_one(secret_row)
        
        return True
        
    except Exception as e:
        import logging
        logging.error(
            "Failed to delete vault secret",
            secret_name=secret_name,
            error_type=type(e).__name__,
            error_message=str(e)
        )
        raise VaultError(f"Failed to delete vault secret: {str(e)}") from e
