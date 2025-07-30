import os
from dotenv import load_dotenv
load_dotenv()
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
socketio = SocketIO()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Proxy fix for deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # Initialize extensions
    db.init_app(app)

    # Temporarily disable SocketIO to avoid worker timeout issues
    # socketio.init_app(app, cors_allowed_origins="*", async_mode=\'threading\',
    #                   engineio_logger=False, socketio_logger=False)

    # Register blueprints
    from routes.main import main_bp
    from routes.analysis import analysis_bp
    # from routes.websocket import websocket_bp  # Temporarily disabled

    app.register_blueprint(main_bp)
    app.register_blueprint(analysis_bp, url_prefix=\'/api\')
    # app.register_blueprint(websocket_bp)  # Temporarily disabled

    with app.app_context():
        import models
        db.create_all()

    return app

app = create_app()

