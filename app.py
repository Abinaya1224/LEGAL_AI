from flask import Flask, request, render_template, redirect, url_for, flash, session
from models import db, User, UploadedFile, ExtractedTexts
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer  # Add this import here
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime
from flask import Flask, request, jsonify, send_file ,session, send_file, send_from_directory, current_app, abort, request
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin, current_user
import psycopg2
from werkzeug.utils import secure_filename
import hashlib
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import google.generativeai as genai
from pdfminer.high_level import extract_text
from io import BytesIO
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from gtts import gTTS
import re 
import os
import urllib.parse
import io




# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = '12345'  # Needed for flashing messages

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "signin"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch user by ID


app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://postgres:Solidpro%402024@localhost:5432/legalai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SESSION_COOKIE_NAME'] = 'session_id'  # Default name for session cookies



# Set up the API key (make sure this is valid and properly set in Google Cloud Console)
genai.configure(api_key="AIzaSyB4kcOA9nB661FF8tFcbUtH1Lxbyle7y3A")
model = genai.GenerativeModel("gemini-1.5-flash")


pytesseract.pytesseract.tesseract_cmd = r'C:/Users/rabinaya/AppData/Local/Programs/Tesseract-OCR/tesseract.exe'
 

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}


db.init_app(app) 
migrate = Migrate(app, db) # Bind SQLAlchemy with Flask

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS




# Serializer initialization
def get_serializer():
    return URLSafeTimedSerializer(current_app.secret_key)

def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(app.secret_key)
    return serializer.dumps(email, salt='password-reset-salt')

# Verify the reset token
def verify_reset_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(app.secret_key)
    try:
        email = serializer.loads(token, salt='password-reset-salt', max_age=expiration)
    except Exception:
        return None
    return email

# Create database tables
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return redirect(url_for('signin'))  # Redirect to signin page

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  # Fetch user by ID

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        # Validate required fields (email and password)
        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for('signin'))

        try:
            # Check if user exists
            user = User.query.filter_by(email=email).first()

            if not user:
                flash("Email not registered.", "error")
                return redirect(url_for('signin'))  # Email does not exist

            # Check if the password matches the stored hashed password
            if not user.check_password(password):  # Assuming check_password() verifies hashed passwords
                flash("Incorrect password.", "error")
                return redirect(url_for('signin'))  # Incorrect password

            # Successful login
            session['user_id'] = user.id  # Store user session
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        
        except Exception as e:
            flash("An error occurred while signing in. Please try again later.", "error")
            print(f"Signin error: {e}")  # Debugging purpose

    return render_template("Signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        # Validate required fields
        if not all([name, email, password, confirm_password]):
            flash("All fields are required!", "error")
            return redirect(url_for('signup'))

        # Validate name (only alphabets, spaces allowed between words)
        name_regex = r"^[A-Za-z]+(?:\s[A-Za-z]+)*$"
        if not re.match(name_regex, name):
            flash("Name must contain only alphabets (no numbers or special characters).", "error")
            return redirect(url_for('signup'))

        # Validate email format
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            flash("Invalid email format!", "error")
            return redirect(url_for('signup'))

        # Validate password strength
        password_regex = r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d@$!%*?&]{8,}$"
        if not re.match(password_regex, password):
            flash("Password must be at least 8 characters long, contain at least one letter and one number.", "error")
            return redirect(url_for('signup'))

        # Check if passwords match
        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup'))

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please sign in.", "error")
            return redirect(url_for('signin'))

        try:
            # Save new user
            new_user = User(name=name, email=email)
            new_user.set_password(password)  # Assuming set_password() hashes the password
            db.session.add(new_user)
            db.session.commit()

            # Optionally log the user in after signup
            session['user_id'] = new_user.id

            flash("Account created successfully! ", "success")
            return redirect(url_for('signin'))  

        except Exception as e:
            db.session.rollback()
            flash("An error occurred. Please try again.", "error")

    return render_template('Signup.html')




@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate a reset token
            token = generate_reset_token(email)
            reset_url = url_for('reset_password', token=token, _external=True)
            
            # Direct user to the reset password page (without sending an email)
            return redirect(url_for('reset_password', token=token))
        else:
            flash("No account found with that email.", "error")
        return redirect(url_for('forgot_password'))
    
    return render_template("Forgotpassword.html")






@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    email = verify_reset_token(token)
    if not email:
        flash("The reset link is invalid or has expired.", "error")
        return redirect(url_for('forgot_password'))

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('reset_password', token=token))

        user = User.query.filter_by(email=email).first()
        if user:
            user.set_password(new_password)
            db.session.commit()
            flash("Your password has been reset successfully.", "success")
            return redirect(url_for('signin'))
    
    return render_template("Resetpassword.html", token=token)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('signin'))






@app.route("/dashboard")
def dashboard():
    # Get the current date and format it
    current_date = datetime.now().strftime("%A, %B %d, %Y")

    # Ensure user is logged in
    if 'user_id' not in session:  # Check if user is logged in
        flash("Please sign in to access the dashboard.", "error")
        return redirect(url_for('signin'))  # Redirect to sign-in page

    # Fetch the user from the database based on user_id stored in session
    user = User.query.get(session['user_id'])

    if user:
        name = user.name  # Get the user's name (username) from the database
    else:
        # Handle case where the user is not found (should not happen if user_id is valid)
        name = "Guest"  # Default name if the user is not found

    # Fetch the 4 most recent uploaded files for the logged-in user
    recent_files = UploadedFile.query.filter_by(user_id=user.id).order_by(UploadedFile.uploaded_at.desc()).limit(4).all()

    return render_template("Dashboard.html", current_date=current_date, name=name, recent_files=recent_files)


@app.route('/documents')
def documents():
    # Ensure user is logged in
    if 'user_id' not in session:
        flash("Please sign in to access your documents.", "error")
        return redirect(url_for('signin'))  # Redirect to sign-in page

    # Fetch the user from the database using user_id from the session
    user = User.query.get(session['user_id'])

    # Fetch the last 4 uploaded files (for the card layout)
    recent_files = UploadedFile.query.filter_by(user_id=user.id).order_by(UploadedFile.uploaded_at.desc()).limit(4).all()

    # Fetch all uploaded files (for the list layout)
    all_files = UploadedFile.query.filter_by(user_id=user.id).all()

    # Pass both recent_files and all_files to the template
    return render_template('document.html', recent_files=recent_files, all_files=all_files)




@app.route('/download/<string:file_id>', methods=['GET'])
def download_file(file_id):
    # Retrieve the file from the database using file_id or file_hash
    file = UploadedFile.query.filter_by(file_hash=file_id).first()  # Adjust if necessary
    
    if not file:
        abort(404, description="File not found")
    
    # Convert file data into a readable stream (binary data from database)
    file_data = io.BytesIO(file.content)
    
    # Return the file as an attachment for download
    return send_file(file_data, as_attachment=True, download_name=file.filename)

@app.route('/view/<file_id>')
def view_file(file_id):
    try:
        # Fetch the file from the database using the UUID file_id
        file = UploadedFile.query.filter_by(file_id=file_id).first()
        
        if file:
            return send_file(io.BytesIO(file.content), as_attachment=True, download_name=file.filename)
        else:
            return "File not found", 404
    except ValueError:
        return "Invalid file ID format", 400


@app.route('/ai_chat')
def ai_chat():
    if 'user_id' not in session:  # Check if the user is logged in
        return redirect(url_for('signin'))  # Redirect to sign-in if not logged in
    return render_template('AI Chat.html')


# Helper function to compute file hash
def compute_file_hash(file_data):
    return hashlib.sha256(file_data).hexdigest()

@app.route('/upload', methods=['POST'])
def upload_file():
    # Ensure user is logged in
    if 'user_id' not in session:
        return jsonify({'error': 'User not logged in'}), 400

    # Check if file is provided
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    file_data = file.read()

    # Compute file hash to check for duplicates
    file_hash = compute_file_hash(file_data)
    existing_file = UploadedFile.query.filter_by(file_hash=file_hash).first()

    if existing_file:
        return jsonify({'message': 'File already uploaded', 'file_id': existing_file.file_id}), 200

    # Get the user_id from session (logged-in user)
    user_id = session['user_id']

    # Save file to DB
    new_file = UploadedFile(
        filename=file.filename,
        content=file_data,
        file_hash=file_hash,
        user_id=user_id  # Associate file with the logged-in user
    )
    db.session.add(new_file)
    db.session.commit()

    # Extract text from the uploaded PDF
    extracted_text = None
    if file.filename.endswith('.pdf'):
        extracted_text = extract_text_from_scanned_pdf(file_data)

    if extracted_text:
        # Save the extracted text in the ExtractedTexts table
        new_extracted_text = ExtractedTexts(
            file_id=new_file.file_id,
            filename=file.filename,
            file_hash=file_hash,
            extracted_text=extracted_text
        )
        db.session.add(new_extracted_text)
        db.session.commit()

    # Return file_id in response
    return jsonify({'file_id': new_file.file_id}), 200


# Function to extract text from scanned PDF using Tesseract
def extract_text_from_scanned_pdf(pdf_bytes):
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")  # Use the 'stream' parameter for bytes
        text = ""
        for page in pdf_document:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            custom_config = r'--oem 3 --psm 11'
            text += pytesseract.image_to_string(img, config=custom_config) + "\n"
        pdf_document.close()
        return text
    except Exception as e:
        print(f"Error extracting text from scanned PDF: {e}")
        return None

 
# Function to extract text from scanned PDF using Tesseract
def extract_text_from_scanned_pdf(pdf_bytes):
    try:
        pdf_document = fitz.open(stream=pdf_bytes, filetype="pdf")  # Use the 'stream' parameter for bytes
        text = ""
        for page in pdf_document:
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            custom_config = r'--oem 3 --psm 11'
            text += pytesseract.image_to_string(img, config=custom_config) + "\n"
        pdf_document.close()
        return text
    except Exception as e:
        print(f"Error extracting text from scanned PDF: {e}")
        return None







@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.json.get('message', '').strip()
    file_id = request.json.get('file_id')  # Get file_id from request

    if not user_input:
        return jsonify({
            "response": "Hey there! 😊 Please enter a valid query so I can assist you. 💡"
        }), 400

    if not file_id:
        return jsonify({
            "response": "Hello! 😊 It looks like you haven't uploaded a document yet. "
                        "Please upload a file so I can assist you better. 📄"
        }), 400

    try:
        extracted_text_entry = ExtractedTexts.query.filter_by(file_id=file_id).first()
        if not extracted_text_entry:
            return jsonify({
                "response": "Oops! 😯 I couldn't find the extracted text for this file. "
                            "Could you please try uploading the document again? 📄"
            }), 400

        extracted_text = extracted_text_entry.extracted_text
        query_input = f"User Query: {user_input}\n\nRelevant Document Context:\n{extracted_text[:1000]}..."

        print(f"Sending Query to AI Model: {query_input}")  # Debugging

        try:
            response = model.generate_content(query_input)
            response_text = response.text if response and response.text else "I couldn't find relevant information. 😞"
        except Exception as e:
            response_text = f"Oops! Something went wrong while processing your query: {str(e)} 😔"

        # Add friendly smileys based on the response content
        if "good" in response_text.lower() or "thank" in response_text.lower():
            response_text += " 😊"
        elif "sorry" in response_text.lower() or "error" in response_text.lower():
            response_text += " 😞"
        elif "help" in response_text.lower():
            response_text += " 🤔"
        else:
            response_text += " 😎"

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({
            "response": "Oops! Something unexpected happened. Please try again. 😔"
        }), 500









if __name__ == "__main__":
    app.run(debug=True)
