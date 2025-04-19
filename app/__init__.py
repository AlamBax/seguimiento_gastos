import os
from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from .models import Usuario
from .db import mysql, init_db

load_dotenv()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    init_db(app)
    login_manager.init_app(app)

    from .routes import main
    from .auth import auth
    app.register_blueprint(main)
    app.register_blueprint(auth)

    @login_manager.user_loader
    def load_user(user_id):
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user = cur.fetchone()
        cur.close()
        if user:
            return Usuario(*user)
        return None

    return app