from Flask import jsonify, request

# class Listing(Resource):

# 	def __init__(self, user_id, place, cost, time, status):
# 		self.user_id = user_id
# 		self.place = place
# 		self.cost = cost
# 		self.time = time
# 		self.status = status

# 	def post(self):

# 	def get(self):

@app.route('/listings', methods = ['GET'])
def get_listings():
	db = get_db()
    cur = db.execute('select user_id, meal_time, place, cost, status from listings order by listing_id desc')
    entries = cur.fetchall()
	return 'success'

@app.route('/listings/<int:listing_id>', methods = ['GET'])
def get_one_listing(listing_id)
	db = get_db()
    cur = db.execute('select user_id, meal_time, place, cost, status from listings where listing_id = ?', listing_id)
    entries = cur.fetchall()
	return 'success'

@app.route('/listings', methods = ['POST'])
def add_listing():
	db = get_db()
    db.execute('insert into listings (user_id, time, place, cost, status) values (?, ?, ?, ?, ?)',
                 [request.form['user'], request.form['time'], request.form['place'], request.form['cost'], 'available'])
    db.commit()
    flash('New listing was successfully posted')
    return 'success'

@app.route('/listings', methods = ['DELETE'])
def delete_listing(listing_id):
	db = get_db()
    db.execute('delete from listings where listing_id = ?', listing_id)
    db.commit()
    return 'success'

@app.route('/listings/<int:listing_id>', methods = ['PUT'])
def update_listing_status(listing_id, new_status)
	db = get_db()
    cur = db.execute('update listings set status = ? where listing_id = ?', new_status, listing_id)
    db.commit()
    flash('Listing was successfully modified')
	return 'success'

@app.route('/listings', methods = ['GET'])
def get_listings_user(user_id):
	db = get_db()
    cur = db.execute('select user_id, meal_time, place, cost, status from listings where user_id = ? order by listing_id desc', user_id)
    entries = cur.fetchall()
	return 'success'
