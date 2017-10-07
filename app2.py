class Listing(Resource):

	def __init__(self, user_id, place, cost, time, status):
		self.user_id = user_id
		self.place = place
		self.cost = cost
		self.time = time
		self.status = status

	def post(self):

	def get(self):

listings = []
@app.route('/listings', methods = ['GET'])
def get_listings():

