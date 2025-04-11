
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
organizer = Blueprint('organzier', __name__)


#------------------------------------------------------------
# Get all bookmarks for an attendee
@organizer.route('/attendee/<id>/bookmarks', methods=['GET'])
def get_attendee_bookmarks(id):
    current_app.logger.info(f'GET /attendee/<id>/bookmarks route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT e.event_id, e.event_name, e.event_date, e.event_location
        FROM event e
        JOIN event_bookmarks eb ON e.event_id = eb.event_id
        JOIN attendee a ON eb.attendee_id = a.attendee_id
        WHERE e.approved_by IS NOT NULL
        ORDER BY e.event_date DESC
        '''
    cursor.execute(query, (id,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response