import pytest
import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import TestConfig
from app import create_app
from src.models import db as _db, DevelopmentGoal
from datetime import date, timedelta

def get_test_db_path():
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    TEST_DATA_DIR = os.path.join(BASE_DIR, "test_data")
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    return os.path.join(TEST_DATA_DIR, "test_development.db")

@pytest.fixture(scope='session')
def app():
    """Create application for the tests."""
    _app = create_app(TestConfig)

    # Create test database and tables
    with _app.app_context():
        _db.create_all()

    yield _app

    # Clean up
    with _app.app_context():
        _db.session.remove()
        _db.drop_all()

@pytest.fixture(scope='function')
def db(app):
    """Create fresh database for each test."""
    with app.app_context():
        _db.session.begin_nested()
        yield _db
        _db.session.rollback()
        _db.session.remove()

@pytest.fixture(autouse=True)
def clean_db(db):
    """Clean test database between tests."""
    yield
    db.session.query(DevelopmentGoal).delete()
    db.session.commit()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def future_date():
    return (date.today() + timedelta(days=7)).strftime('%Y-%m-%d')

@pytest.fixture
def past_date():
    return (date.today() - timedelta(days=7)).strftime('%Y-%m-%d')
