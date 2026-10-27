
from flask import Blueprint, jsonify, request
from database import mysql

admin_bp = Blueprint(
    'administrativos',
    __name__,
    url_prefix='/api/admin'
)


def leer_admin_bd(numempleado):
    cursor = mysql.connection.cursor()

    try:
        sql = """
            SELECT numempleado, nombre, apellidos, telefono, correo, departamento
            FROM administrativos
            WHERE numempleado = %s
        """
        cursor.execute(sql, (numempleado,))
        fila = cursor.fetchone()

        if fila is None:
            return None

        return {
            "numempleado": fila[0],
            "nombre": fila[1],
            "apellidos": fila[2],
            "telefono": fila[3],
            "correo": fila[4],
            "departamento": fila[5]
        }

    finally:
        cursor.close()



@admin_bp.route('', methods=['GET'])
def lista_admin():
    cursor = None

    try:
        cursor = mysql.connection.cursor()
        sql = """
            SELECT numempleado, nombre, apellidos, telefono, correo, departamento
            FROM administrativos
        """
        cursor.execute(sql)
        datos = cursor.fetchall()

        admins = []
        for fila in datos:
            admin = {
                "numempleado": fila[0],
                "nombre": fila[1],
                "apellidos": fila[2],
                "telefono": fila[3],
                "correo": fila[4],
                "departamento": fila[5]
            }
            admins.append(admin)

        return jsonify({
            "admin": admins,
            "mensaje": "Lista de administrativos",
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



@admin_bp.route('/<numempleado>', methods=['GET'])
def obtener_admin(numempleado):
    try:
        admin = leer_admin_bd(numempleado)

        if admin is None:
            return jsonify({
                "admin": None,
                "mensaje": "Administrativo no encontrado",
                "exito": False
            }), 404

        return jsonify({
            "admin": admin,
            "mensaje": "Administrativo encontrado",
            "exito": True
        }), 200

    except Exception as ex:
        return jsonify({
            "mensaje": f"Error: {ex}",
            "exito": False
        }), 500



@admin_bp.route('', methods=['POST'])
def registrar_admin():
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "mensaje": "Debes enviar un objeto JSON valido",
                "exito": False
            }), 400

        campos = [
            "numempleado", "nombre", "apellidos",
            "telefono", "correo", "departamento"
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

        admin = leer_admin_bd(datos["numempleado"])

        if admin is not None:
            return jsonify({
                "mensaje": "El administrativo ya existe, no se puede duplicar",
                "exito": False
            }), 409

        cursor = mysql.connection.cursor()

        sql = """
            INSERT INTO administrativos
            (numempleado, nombre, apellidos, telefono, correo, departamento)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        valores = (
            datos["numempleado"],
            datos["nombre"],
            datos["apellidos"],
            datos["telefono"],
            datos["correo"],
            datos["departamento"]
        )

        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Administrativo registrado correctamente",
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



@admin_bp.route('/<numempleado>', methods=['PUT'])
def actualizar_admin(numempleado):
    cursor = None

    try:
        datos = request.get_json(silent=True)

        if not isinstance(datos, dict):
            return jsonify({
                "mensaje": "Debes enviar un JSON valido",
                "exito": False
            }), 400

        admin = leer_admin_bd(numempleado)

        if admin is None:
            return jsonify({
                "mensaje": "Administrativo no encontrado",
                "exito": False
            }), 404

        campos = [
            "nombre", "apellidos", "telefono",
            "correo", "departamento"
        ]

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
            UPDATE administrativos
            SET nombre = %s,
                apellidos = %s,
                telefono = %s,
                correo = %s,
                departamento = %s
            WHERE numempleado = %s
        """

        valores = (
            datos["nombre"],
            datos["apellidos"],
            datos["telefono"],
            datos["correo"],
            datos["departamento"],
            numempleado
        )

        cursor.execute(sql, valores)
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Administrativo actualizado correctamente",
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



@admin_bp.route('/<numempleado>', methods=['DELETE'])
def eliminar_admin(numempleado):
    cursor = None

    try:
        admin = leer_admin_bd(numempleado)

        if admin is None:
            return jsonify({
                "admin": None,
                "mensaje": "Administrativo no encontrado",
                "exito": False
            }), 404

        cursor = mysql.connection.cursor()
        sql = "DELETE FROM administrativos WHERE numempleado = %s"
        cursor.execute(sql, (numempleado,))
        mysql.connection.commit()

        return jsonify({
            "mensaje": "Administrativo eliminado correctamente",
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
