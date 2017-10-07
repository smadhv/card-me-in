from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class User(Resource):

	def __init__(self, username, password, venmo, phone, rating, listings):
		self.username = username
		self.password = password
		self.venmo_id = venmo
		self.phone_number = phone
		self.rating = rating
		self.listings = listings #list of listings

	def post(self):

    def get(self):
        return {"hello": "world"}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
