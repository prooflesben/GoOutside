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




# adds the sponsor of a given event
@sponsors.route('/<int:sponsor_id>/events/<int:event_id>', methods=['PUT'])
def link_sponsor(sponsor_id, event_id):
    current_app.logger.info(f'PUT link /sponsors/{sponsor_id}/events/{event_id} route')

    cursor = db.get_db().cursor()
    query = '''
        UPDATE Events
        SET sponsor_by = %s
        WHERE event_id = %s
    '''
    cursor.execute(query, (sponsor_id, event_id))
    # saves the modification
    db.get_db().commit()
    the_response = make_response(jsonify({'message': 'Sponsor updated'}))
    the_response.status_code = 200
    return the_response

# removes the sponsor of a given event
@sponsors.route('/<int:sponsor_id>/events/<int:event_id>', methods=['DELETE'])
def unlink_sponsor(sponsor_id, event_id):
    current_app.logger.info(f'DELETE /sponsors/{sponsor_id}/events/{event_id} route')

    cursor = db.get_db().cursor()
    query = '''
        UPDATE Events
        SET sponsor_by = NULL
        WHERE event_id = %s
    '''
    cursor.execute(query, (event_id,))
    db.get_db().commit()
    return make_response(jsonify({'message': 'Sponsor removed'}), 200)



@sponsors.route('/reviews<int: min_rating>}', methods=['GET'])
def get_filtered_sponsor_reviews(min_rating):
    current_app.logger.info(f'GET /reviews<int: min_rating>')

    cursor = db.get_db().cursor()
    query = '''
        SELECT s.name AS sponsor_name, AVG(sr.rating) AS avg_rating
        FROM Sponsors s
        JOIN SponsorReviews sr ON s.sponsor_id = sr.being_reviewed
        GROUP BY s.sponsor_id
        HAVING AVG(sr.rating) >= %s
        ORDER BY avg_rating DESC;
        '''
    cursor.execute(query, (min_rating))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response