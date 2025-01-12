from flask import Flask, render_template
from src.models import db
from src.routes import init_routes
from config import ProductionConfig, TestConfig
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=None):
    app = Flask(__name__,
        template_folder='src/templates',
        static_folder='src/static')

    # Set default config if none provided
    if config_class is None:
        config_class = ProductionConfig
        
    app.config.from_object(config_class)
    
    # Initialize database
    db.init_app(app)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('500.html'), 500

    # Ensure all database tables are created
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            app.logger.error(f"Database initialization error: {e}")
            
    # Initialize routes
    init_routes(app)

    # Logging configuration
    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('Application startup')

    return app

app = create_app(ProductionConfig)

if __name__ == '__main__':
    app.run(debug=True)
