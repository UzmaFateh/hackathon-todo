"""
Security module for encryption and privacy compliance.
"""
from typing import Optional
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataEncryption:
    """
    Class to handle encryption of sensitive data at rest and in transit.
    """

    def __init__(self, encryption_key: Optional[bytes] = None):
        """
        Initialize the encryption handler.

        Args:
            encryption_key: Encryption key (if not provided, will try to get from environment)
        """
        if encryption_key is None:
            key_env = os.getenv('ENCRYPTION_KEY')
            if key_env:
                # Decode the key from base64 if it's in that format
                try:
                    self.key = base64.urlsafe_b64decode(key_env.encode())
                except Exception:
                    # If it's not base64 encoded, assume it's the raw key
                    self.key = key_env.encode()
            else:
                # Generate a new key (in production, this should be provided)
                logger.warning("No encryption key provided, generating a new one. This should not be done in production!")
                self.key = Fernet.generate_key()
        else:
            self.key = encryption_key

        self.cipher_suite = Fernet(self.key)

    def encrypt_data(self, data: str) -> str:
        """
        Encrypt sensitive data.

        Args:
            data: String data to encrypt

        Returns:
            Encrypted data as base64-encoded string
        """
        try:
            encrypted_bytes = self.cipher_suite.encrypt(data.encode())
            return base64.urlsafe_b64encode(encrypted_bytes).decode()
        except Exception as e:
            logger.error(f"Encryption failed: {str(e)}")
            raise

    def decrypt_data(self, encrypted_data: str) -> str:
        """
        Decrypt sensitive data.

        Args:
            encrypted_data: Base64-encoded encrypted data

        Returns:
            Decrypted string data
        """
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode())
            decrypted_bytes = self.cipher_suite.decrypt(encrypted_bytes)
            return decrypted_bytes.decode()
        except Exception as e:
            logger.error(f"Decryption failed: {str(e)}")
            raise

    @staticmethod
    def generate_encryption_key(password: Optional[str] = None) -> bytes:
        """
        Generate an encryption key from a password or randomly.

        Args:
            password: Password to derive key from (if None, generates random key)

        Returns:
            Generated encryption key
        """
        if password:
            salt = b'salt_32_byte_length_for_production'  # In production, use a proper random salt
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=salt,
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
            return key
        else:
            return Fernet.generate_key()


class PrivacyCompliance:
    """
    Class to handle privacy compliance measures as per NF-006.
    """

    def __init__(self):
        """Initialize privacy compliance measures."""
        self.pii_fields = {'email', 'name', 'password_hash'}
        self.encryption_handler = DataEncryption()

    def anonymize_user_data(self, user_data: dict) -> dict:
        """
        Anonymize user data for non-essential operations.

        Args:
            user_data: Dictionary containing user data

        Returns:
            Anonymized user data
        """
        anonymized = user_data.copy()

        # Replace PII with anonymous identifiers
        for field in self.pii_fields:
            if field in anonymized:
                if field == 'email':
                    anonymized[field] = self._hash_identifier(anonymized[field])
                elif field == 'name':
                    anonymized[field] = 'Anonymous User'
                elif field == 'password_hash':
                    anonymized[field] = '***REDACTED***'

        return anonymized

    def encrypt_sensitive_fields(self, data: dict, fields_to_encrypt: list) -> dict:
        """
        Encrypt specific sensitive fields in a data dictionary.

        Args:
            data: Dictionary containing data
            fields_to_encrypt: List of field names to encrypt

        Returns:
            Dictionary with specified fields encrypted
        """
        encrypted_data = data.copy()

        for field in fields_to_encrypt:
            if field in encrypted_data and encrypted_data[field] is not None:
                try:
                    encrypted_data[field] = self.encryption_handler.encrypt_data(str(encrypted_data[field]))
                except Exception as e:
                    logger.error(f"Failed to encrypt field {field}: {str(e)}")
                    raise

        return encrypted_data

    def decrypt_sensitive_fields(self, data: dict, fields_to_decrypt: list) -> dict:
        """
        Decrypt specific encrypted fields in a data dictionary.

        Args:
            data: Dictionary containing encrypted data
            fields_to_decrypt: List of field names to decrypt

        Returns:
            Dictionary with specified fields decrypted
        """
        decrypted_data = data.copy()

        for field in fields_to_decrypt:
            if field in decrypted_data and decrypted_data[field] is not None:
                try:
                    decrypted_data[field] = self.encryption_handler.decrypt_data(decrypted_data[field])
                except Exception as e:
                    logger.error(f"Failed to decrypt field {field}: {str(e)}")
                    raise

        return decrypted_data

    def ensure_no_unnecessary_pii_storage(self, data: dict) -> dict:
        """
        Remove any unnecessary PII from data before storage.

        Args:
            data: Dictionary containing data to be stored

        Returns:
            Data with unnecessary PII removed
        """
        cleaned_data = data.copy()

        # Remove any fields that shouldn't be stored unnecessarily
        unnecessary_pii = ['full_name', 'address', 'phone', 'ssn', 'credit_card']

        for field in unnecessary_pii:
            if field in cleaned_data:
                del cleaned_data[field]

        return cleaned_data

    def _hash_identifier(self, identifier: str) -> str:
        """
        Create a hash of an identifier for anonymization.

        Args:
            identifier: String identifier to hash

        Returns:
            Hashed identifier
        """
        import hashlib
        return hashlib.sha256(identifier.encode()).hexdigest()[:16]  # First 16 chars for brevity


class SecurityValidator:
    """
    Class to handle security validations and checks.
    """

    @staticmethod
    def validate_user_isolation(user_id: str, requested_resource_user_id: str) -> bool:
        """
        Validate that a user can only access resources that belong to them.

        Args:
            user_id: ID of the authenticated user
            requested_resource_user_id: ID of the user that owns the requested resource

        Returns:
            True if access is valid, False otherwise
        """
        return user_id == requested_resource_user_id

    @staticmethod
    def sanitize_input(user_input: str) -> str:
        """
        Sanitize user input to prevent injection attacks.

        Args:
            user_input: Raw user input

        Returns:
            Sanitized input
        """
        if not user_input:
            return user_input

        # Remove control characters that could be used for injection
        sanitized = ''.join(char for char in user_input if ord(char) >= 32 or char in '\n\r\t')

        # Remove potential SQL injection patterns (basic filtering)
        dangerous_patterns = ['--', ';', '/*', '*/', 'xp_', 'sp_']
        for pattern in dangerous_patterns:
            if pattern.lower() in sanitized.lower():
                # Remove or neutralize the dangerous pattern
                sanitized = sanitized.replace(pattern, '')

        # Prevent basic XSS attempts by removing script tags
        import re
        # Remove script tags (case-insensitive)
        sanitized = re.sub(r'<script[^>]*>.*?</script>', '', sanitized, flags=re.IGNORECASE | re.DOTALL)
        # Remove javascript: urls
        sanitized = re.sub(r'javascript:', '', sanitized, flags=re.IGNORECASE)
        # Remove event handlers (onload, onclick, etc.)
        sanitized = re.sub(r'on\w+\s*=', '', sanitized, flags=re.IGNORECASE)

        return sanitized


# Global instances
privacy_compliance = PrivacyCompliance()
security_validator = SecurityValidator()
encryption_handler = DataEncryption()

# Export for easy import
__all__ = [
    'DataEncryption',
    'PrivacyCompliance',
    'SecurityValidator',
    'privacy_compliance',
    'security_validator',
    'encryption_handler'
]