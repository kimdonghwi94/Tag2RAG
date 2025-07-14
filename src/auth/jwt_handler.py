"""JWT handling utilities."""


def create_token(data: dict) -> str:
    """Create a JWT token from data."""
    raise NotImplementedError


def verify_token(token: str) -> dict:
    """Verify a JWT token and return its payload."""
    raise NotImplementedError
