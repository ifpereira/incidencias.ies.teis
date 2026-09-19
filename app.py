from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/incidencia", methods=["POST"])
def crear_incidencia():

    aula = request.form["aula"]
    usuario = request.form["usuario"]
    descripcion = request.form["descripcion"]

    print("Aula:" + aula)
    print("Usuario:" + usuario)
    print("Descripción:" + descripcion)

    conexion = mysql.connector.connect(
        host="localhost",
        user="incidencias",
        password="incidencias",
        database="incidencias"
    )

    cursor = conexion.cursor()

    sql = """
        INSERT INTO registros
        (aula, usuario, descripcion, estado)
        VALUES (%s, %s, %s, %s)
    """

    valores = (
        aula,
        usuario,
        descripcion,
        "Abierta"
    )

    cursor.execute(sql, valores)

    conexion.commit()

    cursor.close()
    conexion.close()

    return "Incidencia recibida"


if __name__ == "__main__":
    app.run(debug=True)