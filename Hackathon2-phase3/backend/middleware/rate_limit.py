"""
Rate limiting middleware for API protection.
"""
from fastapi import Request, HTTPException, status
from collections import defaultdict
from datetime import datetime, timedelta
import time
import threading
from typing import Dict, Optional


class RateLimiter:
    """
    Simple in-memory rate limiter to protect API endpoints from abuse.
    Note: For production use, consider using Redis or similar for distributed rate limiting.
    """

    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)
        self.lock = threading.Lock()

    def is_allowed(self, identifier: str) -> bool:
        """
        Check if a request from the given identifier is allowed.

        Args:
            identifier: A unique identifier for the requester (e.g., IP address, user ID)

        Returns:
            True if the request is allowed, False otherwise
        """
        with self.lock:
            now = datetime.utcnow()
            # Remove requests older than 1 minute
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if now - req_time < timedelta(minutes=1)
            ]

            # Check if we've exceeded the limit
            if len(self.requests[identifier]) >= self.requests_per_minute:
                return False

            # Add current request
            self.requests[identifier].append(now)
            return True


# Global rate limiter instance
rate_limiter = RateLimiter(requests_per_minute=60)


def check_rate_limit(request: Request) -> None:
    """
    Check if a request is within rate limits.

    Args:
        request: The incoming request

    Raises:
        HTTPException: If rate limit is exceeded
    """
    # Use a combination of IP address and user ID if available
    client_ip = request.headers.get('x-forwarded-for') or getattr(request.client, 'host', 'unknown')

    # Ensure client_ip is a string
    if isinstance(client_ip, list):
        client_ip = client_ip[0] if client_ip else 'unknown'

    # Try to get user ID from path parameters or headers
    user_id = None

    # Check path parameters for user_id
    if hasattr(request, 'path_params'):
        user_id = request.path_params.get('user_id')

    # If no user_id in path, try to extract from headers
    if not user_id:
        auth_header = request.headers.get('authorization', '')
        # In a real implementation, you'd decode the JWT to get user_id
        # For now, we'll just use the IP as the identifier
        identifier = str(client_ip) if client_ip else 'unknown'
    else:
        identifier = f"{user_id}"

    if not rate_limiter.is_allowed(identifier):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please slow down your requests."
        )


# Alternative decorator approach for specific endpoints
def rate_limit_decorator(requests_per_minute: int = 60):
    """
    Decorator to add rate limiting to specific endpoints.

    Args:
        requests_per_minute: Number of requests allowed per minute
    """
    local_limiter = RateLimiter(requests_per_minute)

    def decorator(func):
        def wrapper(*args, **kwargs):
            # Extract identifier from arguments (this would need to be adapted based on how the function is called)
            request = kwargs.get('request') or (args[0] if args else None)

            if isinstance(request, Request):
                client_ip = request.headers.get('x-forwarded-for', request.client.host)
                identifier = client_ip  # Simplified identification

                if not local_limiter.is_allowed(identifier):
                    raise HTTPException(
                        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        detail="Rate limit exceeded. Please slow down your requests."
                    )

            return func(*args, **kwargs)
        return wrapper
    return decorator