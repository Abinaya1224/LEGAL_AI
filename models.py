from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        """Encrypt the password."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if the given password matches the stored password."""
        return check_password_hash(self.password_hash, password)
    

class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Primary key, auto-incrementing
    file_id = db.Column(db.String(36), nullable=False, unique=True, default=lambda: str(uuid.uuid4()))  # UUID for file_id
    content = db.Column(db.LargeBinary, nullable=False)  # File content as BYTEA
    uploaded_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)  # Timestamp, defaults to current time
    filename = db.Column(db.String(255), nullable=False)  # Filename
    file_hash = db.Column(db.String(255), nullable=False, unique=True)  # File hash for uniqueness

    def __repr__(self):
        return f"<UploadedFile {self.filename}>"
    
class ExtractedTexts(db.Model):
    __tablename__ = 'extracted_texts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_id = db.Column(db.String(36), db.ForeignKey('uploaded_files.file_id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)  # Ensure this column is added
    file_hash = db.Column(db.String(255), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ExtractedTexts {self.filename}>"




    



