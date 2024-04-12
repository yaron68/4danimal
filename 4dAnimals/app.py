from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///4danimals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the SQLAlchemy db instance
db = SQLAlchemy(app)


def convert_txt_to_date(str_date):
    date_format = "%Y-%m-%d"  # Adjust the format if necessary (e.g., "%m/%d/%Y")
    date_obj = datetime.strptime(str_date, date_format)
    convert_date = date_obj.date()
    return convert_date


# Define the Animal model
class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(50), nullable=False)
    birth_date = db.Column(db.Date)
    age = db.Column(db.Float)
    species = db.Column(db.String(50), nullable=False)
    breed_name = db.Column(db.String(100))
    chip_number = db.Column(db.Integer, unique=True)
    spayed_neutered = db.Column(db.Boolean)
    arrival = db.Column(db.Date, default=datetime.utcnow)
    foster = db.Column(db.Boolean)
    current_owner = db.Column(db.Integer)
    vaccines = db.Column(db.String(255))

class Applicants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    Teudat_Zehut = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    city = db.Column(db.String(255))
    mail = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    approved = db.Column(db.Boolean)
    owner_of = db.Column(db.String(255))

class Volunteers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    Teudat_Zehut = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(100))
    city = db.Column(db.String(255))
    mail = db.Column(db.String(255))
    phone = db.Column(db.String(255))
    job_function = db.Column(db.String(255))
    can_be_foster = db.Column(db.Boolean)
    animal_fostered = db.Column(db.String(255))

# Configure the SQLAlchemy part of the app instance
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///4danimals.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/view-volunteers', methods=['GET', 'POST'])
def view_volunteers():
    if request.method == 'GET':
        # Connect to your SQL database
        conn = sqlite3.connect('4danimals.db')
        cur = conn.cursor()

        # Query for available volunteers
        cur.execute("SELECT * FROM Volunteers")
        volunteers = cur.fetchall()

        # Close the connection
        conn.close()

        # Render the HTML page with the volunteers data
        return render_template('view-volunteers.html', volunteers=volunteers) #animals=animals)

    elif request.method == 'POST':
        # Extract filter values from the form
        animal_fostered = request.form.get('animal_fostered')
        city = request.form.get('city')
        can_be_foster = request.form.get('can_be_foster') == '1'

        # Construct query based on filters
        query = Volunteers.query
        if animal_fostered:
            query = query.filter(Volunteers.animal_fostered == animal_fostered)
        if city:
            query = query.filter(Volunteers.city == city)
        if can_be_foster:
            query = query.filter(Volunteers.can_be_foster == '1')
        volunteers = query.all()
    else:
        # If it's a GET request, just display all volunteers initially
        volunteers = Volunteers.query.all()

    return render_template('view-volunteers.html', volunteers=volunteers)

@app.route('/view-animals', methods=['GET', 'POST'])
def view_animals():
    if request.method == 'GET':
        # Connect to your SQL database
        conn = sqlite3.connect('4danimals.db')
        cur = conn.cursor()

        # Query for available animals
        cur.execute("SELECT * FROM Animal")
        animals = cur.fetchall()

        # Close the connection
        conn.close()

        # Render the HTML page with the animals data
        return render_template('view-animals.html', table_name=Animal) #animals=animals)

    elif request.method == 'POST':
        # Extract filter values from the form
        gender = request.form.get('gender')
        age_min = request.form.get('age_min')
        age_max = request.form.get('age_max')
        species = request.form.get('species')
        breed = request.form.get('breed')
        spayed_neutered = request.form.get('spayed_neutered') == '1'

        # Construct query based on filters
        query = Animal.query
        if gender:
            query = query.filter(Animal.gender == gender)
        if age_min:
            query = query.filter(Animal.age >= age_min)
        if age_max:
            query = query.filter(Animal.age <= age_max)
        if species:
            query = query.filter(Animal.species.ilike(f'%{species}%'))
        if breed:
            query = query.filter(Animal.breed.ilike(f'%{breed}%'))
        if spayed_neutered:
            query = query.filter(Animal.spayed_neutered == spayed_neutered)
        animals = query.all()
    else:
        # If it's a GET request, just display all animals initially
        animals = Animal.query.all()

    return render_template('view-animals.html', animals=animals)

@app.route('/view-adopters', methods=['GET', 'POST'])
def view_adopters():
    if request.method == 'GET':
        # Connect to your SQL database
        conn = sqlite3.connect('4danimals.db')
        cur = conn.cursor()

        # Query for available adopters
        cur.execute("SELECT * FROM Applicants")
        applicants = cur.fetchall()

        # Close the connection
        conn.close()

        # Render the HTML page with the adopters data
        return render_template('view-adopters.html', table_name=applicants)

    elif request.method == 'POST':
        # Extract filter values from the form
        owner_of = request.form.get('owner_of')
        city = request.form.get('city')
        approved = request.form.get('approved') == '1'

        # Construct query based on filters
        query = Applicants.query
        if owner_of:
            query = query.filter(Applicants.owner_of == owner_of)
        if city:
            query = query.filter(Applicants.city == city)
        if approved:
            query = query.filter(Applicants.approved == '1')
        applicants = query.all()
    else:
        # If it's a GET request, just display all applicants initially
        applicants = Applicants.query.all()

    return render_template('view-adopters.html', applicants=applicants)

@app.route('/add-animal', methods=['GET', 'POST'])
def add_animal():
    if request.method == 'POST':
        # Create a new Animal instance using the form data
        new_animal = Animal(
            name=request.form['name'],
            gender=request.form['gender'],
            color=request.form['color'] if request.form['color'] else None,
            birth_date= convert_txt_to_date(request.form['birth_date'] if request.form['birth_date'] else None),
            age=request.form['age'] if request.form['age'] else None,
            species=request.form['species'] if request.form['species'] else None,
            breed_name=request.form['breed_name'] if request.form['breed_name'] else None,
            chip_number=request.form['chip_number'] if request.form['chip_number'] else None,
            spayed_neutered=True if request.form.get('spayed_neutered') == 'on' else False,
            # Assuming 'arrival' is auto-set to current date
            arrival=convert_txt_to_date(request.form['arrival']),
            foster=True if request.form.get('foster') == 'on' else False,
            current_owner=request.form['current_owner'] if request.form['current_owner'] else None,
            vaccines=request.form['vaccines'] if request.form['vaccines'] else None
        )

        # Add the new animal to the session and commit it to the database
        db.session.add(new_animal)
        db.session.commit()

        # Redirect to a new URL, or render a template with a success message
        return redirect(url_for('index'))  # Redirect back to the home page or a confirmation page
    elif request.method == 'GET':
        return render_template('add-animal.html')
    # If the request method isn't POST, you might want to redirect or show an error
    return render_template('error.html')  # Render an error template or redirect

@app.route('/add-adopter', methods=['GET', 'POST'])
def add_adopter():
    if request.method == 'POST':
        # Create a new Animal instance using the form data
        new_adopter = Applicants(
            full_name=request.form['full_name'],
            Teudat_Zehut=request.form['Teudat_Zehut'],
            address=request.form['address'] if request.form['address'] else None,
            city=request.form['city'] if request.form['city'] else None,
            mail=request.form['mail'] if request.form['mail'] else None,
            phone=request.form['phone'] if request.form['phone'] else None,
            approved=True if request.form.get('approved') == 'on' else False,
            owner_of=request.form['owner_of'] if request.form['owner_of'] else None
        )

        # Add the new animal to the session and commit it to the database
        db.session.add(new_adopter)
        db.session.commit()

        # Redirect to a new URL, or render a template with a success message
        return redirect(url_for('index'))  # Redirect back to the home page or a confirmation page
    elif request.method == 'GET':
        return render_template('add-adopter.html')
    # If the request method isn't POST, you might want to redirect or show an error
    return render_template('error.html')  # Render an error template or redirect

@app.route('/add-volunteer', methods=['GET', 'POST'])
def new_volunteer():
    if request.method == 'POST':
        # Create a new Animal instance using the form data
        new_volunteer = Volunteers(
            full_name=request.form['full_name'],
            Teudat_Zehut=request.form['Teudat_Zehut'],
            address=request.form['address'] if request.form['address'] else None,
            city=request.form['city'] if request.form['city'] else None,
            mail=request.form['mail'] if request.form['mail'] else None,
            phone=request.form['phone'] if request.form['phone'] else None,
            job_function=request.form['job_function'] if request.form['job_function'] else None,
            can_be_foster=True if request.form.get('can_be_foster') == 'on' else False,
            animal_fostered=request.form['animal_fostered'] if request.form['animal_fostered'] else None
        )

        # Add the new animal to the session and commit it to the database
        db.session.add(new_volunteer)
        db.session.commit()

        # Redirect to a new URL, or render a template with a success message
        return redirect(url_for('index'))  # Redirect back to the home page or a confirmation page
    elif request.method == 'GET':
        return render_template('add-volunteer.html')
    # If the request method isn't POST, you might want to redirect or show an error
    return render_template('error.html')  # Render an error template or redirect

@app.route('/pets-catalog', methods=['GET'])
def pets_catalog():
    return render_template('pets-catalog.html')

@app.route('/about-us', methods=['GET'])
def about_us():
    return render_template('about-us.html')

@app.route('/faqs', methods=['GET'])
def faqs():
    return render_template('faqs.html')

@app.route('/admin', methods=['GET'])
def admin():
    return render_template('admin.html')

@app.route('/admin/get_table_data/<table>', methods=['GET'])
def get_table_data(table):
    # Connect to the SQLite database
    conn = sqlite3.connect('4danimals.db')
    c = conn.cursor()

    # Fetch data from the specified table
    c.execute(f'SELECT * FROM {table}')
    data = c.fetchall()

    # Close the database connection
    conn.close()

    # Convert the data to a list of dictionaries for JSON serialization
    table_data = []
    for row in data:
        table_data.append(dict(zip([column[0] for column in c.description], row)))

    # Return the table data as JSON
    return jsonify(table_data)

USER_DATA = {
    "admin": generate_password_hash("Password123!")}

@app.route('/log-in', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_hash = USER_DATA.get(username)

        if user_hash and check_password_hash(user_hash, password):
            return redirect(url_for('admin'))
        else:
            error = "Invalid username or password"
            return render_template('login.html', error=error)

    elif request.method == 'GET':
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)
