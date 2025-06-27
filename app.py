from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient
from datetime import datetime, date

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///patients.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the app with the database
db.init_app(app)

# Add current date to all templates
@app.context_processor
def inject_now():
    return {'now': datetime.now()}

### Backend Logic
@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = datetime.strptime(request.form['date_of_birth'], '%Y-%m-%d').date()
        therapist_name = request.form['therapist_name']
        
        # Validate date of birth isn't in the future
        if date_of_birth > datetime.today().date():
            # Return to form with error message
            return render_template('form.html', 
                                  error="Date of birth cannot be in the future.",
                                  first_name=first_name,
                                  last_name=last_name,
                                  therapist_name=therapist_name)
        
        # Check for existing patient with the same first name, last name, and date of birth
        # Print the parameters we're searching for
        print(f"Searching for: {first_name}, {last_name}, {date_of_birth}")
        
        # Use a more explicit query with debugging
        all_patients = Patient.query.all()
        print(f"Total patients in DB: {len(all_patients)}")
        for p in all_patients:
            print(f"DB Patient: {p.first_name} {p.last_name}, DOB: {p.date_of_birth}")
    
        # The query using explicit filter to handle date comparison
        existing_patient = Patient.query.filter_by(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        ).first()
        
        # Print the result
        print(f"Found matching patient: {existing_patient}")
        
        if existing_patient:
            # Patient already exists, return to form with error
            return render_template('form.html',
                                  error="A patient with this name and date of birth already exists.",
                                  first_name=first_name,
                                  last_name=last_name,
                                  therapist_name=therapist_name)
        
        # Create new patient record
        new_patient = Patient(fname=first_name, lname=last_name, dob=date_of_birth, therapist=therapist_name)
        
        # Add to database
        db.session.add(new_patient)
        db.session.commit()
        
        # Redirect to confirmation page with the patient's ID
        return redirect(url_for('confirmation', patient_id=new_patient._id))

@app.route('/confirmation/<int:patient_id>')
def confirmation(patient_id):
    # Query the database to get the patient with the given ID
    patient = Patient.query.get_or_404(patient_id)
    return render_template('confirmation.html', patient=patient)
### /Backend Logic

def main():
    print("Hello from test-therapy-app!")
    # Create the database tables if they don't exist
    with app.app_context():
        db.create_all()
    app.run(debug=True)

if __name__ == "__main__":
    main()

