from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)

def fila_a_diccionario(cursor,fila):
    columnas = [columna[0] for columna in cursor.description]
    return dict(zip(columnas,fila))

#GET: consultar todos los alumnos
@alumnos_bp.route('',methods=['GET'])
def lista_alumno():
    cursor=None

    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT matricula, nombre, aPaterno, aMaterno, correo
            FROM alumnos
            """)

            datos= cursor.fetchall()
            alumnos = [
                fila_a_diccionario(cursor,fila)
                for fila in datos
            ]
            return jsonify({
                'alumnos': alumnos,
                'mensaje':'Lista de alumnos',
                'exito':True
            }),200

        except Exception:
            return jsonify({
                'mensaje':'Error al consultar los alumnos',
                'exito': False
            }),500

        finally:
            if cursor is not None:
                cursor.close()