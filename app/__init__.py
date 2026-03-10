from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp
    from app.routes.request_routes import request_bp
    from app.routes.provider_routes import provider_bp
    

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(request_bp, url_prefix="/api/requests")
    app.register_blueprint(provider_bp, url_prefix="/api/providers")
    
    @app.route("/api/health", methods=["GET"])
    def health_check():
       return {
          "status": "ok",
          "service": "Automobile Breakdown Backend"
        }  


    return app