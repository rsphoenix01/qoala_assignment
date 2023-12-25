
from flask import Flask, request, send_from_directory, jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import datetime
import os


from security import authenticate, identity

# Resources
from resources.user import Login, User, UserInformation

app = Flask(__name__, static_folder="client/public")
app.secret_key = "secret"
app.config['MONGO_DBNAME'] = 'VISION-API'
app.config['MONGO_URI'] = "mongodb://ahmed:fwm_123456@ds125486.mlab.com:25486/vision_api"

api = Api(app)

# config JWT
app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=365)
app.config['JWT_AUTH_USERNAME_KEY'] = 'email'
jwt = JWTManager(app)


# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists("client/public/" + path):
        return send_from_directory('client/public', path)
    else:
        return send_from_directory('client/public', 'index.html')


#api.add_resource(User, '/user/<string:email>')
api.add_resource(Login, '/api/users/google')
# api.add_resource(Login, '/api/users/google/')


if __name__ == "__main__":
    from db import mongo
    mongo.init_app(app)
    app.run(port=5000, debug=True)
