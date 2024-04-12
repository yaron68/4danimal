import sqlite3

# Connect to the SQLite database. If it doesn't exist, it will be created.
conn = sqlite3.connect('instance/4danimals.db')

# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Create table Animal
cursor.execute('''
CREATE TABLE Animal (
  id INTEGER PRIMARY KEY,
  name TEXT,
  gender TEXT,
  color TEXT,
  birth_date DATE,
  age REAL,
  species TEXT,
  breed_name TEXT,
  chip_number INTEGER,
  spayed_neutered BOOLEAN,
  arrival DATE,
  foster BOOLEAN,
  current_owner INTEGER,
  Vaccines TEXT
)
''')

# Create table Breeds
cursor.execute('''
CREATE TABLE Breeds (
  breed_name TEXT PRIMARY KEY,
  dangerous_species BOOLEAN
)
''')

# Create table Applicants
cursor.execute('''
CREATE TABLE Applicants (
  id INTEGER PRIMARY KEY,
  full_name TEXT,
  teudat_zehut TEXT,
  address TEXT,
  city TEXT,
  mail TEXT,
  phone TEXT,
  approved BOOLEAN,
  owner_of TEXT
)
''')

# Create table Volunteers
cursor.execute('''
CREATE TABLE Volunteers (
  id INTEGER PRIMARY KEY,
  full_name TEXT,
  teudat_zehut TEXT,
  address TEXT,
  city TEXT,
  mail TEXT,
  phone TEXT,
  job_function TEXT,
  can_be_foster BOOLEAN,
  animal_fostered TEXT
)
''')

# Create table Vaccines
cursor.execute('''
CREATE TABLE Vaccines (
  id INTEGER PRIMARY KEY,
  Vaccine_name TEXT,
  Vaccine_date DATE
)
''')

# Create table Foster_application_form
cursor.execute('''
CREATE TABLE Foster_application_form (
  id INTEGER PRIMARY KEY,
  full_name TEXT,
  phone_number TEXT,
  address TEXT,
  email TEXT,
  foster_dog BOOLEAN,
  foster_cat BOOLEAN,
  foster_pups BOOLEAN,
  foster_kittens BOOLEAN,
  foster_dog_with_newborns BOOLEAN,
  foster_newborn_kittens BOOLEAN,
  has_car BOOLEAN,
  previous_experience BOOLEAN,
  detailed_experience TEXT,
  other_pets_at_home BOOLEAN,
  detailed_pets_at_home TEXT
)
''')

# Commit the transaction
conn.commit()

# Close the connection
conn.close()

print("Database and tables created successfully.")
