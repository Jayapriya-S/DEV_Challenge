import os


class Config:
    """Base config."""

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASK_APP = os.getenv("FLASK_APP", "app.py")


class TestConfig(Config):
    """Test configuration."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = os.getenv("TEST_SECRET_KEY", "test-secret-key")
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    """Production configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f'sqlite:///{os.path.join(Config.BASE_DIR, "development_goals.db")}',
    )
    SECRET_KEY = os.getenv("PROD_SECRET_KEY", "production-secret-key")

    WTF_CSRF_ENABLED = True


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URL", "sqlite:///development.db")
    SECRET_KEY = os.getenv("DEV_SECRET_KEY", "dev-secret-key")
