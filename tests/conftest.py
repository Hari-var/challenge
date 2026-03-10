"""
Pytest configuration and shared fixtures
"""
import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_database():
    """Provide a mock database session"""
    db_mock = MagicMock()
    return db_mock


@pytest.fixture
def mock_user():
    """Provide a mock user object"""
    user_mock = MagicMock()
    user_mock.id = 1
    user_mock.username = "test_user"
    user_mock.email = "test@example.com"
    return user_mock


@pytest.fixture
def mock_policy():
    """Provide a mock policy object"""
    policy_mock = MagicMock()
    policy_mock.id = 1
    policy_mock.policy_number = "POL-2026-001"
    policy_mock.status = "active"
    return policy_mock


@pytest.fixture
def mock_claim():
    """Provide a mock claim object"""
    claim_mock = MagicMock()
    claim_mock.id = 1
    claim_mock.claim_number = "CLM-2026-001"
    claim_mock.status = "pending"
    return claim_mock


@pytest.fixture
def mock_vehicle():
    """Provide a mock vehicle object"""
    vehicle_mock = MagicMock()
    vehicle_mock.id = 1
    vehicle_mock.make = "Toyota"
    vehicle_mock.model = "Camry"
    vehicle_mock.year = 2020
    return vehicle_mock
