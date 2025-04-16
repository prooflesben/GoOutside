
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
attendee = Blueprint('attendee', __name__)


#------------------------------------------------------------
# Get all bookmarked events for an attendee
@attendee.route('/<id>/bookmarks', methods=['GET'])
def get_attendee_bookmarks(id):
    current_app.logger.info(f'GET /attendee/<id>/bookmarks route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT e.event_id, e.name, e.start_time, e.location
        FROM Events e
        JOIN Event_Bookmarks eb ON e.event_id = eb.event_id
        JOIN Attendees a ON eb.attendee_id = a.attendee_id
        WHERE e.approved_by IS NOT NULL
        AND a.attendee_id = %s
        ORDER BY e.start_time DESC
        '''
    
    cursor.execute(query, (id,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response
