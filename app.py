from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename

# Load environment variables
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# MongoDB Configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/caryard"
mongo = PyMongo(app)
bcrypt = Bcrypt(app)

# File upload configuration
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Helper function to check allowed file types
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Set Permissions-Policy to prevent unnecessary features causing issues
@app.after_request
def add_headers(response):
    # Disable or restrict unnecessary features
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=()'
    return response

# Routes

# Home Page
@app.route('/')
def home():
    cars = mongo.db.cars.find()
    return render_template("index.html", cars=cars)

# Admin Registration
@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        if mongo.db.admins.find_one({"username": username}) or mongo.db.admins.find_one({"email": email}):
            flash("Username or email already exists.", "danger")
            return redirect(url_for('admin_register'))
        
        mongo.db.admins.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        })
        flash("Admin registered successfully!", "success")
        return redirect(url_for('admin_login'))
    
    return render_template("admin_register.html")

# Admin Login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = mongo.db.admins.find_one({"username": username})
        
        if admin and bcrypt.check_password_hash(admin['password'], password):
            session['admin'] = str(admin['_id'])
            flash("Login successful!", "success")
            return redirect(url_for('admin_dashboard'))
        
        flash("Invalid username or password", "danger")
    
    return render_template("admin_login.html")

# Admin Dashboard
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin' not in session:
        flash("Please log in as an admin to access the dashboard.", "warning")
        return redirect(url_for('admin_login'))
    
    cars = mongo.db.cars.find()
    return render_template("admin_dashboard.html", cars=cars)

# Add Car
@app.route('/admin/add_car', methods=['POST'])
def add_car():
    if 'admin' not in session:
        flash("Unauthorized access", "danger")
        return redirect(url_for('admin_login'))
    
    image_file = request.files.get('image')
    
    # Check for valid image file
    if image_file and allowed_file(image_file.filename):
        filename = secure_filename(image_file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image_file.save(file_path)
        image_url = url_for('static', filename=f'uploads/{filename}')
    else:
        flash("Please upload a valid image file.", "danger")
        return redirect(url_for('admin_dashboard'))
    
    car = {
        "make": request.form['make'],
        "model": request.form['model'],
        "year": request.form['year'],
        "description": request.form['description'],
        "price": request.form['price'],
        "image_url": image_url
    }
    mongo.db.cars.insert_one(car)
    flash("Car added successfully!", "success")
    return redirect(url_for('admin_dashboard'))

# Edit Car
@app.route('/admin/edit_car/<car_id>', methods=['GET', 'POST'])
def edit_car(car_id):
    if 'admin' not in session:
        flash("Unauthorized access", "danger")
        return redirect(url_for('admin_login'))
    
    car = mongo.db.cars.find_one({"_id": ObjectId(car_id)})
    
    if request.method == 'POST':
        image_file = request.files.get('image')
        image_url = car.get("image_url")

        # Check if a new image file is uploaded
        if image_file and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(file_path)
            image_url = url_for('static', filename=f'uploads/{filename}')
        
        updated_car = {
            "make": request.form['make'],
            "model": request.form['model'],
            "year": request.form['year'],
            "description": request.form['description'],
            "price": request.form['price'],
            "image_url": image_url
        }
        mongo.db.cars.update_one({"_id": ObjectId(car_id)}, {"$set": updated_car})
        flash("Car updated successfully!", "success")
        return redirect(url_for('admin_dashboard'))
    
    return render_template("edit_car.html", car=car)

# Delete Car
@app.route('/admin/delete_car/<car_id>', methods=['POST'])
def delete_car(car_id):
    if 'admin' not in session:
        flash("Unauthorized access", "danger")
        return redirect(url_for('admin_login'))
    
    mongo.db.cars.delete_one({"_id": ObjectId(car_id)})
    flash("Car deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
