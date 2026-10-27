
from flask import Blueprint, jsonify, request
from database import mysql

alumnos_bp = Blueprint(
    'alumnos',
    __name__,
    url_prefix='/api/alumnos'
)


def leer_alumno_bd(matricula):
    cursor = mysql.connection.cursor()

    try:
        sql = """
            SELECT matricula, nombre, aPaterno, aMaterno, correo
            FROM alumnos
            WHERE matricula = %s
        """
        cursor.execute(sql, (matricula,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        return {
            "matricula": fila[0],
            "nombre": fila[1],
            "aPaterno": fila[2],
            "aMaterno": fila[3],
            "correo": fila[4]
        }

    finally:
        cursor.close()



@alumnos_bp.route('', methods=['GET'])
def lista_alumno():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT matricula, nombre, aPaterno, aMaterno, correo
            FROM alumnos
        """
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
            "alumnos": alumnos,
            "mensaje": "Lista de alumnos",
            "exito": True
        }), 200

    except Exception as ex:
        return jsonify({
            "mensaje": f"Error: {ex}",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()



@alumnos_bp.route('/<mat>', methods=['GET'])
def obtener_alumno(mat):
    try:
        alumno = leer_alumno_bd(mat)

        if alumno is None:
            return jsonify({
                "alumno": None,
                "mensaje": "Alumno no encontrado",
                "exito": False
            }), 404

        return jsonify({
            "alumno": alumno,
            "mensaje": "Alumno encontrado",
            "exito": True
        }), 200

    except Exception as ex:
        return jsonify({
            "mensaje": f"Error: {ex}",
            "exito": False
        }), 500



@alumnos_bp.route('', methods=['POST'])
def registrar_alumno():
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "mensaje": "Debes enviar un objeto JSON valido",
                "exito": False
            }), 400

        campos = [
            "matricula", "nombre", "aPaterno",
            "aMaterno", "correo"
        ]

        faltantes = [
            campo for campo in campos
            if campo not in datos
            or datos[campo] is None
            or datos[campo] == ""
        ]

        if faltantes:
            return jsonify({
                "mensaje": "Faltan campos obligatorios",
                "campos": faltantes,
                "exito": False
            }), 400

        alumno = leer_alumno_bd(datos["matricula"])

        if alumno is not None:
            return jsonify({
                "mensaje": "El alumno ya existe, no se puede duplicar",
                "exito": False
            }), 409

        cursor = mysql.connection.cursor()

        sql = """
            INSERT INTO alumnos
            (matricula, nombre, aPaterno, aMaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            datos["matricula"],
            datos["nombre"],
            datos["aPaterno"],
            datos["aMaterno"],
            datos["correo"]
        )

        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Alumno registrado correctamente",
            "exito": True
        }), 201

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            "mensaje": f"Error: {ex}",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()



@alumnos_bp.route('/<mat>', methods=['PUT'])
def actualizar_alumno(mat):
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "mensaje": "Debes enviar un JSON valido",
                "exito": False
            }), 400

        alumno = leer_alumno_bd(mat)

        if alumno is None:
            return jsonify({
                "mensaje": "Alumno no encontrado",
                "exito": False
            }), 404

        campos = ["nombre", "aPaterno", "aMaterno", "correo"]

        faltantes = [
            campo for campo in campos
            if campo not in datos
            or datos[campo] is None
            or datos[campo] == ""
        ]

        if faltantes:
            return jsonify({
                "mensaje": "Faltan campos para actualizar",
                "campos": faltantes,
                "exito": False
            }), 400

        cursor = mysql.connection.cursor()

        sql = """
            UPDATE alumnos
            SET nombre = %s,
                aPaterno = %s,
                aMaterno = %s,
                correo = %s
            WHERE matricula = %s
        """

        valores = (
            datos["nombre"],
            datos["aPaterno"],
            datos["aMaterno"],
            datos["correo"],
            mat
        )

        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Alumno actualizado correctamente",
            "exito": True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            "mensaje": f"Error: {ex}",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()


@alumnos_bp.route('/<mat>', methods=['DELETE'])
def eliminar_alumno(mat):
    cursor = None

    try:
        alumno = leer_alumno_bd(mat)

        if alumno is None:
            return jsonify({
                "mensaje": "Alumno no encontrado",
                "exito": False
            }), 404

        cursor = mysql.connection.cursor()
        sql = "DELETE FROM alumnos WHERE matricula = %s"
        cursor.execute(sql, (mat,))
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Alumno eliminado correctamente",
            "exito": True
        }), 200

    except Exception as ex:
        mysql.connection.rollback()
        return jsonify({
            "mensaje": f"Error: {ex}",
            "exito": False
        }), 500

    finally:
        if cursor is not None:
            cursor.close()
