from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = "dev-secret-key"

    from website.views import views
    from website.auth import auth

    app.register_blueprint(views)
    app.register_blueprint(auth)

    return app
