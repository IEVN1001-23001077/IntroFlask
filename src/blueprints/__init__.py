from blueprints.alumnos.routes import alumnos_bp
from blueprints.maestros.routes import maestros_bp
from blueprints.administrativos.routes import admin_bp


def registrar_blueprints(app):
    app.register_blueprint(alumnos_bp)
    app.register_blueprint(maestros_bp)
    app.register_blueprint(admin_bp)