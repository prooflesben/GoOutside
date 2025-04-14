
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
# Get all bookmarks for an attendee
@attendee.route('/attendee/<id>/bookmarks', methods=['GET'])
def get_attendee_bookmarks(id):
    try:
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
    except Exception as e:
        current_app.logger.error(f"Error fetching attendee bookmarks: {e}")

    return the_response

#------------------------------------------------------------
# Get all events an attendee has rsvpd to
@attendee.route('/attendee/<id>/rsvps', methods=['GET'])
def get_attendee_rsvps(id):
    try:
        current_app.logger.info(f'GET /attendee/<id>/rsvps route')

        cursor = db.get_db().cursor()
        query = '''
            SELECT e.event_id, e.event_name, e.event_date, e.event_location
            FROM Events e
            JOIN Event_Attendance er ON e.event_id = er.event_id
            JOIN Attendee a ON er.attendee_id = a.attendee_id
            WHERE e.approved_by IS NOT NULL
            ORDER BY e.event_date DESC
            '''
        cursor.execute(query, (id,))
        
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error fetching attendee rsvps: {e}")

    return the_response
