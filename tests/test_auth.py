import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from src.web_mcp.auth.jwt_auth import JWTAuthProvider


@pytest.fixture
def jwt_provider():
    return JWTAuthProvider()


def test_jwt_token_creation(jwt_provider):
    """Test JWT token creation."""
    data = {"user_id": "test_user", "role": "admin"}
    token = jwt_provider.create_access_token(data)
    assert token is not None
    assert isinstance(token, str)


def test_jwt_token_verification(jwt_provider):
    """Test JWT token verification."""
    data = {"user_id": "test_user", "role": "admin"}
    token = jwt_provider.create_access_token(data)
    
    payload = jwt_provider.verify_token(token)
    assert payload is not None
    assert payload["user_id"] == "test_user"
    assert payload["role"] == "admin"


def test_jwt_invalid_token(jwt_provider):
    """Test invalid JWT token handling."""
    invalid_token = "invalid.token.here"
    payload = jwt_provider.verify_token(invalid_token)
    assert payload is None


def test_password_hashing(jwt_provider):
    """Test password hashing and verification."""
    password = "test_password_123"
    hashed = jwt_provider.get_password_hash(password)
    
    assert hashed != password
    assert jwt_provider.verify_password(password, hashed)
    assert not jwt_provider.verify_password("wrong_password", hashed)


@pytest.mark.asyncio
async def test_authentication_success(jwt_provider):
    """Test successful authentication."""
    # Mock request with valid token
    class MockRequest:
        def __init__(self, token):
            self.headers = {"Authorization": f"Bearer {token}"}
            self.state = type('obj', (object,), {})()
    
    data = {"user_id": "test_user"}
    token = jwt_provider.create_access_token(data)
    request = MockRequest(token)
    
    result = await jwt_provider.authenticate(request)
    assert result is True
    assert hasattr(request.state, 'user')
    assert request.state.user["user_id"] == "test_user"


@pytest.mark.asyncio
async def test_authentication_failure(jwt_provider):
    """Test authentication failure scenarios."""
    # No Authorization header
    class MockRequestNoAuth:
        def __init__(self):
            self.headers = {}
    
    request = MockRequestNoAuth()
    result = await jwt_provider.authenticate(request)
    assert result is False
    
    # Invalid token format
    class MockRequestInvalidFormat:
        def __init__(self):
            self.headers = {"Authorization": "InvalidFormat token"}
    
    request = MockRequestInvalidFormat()
    result = await jwt_provider.authenticate(request)
    assert result is False
    
    # Invalid token
    class MockRequestInvalidToken:
        def __init__(self):
            self.headers = {"Authorization": "Bearer invalid.token.here"}
    
    request = MockRequestInvalidToken()
    result = await jwt_provider.authenticate(request)
    assert result is False
