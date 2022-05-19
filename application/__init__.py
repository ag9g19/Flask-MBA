from flask import Flask

from application.dash.userData import init_dashboard2


def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.secret_key = "hello"
    app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024
    app.config["UPLOAD_EXTENSIONS"] = [".csv"]

    with app.app_context():
        # import parts of core Flask app
        from application import routes

        # import Dash Application
        from .dash.dashboard import init_dashboard
        from .dash.userData import init_dashboard2

        app = init_dashboard(app)
        app2 = init_dashboard2(app)

        return app, app2
