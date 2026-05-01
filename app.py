from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

def conectar():
    return sqlite3.connect("clientes.db")

#PANEL ADMIN
@app.route("/", methods=["GET", "POST"])
def admin():

    saldo = None
    id_cliente = None
    nombre = None
    resultado = None
    historial = []

    if request.method == "POST":

        accion = request.form["accion"]

        conn = conectar()
        cursor = conn.cursor()

        # BUSCAR POR ID O NOMBRE
        if accion == "buscar":
            valor = request.form["id"]

            cursor.execute("""
                SELECT id, nombre, saldo
                FROM clientes
                WHERE id = ? OR nombre LIKE ?
            """, (valor, f"%{valor}%"))

            r = cursor.fetchone()

            if r:
                id_cliente = r[0]
                nombre = r[1]
                saldo = r[2]

                cursor.execute("""
                    SELECT fecha, total, saldo_usado, pagado, bonus
                    FROM historial
                    WHERE cliente_id = ?
                    ORDER BY id DESC
                """, (id_cliente,))
                historial = cursor.fetchall()

        #  GUARDAR NOMBRE
        if accion == "nombre":
            id_cliente = request.form["id"]
            nombre = request.form["nombre"]

            cursor.execute("""
                UPDATE clientes
                SET nombre = ?
                WHERE id = ?
            """, (nombre, id_cliente))

            conn.commit()

        #  PROCESAR PAGO
        if accion == "pagar":

            id_cliente = request.form["id"]
            total = float(request.form["total"])
            usar_saldo = "usar_saldo" in request.form

            cursor.execute("SELECT nombre, saldo FROM clientes WHERE id = ?", (id_cliente,))
            r = cursor.fetchone()

            nombre = r[0]
            saldo_actual = r[1]

            saldo_usado = min(saldo_actual, total) if usar_saldo else 0
            pagado = total - saldo_usado
            bonus = pagado * 0.04

            nuevo_saldo = saldo_actual - saldo_usado + bonus
            fecha = datetime.now().strftime("%d-%m-%Y %H:%M")

            # actualizar saldo
            cursor.execute("""
                UPDATE clientes
                SET saldo = ?
                WHERE id = ?
            """, (nuevo_saldo, id_cliente))

            # guardar historial
            cursor.execute("""
                INSERT INTO historial
                (cliente_id, fecha, total, saldo_usado, pagado, bonus)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (id_cliente, fecha, total, saldo_usado, pagado, bonus))

            conn.commit()

            resultado = {
                "total": total,
                "saldo_usado": saldo_usado,
                "pagado": pagado,
                "bonus": bonus,
                "nuevo_saldo": nuevo_saldo,
                "fecha": fecha
            }

            saldo = nuevo_saldo

            cursor.execute("""
                SELECT fecha, total, saldo_usado, pagado, bonus
                FROM historial
                WHERE cliente_id = ?
                ORDER BY id DESC
            """, (id_cliente,))
            historial = cursor.fetchall()

        conn.close()

    return render_template("admin.html",
                           saldo=saldo,
                           id_cliente=id_cliente,
                           nombre=nombre,
                           resultado=resultado,
                           historial=historial)

# VISTA CLIENTE 
@app.route("/cliente/<id_cliente>")
def cliente(id_cliente):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT nombre, saldo FROM clientes WHERE id = ?", (id_cliente,))
    cliente = cursor.fetchone()

    cursor.execute("""
        SELECT fecha, total, saldo_usado, pagado, bonus
        FROM historial
        WHERE cliente_id = ?
        ORDER BY id DESC
    """, (id_cliente,))
    historial = cursor.fetchall()

    conn.close()

    return render_template("cliente.html",
                           nombre=cliente[0],
                           id_cliente=id_cliente,
                           saldo=cliente[1],
                           historial=historial)

# RUN
if __name__ == "__main__":
    app.run(debug=True)