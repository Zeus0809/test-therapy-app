from flask import Flask, render_template, request, redirect, url_for
from models import db, Patient
from datetime import datetime
import os

# Set instance path to /data where we have write permissions
app = Flask(__name__, instance_path='/data')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////data/patients.db'  # Absolute path
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
    
        # The query using explicit filter to handle date comparison
        existing_patient = Patient.query.filter_by(
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        ).first()
        
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
    print("Starting test-therapy-app...")
    
    # # Debug: Check directory permissions and existence
    # print(f"Current working directory: {os.getcwd()}")
    # print(f"Current user: {os.getenv('USER', 'unknown')}")
    # print(f"/data exists: {os.path.exists('/data')}")
    # print(f"/data is writable: {os.access('/data', os.W_OK)}")
    
    # try:
    #     # List contents of /data directory
    #     if os.path.exists('/data'):
    #         print(f"/data contents: {os.listdir('/data')}")
    # except Exception as e:
    #     print(f"Error listing /data: {e}")
    
    # Create the database tables if they don't exist
    with app.app_context():
        # Ensure the data directory exists
        # try:
        #     os.makedirs("/data", exist_ok=True)
        #     print("Successfully ensured /data directory exists")
            
        #     # Try to create a test file to verify write permissions
        #     test_file = "/data/test_write.txt"
        #     with open(test_file, 'w') as f:
        #         f.write("test")
        #     os.remove(test_file)
        #     print("Write test successful")
            
            db.create_all()
            # print("Database tables created successfully")
        # except Exception as e:
        #     print(f"Error during database setup: {e}")
        #     raise
    
    # Get the port from environment or use 8080 as default
    port = int(os.environ.get("PORT", 8080))
    
    # Run the app with the correct host and port for production
    app.run(host='0.0.0.0', port=port)

if __name__ == "__main__":
    main()
else:
    # When running in production (not as main), still initialize the database
    with app.app_context():
        os.makedirs("/data", exist_ok=True)
        db.create_all()

