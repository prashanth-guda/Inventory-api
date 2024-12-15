from flask import Flask
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config
from routes.product_route import product_bp
from auth.auth import auth_bp

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
jwt = JWTManager(app)

app.register_blueprint(product_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
