from flask import Flask
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config

cache = Cache()
limiter = Limiter(key_func=get_remote_address)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    cache.init_app(app)
    limiter.init_app(app)
    
    # Register blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app
