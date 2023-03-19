from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    doctors = db.relationship('Doctor', backref='user', lazy=True)
    assistants = db.relationship('Assistant', backref='user', lazy=True)
    treatments = db.relationship('Treatment', backref='user', lazy=True)

class Doctor(db.Model):
    __tablename__ = 'doctors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    specialty = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    patients = db.relationship('Patient', backref='doctor', lazy=True)

class Patient(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(200), nullable=False)

    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)

    assistants = db.relationship('Assistant', secondary='patient_assistants', backref='patients', lazy=True)
    treatments = db.relationship('Treatment', backref='patient', lazy=True)

class Assistant(db.Model):
    __tablename__ = 'assistants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class PatientAssistant(db.Model):
    __tablename__ = 'patient_assistants'

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), primary_key=True)
    assistant_id = db.Column(db.Integer, db.ForeignKey('assistants.id'), primary_key=True)

class Treatment(db.Model):
    __tablename__ = 'treatments'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)