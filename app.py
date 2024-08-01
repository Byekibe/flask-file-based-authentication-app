from flask import Flask, render_template, request, redirect, url_for, flash
import csv
import re
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

FILE_PATH = 'user_data.csv'

def initialize_file():
    """Create the CSV file if it does not exist."""
    if not os.path.isfile(FILE_PATH):
        with open(FILE_PATH, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['email', 'password'])  # Optional header row

def is_valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email)

def is_valid_password(password):
    return len(password) > 8

def save_user(email, password):
    with open(FILE_PATH, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, password])

def is_user_exists(email):
    with open(FILE_PATH, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == email:
                return True
    return False

def authenticate_user(email, password):
    try:
        with open(FILE_PATH, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email and row[1] == password:
                    return True
        return False
    except FileNotFoundError:
        print("User data file not found")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

# Replace @app.before_first_request with this
_initialization_has_run = False

@app.before_request
def setup():
    global _initialization_has_run
    if not _initialization_has_run:
        """Initialize the CSV file before the first request."""
        initialize_file()
        _initialization_has_run = True

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if not email or not password:
            flash("Fields cannot be empty.", "danger")
        elif not is_valid_email(email):
            flash("Invalid email address.", "danger")
        elif not is_valid_password(password):
            flash("Password must be more than 8 characters.", "danger")
        elif is_user_exists(email):
            flash("Email already registered.", "danger")
        else:
            save_user(email, password)
            flash("Registration successful! Please log in.", "success")
            return redirect(url_for('login'))
        return redirect(url_for('register'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if authenticate_user(email, password):
            flash("Login successful!", "success")
            return redirect(url_for('success'))
        else:
            flash("Invalid email or password.", "danger")
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/success')
def success():
    return render_template("success.html")

if __name__ == '__main__':
    app.run(debug=True, port=7000)