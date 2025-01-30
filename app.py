from flask import Flask, request, render_template, redirect, url_for, flash, session
from models import db, User, UploadedFile, ExtractedTexts
from flask_migrate import Migrate
from itsdangerous import URLSafeTimedSerializer  # Add this import here
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app
from datetime import datetime
from flask import Flask, request, jsonify, send_file ,session
import psycopg2
from werkzeug.utils import secure_filename
import uuid
import hashlib
import os
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import google.generativeai as genai
from pdfminer.high_level import extract_text
from io import BytesIO
import fitz  # PyMuPDF
import pytesseract
from PIL import Image




# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = '12345'  # Needed for flashing messages

app.config['SQLALCHEMY_DATABASE_URI']  = 'postgresql://postgres:Solidpro%402024@localhost:5432/legalai'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TEMPLATES_AUTO_RELOAD'] = True

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


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Add your login logic here
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            # Store user ID in session
            session['user_id'] = user.id  # Save the user ID in session
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash("Invalid credentials, please try again.", "error")
            return redirect(url_for('signin'))  # Stay on the sign-in page

    return render_template("Signin.html")




@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        terms = request.form.get('terms')

        # Validation
        if not all([name, email, password, confirm_password, terms]):
            flash("All fields are required and you must agree to the terms!", "error")
            return redirect(url_for('signup'))  # Stay on signup page

        if password != confirm_password:
            flash("Passwords do not match!", "error")
            return redirect(url_for('signup'))  # Stay on signup page

        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already registered. Please sign in.", "error")
            return redirect(url_for('signin'))  # Redirect to sign-in page

        # Save new user
        new_user = User(name=name, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash("Account created successfully! Please sign in.", "success")
        return redirect(url_for('signin'))  # Redirect to sign-in page

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






@app.route("/dashboard")
def dashboard():
    # Get the current date and format it
    current_date = datetime.utcnow().strftime("%A, %B %d, %Y")

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

    return render_template("Dashboard.html", current_date=current_date, name=name)

@app.route('/documents')
def documents():
    if 'user_id' not in session:  # Check if the user is logged in
        return redirect(url_for('signin'))  # Redirect to sign-in if not logged in
    return render_template('Document.html')

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
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    file_data = file.read()

    # Compute file hash to check for duplicates
    file_hash = compute_file_hash(file_data)
    existing_file = UploadedFile.query.filter_by(file_hash=file_hash).first()

    if existing_file:
        return jsonify({'message': 'File already uploaded', 'file_id': existing_file.file_id}), 200

    # Save file to DB
    new_file = UploadedFile(
        filename=file.filename,
        content=file_data,
        file_hash=file_hash
    )
    db.session.add(new_file)
    db.session.commit()

    # Store the file_id in the session for later use
    session['file_id'] = new_file.file_id

    # Extract text from the uploaded PDF or scanned image
    extracted_text = None
    if file.filename.endswith('.pdf'):
        extracted_text = extract_text_from_scanned_pdf(file_data)

    if extracted_text:
        # Save the extracted text in the ExtractedTexts table
        new_extracted_text = ExtractedTexts(
            file_id=new_file.file_id,       # Correctly reference the file_id
            filename=file.filename,         # Save the filename
            file_hash=file_hash,            # Use the file_hash for uniqueness
            extracted_text=extracted_text   # Save the extracted text
        )
        db.session.add(new_extracted_text)
        db.session.commit()

    return jsonify({'message': 'File uploaded and processed successfully', 'file_id': new_file.file_id}), 201

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
    if not user_input:
        return jsonify({"response": "Please enter a valid query."}), 400

    file_id = session.get('file_id')
    if not file_id:
        return jsonify({"response": "No document uploaded yet. Please upload a file first."}), 400

    try:
        extracted_text_entry = ExtractedTexts.query.filter_by(file_id=file_id).first()
        if not extracted_text_entry:
            return jsonify({"response": "Extracted text not found. Please upload the document again."}), 400

        extracted_text = extracted_text_entry.extracted_text
        query_input = f"{user_input}\n\nBased on the document content: {extracted_text}"

        print(f"Sending Query to AI Model: {query_input}")  # Debugging line

        try:
            response = model.generate_content(query_input)
           

            response_text = response.text if response and response.text else "I couldn't find relevant information."
        
        except Exception as e:
            response_text = f"Error processing the query: {str(e)}"

        return jsonify({"response": response_text})

    except Exception as e:
        return jsonify({"response": f"An error occurred: {str(e)}"}), 500







if __name__ == "__main__":
    app.run(debug=True)
