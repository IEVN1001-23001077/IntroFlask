
from flask import Blueprint, jsonify, request
from database import mysql

maestros_bp = Blueprint(
    'maestros',
    __name__,
    url_prefix='/api/maestros'
)


def leer_maestro_bd(idmaestro):
    cursor = mysql.connection.cursor()

    try:
        sql = """
            SELECT idmaestro, nombre, aPaterno, aMaterno, correo
            FROM maestros
            WHERE idmaestro = %s
        """
        cursor.execute(sql, (idmaestro,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        return {
            "idmaestro": fila[0],
            "nombre": fila[1],
            "aPaterno": fila[2],
            "aMaterno": fila[3],
            "correo": fila[4]
        }

    finally:
        cursor.close()



@maestros_bp.route('', methods=['GET'])
def lista_maestro():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT idmaestro, nombre, aPaterno, aMaterno, correo
            FROM maestros
        """
        cursor.execute(sql)
        datos = cursor.fetchall()

        maestros = []
        for fila in datos:
            maestro = {
                "idmaestro": fila[0],
                "nombre": fila[1],
                "aPaterno": fila[2],
                "aMaterno": fila[3],
                "correo": fila[4]
            }
            maestros.append(maestro)

        return jsonify({
            "maestros": maestros,
            "mensaje": "Lista de maestros",
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



@maestros_bp.route('/<idmaestro>', methods=['GET'])
def obtener_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro is None:
            return jsonify({
                "maestro": None,
                "mensaje": "Maestro no encontrado",
                "exito": False
            }), 404

        return jsonify({
            "maestro": maestro,
            "mensaje": "Maestro encontrado",
            "exito": True
        }), 200

    except Exception as ex:
        return jsonify({
            "mensaje": f"Error: {ex}",
            "exito": False
        }), 500



@maestros_bp.route('', methods=['POST'])
def registrar_maestro():
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "mensaje": "Debes enviar un objeto JSON valido",
                "exito": False
            }), 400

        campos = [
            "idmaestro", "nombre", "aPaterno",
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

        maestro = leer_maestro_bd(datos["idmaestro"])

        if maestro is not None:
            return jsonify({
                "mensaje": "El maestro ya existe, no se puede duplicar",
                "exito": False
            }), 409

        cursor = mysql.connection.cursor()

        sql = """
            INSERT INTO maestros
            (idmaestro, nombre, aPaterno, aMaterno, correo)
            VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            datos["idmaestro"],
            datos["nombre"],
            datos["aPaterno"],
            datos["aMaterno"],
            datos["correo"]
        )

        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Maestro registrado correctamente",
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



@maestros_bp.route('/<idmaestro>', methods=['PUT'])
def actualizar_maestro(idmaestro):
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "mensaje": "Debes enviar un JSON valido",
                "exito": False
            }), 400

        maestro = leer_maestro_bd(idmaestro)

        if maestro is None:
            return jsonify({
                "mensaje": "Maestro no encontrado",
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
            UPDATE maestros
            SET nombre = %s,
                aPaterno = %s,
                aMaterno = %s,
                correo = %s
            WHERE idmaestro = %s
        """

        valores = (
            datos["nombre"],
            datos["aPaterno"],
            datos["aMaterno"],
            datos["correo"],
            idmaestro
        )

        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Maestro actualizado correctamente",
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



@maestros_bp.route('/<idmaestro>', methods=['DELETE'])
def eliminar_maestro(idmaestro):
    cursor = None

    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro is None:
            return jsonify({
                "mensaje": "Maestro no encontrado",
                "exito": False
            }), 404

        cursor = mysql.connection.cursor()
        sql = "DELETE FROM maestros WHERE idmaestro = %s"
        cursor.execute(sql, (idmaestro,))
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Maestro eliminado correctamente",
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
