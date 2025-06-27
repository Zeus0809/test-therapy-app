# test-therapy-app
A test project for a Flask part-time position at Charleston Children's Therapy Center.

## Responses To Task Questions
1. The app uses client-side validation for empty fields, server-side validation for DOB in the future, and server-side validation for a duplicate patient entry:
 - Empty fields:
    there is a JavaScript function inside form.html that loops over all forms that use a 'needs-validation' class and adds an event listener for the Submit action. When the user clicks 'submit', it validates the form input and shows the error block if it fails, or proceeds with form submission if it succeeds.
 - DOB in the future:
    Inside the submit route method, there is a check whether the user-submitted DOB is greater than today's date. If it is, the server returns the form back with an error message and the input data to put it back in the fields.
 - Duplicate patient:
    Once the server receives patient info, it queries the database to see if there is already a patient with that first name, last name, and DOB. Then if the query result is not None, it also returns the form back with an error preventing a database commit.

2. I would start with drawing the ERD for the database, since Therapist logins would require a second entity - Therapist. One therapist can work with multiple patients (at least that's my assumption), so there would be a one-to-many relationship from Therapist to Patient. I would define a SQL model for Therapist in my models.py, add an FK field to Patient ('therapist_id' or similar) and setup the relationship. Also, if the goal is to create a login system for both patients and therapists, I would create a separate User table to store login credentials, names and things like role and last_login. Then I would relate that User table to both Patient and Therapist as one-to-one, and make sure that role-specific tables only store data unique to the roles (e.g. insurance_info for Patient and hourly_rate for Therapist). That way authentication data and logic would be centralized, making it easier to maintain and extend. There would be no data duplication that way so the database would be normalized. Lastly, I would also think about implementing user sessions and storing them in a separate table to make the app stateful, but that is beyond the scope of the question.

3. I don't have experience with cloud deployment, so it's hard to answer this question directly. Depending on the scale of the app and the number of potential users, a proper cloud provider would need to be chosen. AWS, Google Cloud and Microsoft Azure provide HIPAA-compliant options, but I would need to do some research to see if they are worth it for the use case, or it is enough to use smaller providers. But additional things would definitely need to be implemented, like HTTPS, secure authentication, password policies, database encyption (if not provided by cloud vendor). Also the app.run() call would need to be replaced with a migration process using Flask-Migrate, which I would also need to research. This is more of a DevOps job so I would need to spend more time researching this. In any case, I don't mind the challenge, as long as I understand the goal and the requirements, I can do it.

4. During the initial deployment process, the database schema would be created and migrated onto the cloud using Flask Migrate. For that to work I would need to add the initialization of flask-migrate support at the top of app.py, and remove the 'db.create_all()' line from main(). Later, for every new deployment cycle a new flask migration would be created and run, ensuring that any database schema or code changes are applied without affecting production data.



