from flask import Flask


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )

    from .public import public_bp

    app.register_blueprint(public_bp)

    return app


