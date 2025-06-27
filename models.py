# Database models (python classes) to map to SQLite tables
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):

    _id = db.Column("patient_id", db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    therapist_name = db.Column(db.String(100), nullable=False)

    def __init__(self, fname, lname, dob, therapist):
        self.first_name = fname
        self.last_name = lname
        self.date_of_birth = dob
        self.therapist_name = therapist


