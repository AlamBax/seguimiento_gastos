from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash

from .models import Usuario
from .db import mysql

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            user_obj = Usuario(*user)
            login_user(user_obj)
            return redirect(url_for("main.dashboard"))
        else:
            flash("Correo o contraseña incorrectos")

    return render_template("login.html")

@auth.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO usuarios (nombre, email, contraseña) VALUES (%s, %s, %s)", (nombre, email, password))
        mysql.connection.commit()
        cur.close()
        flash("Usuario registrado correctamente")
        return redirect(url_for("auth.login"))
    
    return render_template("registro.html")

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))