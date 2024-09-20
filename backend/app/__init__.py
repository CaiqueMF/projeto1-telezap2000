from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from .config import Config
from .models import iniciar_db,db
jwt = JWTManager()
blacklist = set()
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)
    jwt = JWTManager(app)
    db.init_app(app)

    with app.app_context():
        iniciar_db()

    from .routes import main
    app.register_blueprint(main)

    return app