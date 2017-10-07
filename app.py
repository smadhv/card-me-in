from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class User(Resource):
	username = ''
	password = ''
	venmo_id = ''
	phone_number = 0
	rating = 5
	listings = []

	def __init__():

	def post(self):

    def get(self):
        return {"hello": "world"}


api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
