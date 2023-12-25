from flask import request, jsonify
from flask_restful import Resource, reqparse
# from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests
import random
import string
import os

from models.user import UserModel
import security


class User(Resource):
    def get(self, email):
        user = UserModel.find_by_email(email)

        if not user:
            return {"success": False, "message": "User not found"}, 404
        return user.json()


class UserInformation(Resource):
    # @jwt_required()
    def get(self, id):

        user = UserModel.find_by_id(id)

        if not user:
            return {"success": False, "message": "User not found"}, 404
        return user.json()


# refrencing the client secret file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']


class Login(Resource):
    @jwt_required
    def get(self):
        # Access the identity of the current user with get_jwt_identity
        current_user = get_jwt_identity()
        return current_user, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('code')
        args = parser.parse_args()

        # check if data were passed
        if args['code'] is None:
            return {
                'success': False,
                'Message': 'Invalid request.'
            }, 400

        # Collect the login data
        code = args['code']

        try:
            # upgrade the authorization code into a credentials object
            oauth_flow = flow_from_clientsecrets(
                'client_secrets.json', scope='')
            oauth_flow.redirect_uri = 'postmessage'
            credentials = oauth_flow.step2_exchange(code)
            access_token = credentials.access_token

        except FlowExchangeError:
            return {
                'Success': False,
                'Message': 'Faild to upgrade the authorization code.'
            }, 401

        # Check that the access token is valid
        url = (
            'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(access_token))
        h = httplib2.Http()
        result = json.loads(h.request(url, 'GET')[1].decode('utf-8'))

        # if there was an error in the access token info, abort
        if result.get('error') is not None:
            return {
                'Sucess': False,
                'Message': result.get('error')
            }, 500

        # Verify that the access token is used for the intended user
        gplus_id = credentials.id_token['sub']
        if result['user_id'] != gplus_id:
            return {
                'Success': False,
                'Message': "Token's user ID dosn't match given user ID."
            }, 401

        # Verify that the access token is valid for this app
        if result['issued_to'] != CLIENT_ID:
            return {
                'Success': False,
                'Message': "Token's client ID does not match app's"
            }, 401

        # Get user info
        userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
        params = {'access_token': access_token}
        answer = requests.get(userinfo_url, params=params)
        data = json.loads(answer.text)

        # store user info
        user_data = {}

        if not data["name"] or len(data['name']) < 1:
            user_data["username"] = data['email']
        else:
            user_data["username"] = data['name']
        user_data["google_id"] = data["id"]
        user_data["email"] = data['email']
        user_data["picture"] = data['picture']

        # check if the user is in our db
        user = UserModel.find_by_email(user_data["email"])
        if user is None:
            user = UserModel(None, **user_data)
            user.save_to_db()

        user = UserModel.find_by_email(user_data["email"])
        access_token = create_access_token(identity=user.json())

        return {"token": access_token}
