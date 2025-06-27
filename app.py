from flask import Flask
from models import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the database
db.init_app(app)

### Backend Logic

### /Backend Logic

# Create the database tables if they don't exist
with app.app_context():
    db.create_all()

def main():
    print("Hello from test-therapy-app!")
    app.run(debug=True)

if __name__ == "__main__":
    main()

