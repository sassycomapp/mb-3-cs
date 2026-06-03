# Mybizz CS — Custom Exception Classes
# Phase 0 Implementation — TODO 1

class VaultError(Exception):
    """Base exception for Vault-related errors."""
    pass

class VaultSecretNotFoundError(VaultError):
    """Raised when a vault secret is not configured."""
    pass

class VaultDecryptionError(VaultError):
    """Raised when vault secret decryption fails."""
    pass
