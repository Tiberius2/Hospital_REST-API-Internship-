from flask_restful import Api, Resource, reqparse, fields, marshal_with
from datetime import datetime
from flask_jwt import JWT

api = Api(app)


# Resource fields that we're gonna use marshal_with. Or at least wanted to use
doctor_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'specialty': fields.String
}

patient_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'birthdate': fields.DateTime(dt_format='iso8601'),
    'gender': fields.String,
    'address': fields.String,
    'doctor': fields.Nested(doctor_fields),
    'assistants': fields.List(fields.String),
    'treatments': fields.List(fields.String)
}

assistant_fields = {
    'id': fields.Integer,
    'name': fields.String
}

treatment_fields = {
    'id': fields.Integer,
    'description': fields.String,
    'date': fields.DateTime(dt_format='iso8601'),
    'patient': fields.String,
    'user': fields.String
}

# Request parsers
doctor_parser = reqparse.RequestParser()
doctor_parser.add_argument('name', type=str, required=True)
doctor_parser.add_argument('specialty', type=str, required=True)

patient_parser = reqparse.RequestParser()
patient_parser.add_argument('name', type=str, required=True)
patient_parser.add_argument('birthdate', type=str, required=True)
patient_parser.add_argument('gender', type=str, required=True)
patient_parser.add_argument('address', type=str, required=True)
patient_parser.add_argument('doctor_id', type=int, required=True)

assistant_parser = reqparse.RequestParser()
assistant_parser.add_argument('name', type=str, required=True)

treatment_parser = reqparse.RequestParser()
treatment_parser.add_argument('description', type=str, required=True)
treatment_parser.add_argument('date', type=str, required=True)
treatment_parser.add_argument('patient_id', type=int, required=True)

# Defining the Resources
class DoctorResource(Resource):
    @jwt_required()
    def get(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        return doctor.serialize()

    @jwt_required()
    def put(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        args = doctor_parser.parse_args()
        doctor.name = args['name']
        doctor.specialty = args['specialty']
        db.session.commit()
        return doctor.serialize()


class PatientResource(Resource):
    @jwt_required()
    def get(self, patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return {'message': 'Patient not found'}, 404
        return patient.serialize()
    @jwt_required()
    def put(self, patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return {'message': 'Patient not found'}, 404
        args = patient_parser.parse_args()
        doctor = Doctor.query.get(args['doctor_id'])
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        patient.name = args['name']
        patient.birthdate = datetime.fromisoformat(args['birthdate'])
        patient.gender = args['gender']
        patient.address = args['address']
        patient.doctor = doctor
        db.session.commit()
        return patient.serialize()


class AssistantResource(Resource):
    @jwt_required()
    def get(self, assistant_id):
        assistant = Assistant.query.get(assistant_id)
        if not assistant:
            return {'message': 'Assistant not found'}, 404
        return assistant.serialize()

    @jwt_required()
    def put(self, assistant_id):
        assistant = Assistant.query.get(assistant_id)
        if not assistant:
            return {'message': 'Assistant not found'}, 404
        args = assistant_parser.parse_args()
        assistant.name = args['name']
        db.session.commit()
        return assistant.serialize()


class TreatmentResource(Resource):
    @jwt_required()
    def get(self, treatment_id):
        treatment = Treatment.query.get(treatment_id)
        if not treatment:
            return {'message': 'Treatment not found'}, 404
        return treatment.serialize()
    @jwt_required()
    def_put(self, treatment_id):
        treatment = Treatment.query.get(treatment_id)
        if not treatment:
            return {'message': 'Treatment not found!'}, 404
        args = patient_parser.parse_args()
        patient.name = args['name']
        patient.birthdate = datetime.fromisoformat(args['birthdate'])
        patient.gender = args['gender']
        patient.adress = args['adress']
        doctor = Doctor.query.get(args['doctor_id'])
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        patient.doctor = doctor
        db.session.commit()
        return patient.serialize()


class AssistantResource(Resource):
    @jwt_required()
    def get(self, assistant_id):
        assistant = Assistant.query.get(assistant_id)
        if not assistant:
            return {'message': 'Assistant not found'}, 404
        return assistant.serialize()
    @jwt_required()
    def put(self, assistant_id):
        assistant = Assistant.query.get(assistant_id)
        if not assistant:
            return {'message' : 'Assistant not found'}, 404
        args = assistant_parser.parse_args()
        assistant_name = args['name']
        db.session.commit()
        return assistant.serialize()

class TreatmentResource(Resource):
    @jwt_require()
    def get(self,treatment_id):
        treatment = Treatment.query.get(treatment_id)
        if not treatment:
            return {'message':'Treatent not found'}, 404
        return treatment.serialize()

    @jwt_required()
    def post(self):
        args = treatment_parser.parse_args()
        patient = Patient.query.get(args['patient_id'])
        if not patient:
            return {'message':'Patient not found'}, 404
        user = current_identity
        treatment = Treatment(description=args['description'], date=datetime.fromisoformat(args['date']), patient=patient.name, user=user.username)
        db.session.add(treatment)
        db.session.commit()
        return treatment.serialize()


class DoctorPatientResource(Resource):
    @jwt_required()
    def get(self, doctor_id):
        doctor = Doctor.query.get(doctor_id)
        if not doctor:
            return {'message': 'Doctor not found'}, 404
        patients = [patient.serialize() for patient in doctor.patients]
        return {'doctor' : doctor.serialize(), 'patients': patients}


class GeneralManagerReportResource(Resource):
    @jwt_required()
    def get(self):
        doctors = []
        for doctor in Doctor.query.all():
            patients = [patient.name for patient in doctor.patients]
            doctors.append({'doctor': doctor.name, 'patients':patients})
        treatments = []
        for treatment in Treatment.query.all():
            treatments.append(treatment.serialize())
        return {'doctors': doctors, 'treatments' : treatments}

class PatientReportResource(Resource):
    @jwt_required()
    def get(self, patient_id):
        patient = Patient.query.get(patient_id)
        if not patient:
            return {'message': 'Patient not found'}, 404
        treatments = [treatments.serialize() for treatment in patient.treatments]
        return {'patient': patient.name, 'treatments' : treatments}

# adding the resources to the API
api.add_resource(DoctorResource, '/doctors/<int:doctor_id>')
api.add_resource(PatientResource, '/patients/<int:patient_id>')
api.add_resource(AssistantResource, '/assistants/<int:assistant_id>')
api.add_resource(TreatmentResource, '/treatments/<int:treatment_id>')
api.add_resource(DoctorPatientResource, '/doctors/<int:doctor_id>/patients')
api.add_resource(GeneralManagerReportResource, '/reports/general')
api.add_resource(PatientReportResource, '/reports/patient/<int:patient_id>')


# AUTHENTICATION PART

# app.config['JWT_SECRET_KEY'] = 'password'
# app.config['JWT_EXPIRATION_DELTA'] = timedelta(days=1)

# jwt = JWT(app, autheticate, identity)
