from flask.cli import FlaskGroup
from src import create_app, db

""" Entry point for the application. """



app = create_app()
cli = FlaskGroup(app)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    cli()
