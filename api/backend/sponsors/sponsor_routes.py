from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
from backend.ml_models.model01 import predict

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
sponsors = Blueprint('sponsors', __name__)


#------------------------------------------------------------

# will return sponsor ids and names from this
@sponsors.route('/', methods=['GET'])
def get_sponsors():
    current_app.logger.info(f'GET /sponsors route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT sponsor_id, sponsor_name
        FROM Sponsors
        '''
    cursor.execute(query)
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

# will return sponsor ids and names from this, will pass thru via json
@sponsors.route('/', methods=['POST'])
def post_sponsor():
    current_app.logger.info(f'POST /sponsors route')

    # get data
    the_data = request.json
    current_app.logger.info(f'Received data: {the_data}')
    name = the_data['name']
    email = the_data['email']
    phone = the_data.get('phone')
    approved_by = the_data['approved_by']

    query = '''
        INSERT INTO Sponsors (name, email, phone, approved_by)
        VALUES (%s, %s, %s, %s)
    '''
    
    cursor = db.get_db().cursor()
    cursor.execute(query, (name, email, phone, approved_by))
    db.get_db().commit()

    sponsor_id = cursor.lastrowid
    response = make_response(jsonify({"sponsor_id": sponsor_id}))
    response.status_code = 200
    return response




# gets ids of all sponsors and 
@sponsors.route('/<int:sponsor-id>}/events/<int:event-id>}', methods=['GET'])
def get_sponsors(id):
    current_app.logger.info(f'GET /sponors/<id>/bookmarks route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT o.name, avg(orgRev.rating) as 'Average Rating'
        FROM Organizer o JOIN OrganizerReviews orgRev ON orgRev.being_reviewed = o.organizer_id
        GROUP BY orgRev.being_reviewed
        ORDER BY avg(orgRev.rating) DESC
        '''
    # no params needed
    cursor.execute(query, ())
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

@sponsors.route('/review<int:id>', methods['POST'])
def post_sponsor_review(id):

@sponsors.route('/<int:sponsor-id>}/events/<int:event-id>}', methods=['GET'])
def get_sponsors(id):
