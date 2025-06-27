from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


def main():
    print("Hello from test-therapy-app!")


if __name__ == "__main__":
    main()

