import os
import mimetypes
from flask import Flask, render_template
from whitenoise import WhiteNoise
from .config import Config
from .extensions import db, jwt, migrate
from .utils.logger import setup_logger

# Fix CSS MIME type on some Linux/cloud environments
mimetypes.add_type('text/css', '.css')
mimetypes.add_type('application/javascript', '.js')

def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))

    app = Flask(
        __name__,
        template_folder=os.path.join(base_dir, "templates"),
        static_folder=os.path.join(base_dir, "static")
    )

    app.config.from_object(Config)
    app.logger.info(f"template_folder={app.template_folder}")
    # ensure folder exists on startup
    if not os.path.isdir(app.template_folder):
        app.logger.error("template_folder does not exist")

    @app.route("/")
    def home():
        app.logger.info("home route accessed")
        try:
            rendered = render_template("login.html")
            app.logger.info(f"rendered length: {len(rendered)}")
            return rendered
        except Exception as e:
            app.logger.error(f"error rendering login: {e}")
            return "Template error", 500

    @app.route('/favicon.ico')
    def favicon():
        from flask import send_from_directory
        return send_from_directory(app.static_folder, 'favicon.ico')

    @app.route('/sw.js')
    def service_worker():
        from flask import send_from_directory
        resp = send_from_directory(app.static_folder, 'sw.js')
        resp.headers['Service-Worker-Allowed'] = '/'
        resp.headers['Content-Type'] = 'application/javascript'
        return resp

    @app.route("/dashboard")
    def dashboard():
        app.logger.info("dashboard route accessed")
        try:
            rendered = render_template("dashboard.html")
            app.logger.info(f"dashboard rendered length: {len(rendered)}")
            return rendered
        except Exception as e:
            app.logger.error(f"error rendering dashboard: {e}")
            return "Template error", 500

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # postpone creation of tables until first actual HTTP request; use flag to run once
    init_done = False
    @app.before_request
    def ensure_db():
        nonlocal init_done
        if init_done:
            return
        from .models.user import User
        try:
            db.create_all()
            admin = User.query.filter_by(username="admin").first()
            if not admin:
                app.logger.info("Creating default admin user 'admin'/'admin'")
                admin = User(username="admin", role="admin")
                admin.set_password("admin")
                db.session.add(admin)
                db.session.commit()
        except Exception as e:
            app.logger.error(f"database initialization failed: {e}")
        init_done = True

    setup_logger(app)

    from .routes.auth_routes import auth_bp
    from .routes.process_routes import process_bp
    from .routes.admin_routes import admin_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(process_bp, url_prefix="/api/process")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    # Serve static files with correct MIME types via WhiteNoise
    app.wsgi_app = WhiteNoise(app.wsgi_app, root=os.path.join(base_dir, "static"), prefix="static")

    return app