#!venv/bin/python

from app import flask_app


if __name__ == '__main__':
    try:
        flask_app.run()
    except Exception as e:
        raise
    flask_app.clean()
