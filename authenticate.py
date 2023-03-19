from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(user_id)

jwt = JWT(app, authenticate, identity)

@jwt_required()
def protected_route():
    user = current_identity
    # Access control logic here