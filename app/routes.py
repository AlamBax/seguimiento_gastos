import json
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .db import mysql

main = Blueprint('main', __name__)

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/dashboard")
@login_required
def dashboard():
    cur = mysql.connection.cursor()
    
    cur.execute("""
        SELECT tipo, categoria, monto, fecha 
        FROM movimientos
        WHERE usuario_id = %s 
        ORDER BY fecha DESC
    """, (current_user.id,))
    movimientos = cur.fetchall()

    cur.execute("""
        SELECT tipo, categoria, SUM(monto)
        FROM movimientos
        WHERE usuario_id = %s
        GROUP BY tipo, categoria
    """, (current_user.id,))
    resumen = cur.fetchall()

    cur.close()

    movimientos = [
        {"tipo": m[0], "categoria": m[1], "monto": m[2], "fecha": m[3].strftime("%Y-%m-%d %H:%M")}
        for m in movimientos
    ]
    resumen_dict = []
    for r in resumen:
        resumen_dict.append({
            "tipo": r[0],
            "categoria": r[1],
            "total": float(r[2])
        })

    categorias = {}
    for item in resumen_dict:
        key = f"{item['tipo']}_{item['categoria']}"
        categorias[key] = item['total']

    return render_template(
        "dashboard.html", 
        usuario=current_user.nombre, 
        movimientos=movimientos,
        resumen=resumen_dict,
        chart_data=json.dumps(categorias)
    )

@main.route("/agregar", methods=["POST"])
@login_required
def agregar():
    tipo = request.form["tipo"]
    categoria = request.form["categoria"]
    monto = request.form["monto"]

    if not tipo or not categoria or not monto:
        flash("Todos los campos son obligatorios.")
        return redirect(url_for("main.dashboard"))

    if tipo not in ['ingreso', 'egreso']:
        flash("Tipo no válido.")
        return redirect(url_for("main.dashboard"))

    try:
        monto = float(monto)
    except ValueError:
        flash("Monto inválido.")
        return redirect(url_for("main.dashboard"))

    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO movimientos (usuario_id, tipo, categoria, monto)
        VALUES (%s, %s, %s, %s)
    """, (current_user.id, tipo, categoria, monto))
    mysql.connection.commit()
    cur.close()

    flash("Movimiento guardado con éxito")
    return redirect(url_for("main.dashboard"))