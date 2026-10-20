
from flask import Flask, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

app = Flask(__name__)

# Configuración de la aplicación
app.config.from_object(config['development'])

# Inicializar extensiones
CORS(app)
con = MySQL(app)


@app.route("/alumnos", methods=['GET'])
def lista_alumno():
    try:
        cursor = con.connection.cursor()

        sql = "SELECT * FROM alumnos"
        cursor.execute(sql)

        datos = cursor.fetchall()

        alumnos = []

        for fila in datos:
            alumno = {
                "matricula": fila[0],
                "nombre": fila[1],
                "aPaterno": fila[2],
                "aMaterno": fila[3],
                "correo": fila[4]
            }

            alumnos.append(alumno)

        return jsonify({
            'alumnos': alumnos,
            'mensaje': 'Lista de alumnos',
            'exito': True
        })

    except Exception as ex:
        return jsonify({
            'mensaje': f'Error: {ex}',
            'exito': False
        }), 500


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


if __name__ == "__main__":
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5000, debug=True)
