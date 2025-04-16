
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

    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT e.event_id, e.name, e.start_time, e.location
            FROM Events e
            JOIN Event_Bookmarks eb ON e.event_id = eb.event_id
            JOIN Attendees a ON eb.attendee_id = a.attendee_id
            WHERE e.approved_by IS NOT NULL
            AND eb.attendee_id = %s
            ORDER BY e.start_time DESC
            '''
        cursor.execute(query, (id,))

        theData = cursor.fetchall()
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200

    except Exception as e:
        current_app.logger.error(f"Error fetching bookmarks: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while fetching bookmarks'}))
        the_response.status_code = 500

    return the_response

#------------------------------------------------------------
# Add a new event bookmark for an attendee
@attendee.route('/<id>/bookmarks/<eventId>', methods=['POST'])
def add_attendee_bookmark(id, eventId):
    current_app.logger.info(f'POST /attendee/<id>/bookmarks/<eventId> route')

    try:
        cursor = db.get_db().cursor()
        query = '''
            INSERT INTO Event_Bookmarks (event_id, attendee_id)
            VALUES (%s, %s)
            '''
        cursor.execute(query, (eventId, id))
        
        db.get_db().commit()
        
        the_response = make_response(jsonify({'message': 'Bookmark added!'}))
        the_response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error adding bookmark: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while adding the bookmark'}))
        the_response.status_code = 500

    return the_response
    

#------------------------------------------------------------
# Delete a new event bookmark for an attendee
@attendee.route('/<id>/bookmarks/<eventId>', methods=['DELETE'])
def delete_attendee_bookmark(id, eventId):
    current_app.logger.info(f'DELETE /attendee/<id>/bookmarks/<eventId> route')

    try:
        cursor = db.get_db().cursor()
        query = '''
            DELETE FROM Event_Bookmarks
            WHERE event_id = %s AND attendee_id = %s
            '''
        cursor.execute(query, (eventId, id))
        
        db.get_db().commit()
        
        the_response = make_response(jsonify({'message': 'Bookmark deleted!'}))
        the_response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error deleting bookmark: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while deleting the bookmark'}))
        the_response.status_code = 500

    return the_response

#------------------------------------------------------------
# Get recommended events for an attendee based on their favorite event category
@attendee.route('/<id>/recommendations', methods=['GET'])
def get_attendee_recommendations(id):
    current_app.logger.info(f'GET /attendee/<id>/recommendations route')

    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT e.event_id, e.name, e.start_time, e.location, e.cost
            FROM Events e
            JOIN Attendees a ON e.category_name = a.fav_category
            WHERE e.approved_by IS NOT NULL
            AND a.attendee_id = %s
        '''
        cursor.execute(query, (id,))
        
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200

    except Exception as e:
        current_app.logger.error(f"Error fetching recommendations: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while fetching recommendations'}))
        the_response.status_code = 500

    return the_response

#------------------------------------------------------------
# Get all events an attendee has rsvpd to
@attendee.route('/<id>/rsvps', methods=['GET'])
def get_attendee_rsvps(id):
    current_app.logger.info(f'GET /attendee/<id>/rsvps route')

    try:
        cursor = db.get_db().cursor()

        query = '''
            SELECT e.event_id, e.name, e.start_time, e.location
            FROM Events e
            JOIN Event_Attendance er ON e.event_id = er.event_id
            JOIN Attendees a ON er.attendee_id = a.attendee_id
            WHERE e.approved_by IS NOT NULL
            AND er.attendee_id = %s
            ORDER BY e.start_time DESC
            '''
        cursor.execute(query, (id,))
        
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200

    except Exception as e:
        current_app.logger.error(f"Error fetching RSVPs: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while fetching RSVPs'}))
        the_response.status_code = 500

    return the_response

#------------------------------------------------------------
# Submit an organizer review from an attendee
@attendee.route('/<int:attendee_id>/review/organizer/<int:organizer_id>', methods=['POST'])
def submit_organizer_review(attendee_id, organizer_id):

    try:
        data = request.get_json()

        rating = data.get('rating')
        comments = data.get('comments', None)
        flagged_by = data.get('flagged_by')  # Can be None

        cursor = db.get_db().cursor()

        query = '''
            INSERT INTO OrganizerReviews (rating, comments, written_by, being_reviewed, flagged_by)
            VALUES (%s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (rating, comments, attendee_id, organizer_id, flagged_by))
        db.get_db().commit()

        the_response = make_response(jsonify({'message': 'Review submitted successfully!'}))
        the_response.status_code = 200

    except Exception as e:
        current_app.logger.error(f"Error submitting review: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while submitting the review'}))
        the_response.status_code = 500

    return the_response

