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

@attendee.route('/', methods=['GET'])
def get_attendees():
    current_app.logger.info(f'GET /attendee route')
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT *
            FROM Attendees
            '''
        cursor.execute(query)
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500  
    return the_response
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
# RSVP to an event
@attendee.route('/<id>/rsvps/<eventId>', methods=['POST'])
def post_attendee_rsvp(id, eventId):
    current_app.logger.info(f'POST /attendee/<id>/rsvps/<eventId> route')

    try:
        cursor = db.get_db().cursor()
        query = '''
            INSERT INTO Event_Attendance (event_id, attendee_id)
            VALUES (%s, %s)
            '''
        cursor.execute(query, (eventId, id))
        
        db.get_db().commit()
        
        the_response = make_response(jsonify({'message': 'RSVP successful!'}))
        the_response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error RSVPing to event: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while RSVPing to the event'}))
        the_response.status_code = 500

    return the_response

#------------------------------------------------------------
# Un-RSVP from an event
@attendee.route('/<id>/rsvps/<eventId>', methods=['DELETE'])
def delete_attendee_rsvp(id, eventId):
    current_app.logger.info(f'DELETE /attendee/<id>/rsvps/<eventId> route')

    try:
        cursor = db.get_db().cursor()
        query = '''
            DELETE FROM Event_Attendance
            WHERE event_id = %s AND attendee_id = %s
            '''
        cursor.execute(query, (eventId, id))
        
        db.get_db().commit()
        
        the_response = make_response(jsonify({'message': 'Un-RSVP successful!'}))
        the_response.status_code = 200
    except Exception as e:
        current_app.logger.error(f"Error un-RSVPing from event: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while un-RSVPing from the event'}))
        the_response.status_code = 500

    return the_response

#------------------------------------------------------------
# Get all event organizers of events an attendee has attended
@attendee.route('/<id>/organizers', methods=['GET'])
def get_attendee_organizers(id):
    current_app.logger.info(f'GET /attendee/<id>/organizers route')

    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT DISTINCT o.name, o.organizer_id
            FROM Organizer o
            JOIN Events e ON o.organizer_id = e.organized_by
            JOIN Event_Attendance er ON e.event_id = er.event_id
            JOIN Attendees a ON er.attendee_id = a.attendee_id
            WHERE er.attendee_id = %s
            AND e.approved_by IS NOT NULL
        '''
        cursor.execute(query, (id,))
        
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200

    except Exception as e:
        current_app.logger.error(f"Error fetching organizers: {e}")
        the_response = make_response(jsonify({'error': 'An error occurred while fetching organizers'}))
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

#------------------------------------------------------------
# deleting a review
@attendee.route('/<attendee_id>/reviews/<review_id>', methods=['DELETE'])
def delete_attendee_review(attendee_id, review_id):
    current_app.logger.info(f'DELETE /attendee/<attendee_id>/reviews/<review_id> route')

    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM OrganizerReviews
        WHERE written_by = %s AND org_review_id = %s
        '''
    cursor.execute(query, (attendee_id, review_id))
    # if got no reviews
    if cursor.rowcount == 0:
        the_response = make_response(jsonify({'error': 'Review not found'}), 404)
    else:
        # actually delete 
        db.get_db().commit()
        the_response = make_response(jsonify({'message': 'Review deleted successfully'}))
        the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# make review from attendee to organizer
@attendee.route('/<attendee_id>/reviews/<organizer_id>', methods=['POST'])
def create_attendee_review(attendee_id, organizer_id):
    current_app.logger.info(f'POST /attendee/<attendee_id>/reviews/<organizer_id> route')

    try:
        the_data = request.json
        current_app.logger.info(f'Received data: {the_data}')
        
        rating = the_data['rating']
        # note comment is optional
        comments = the_data.get('comments', '')

        cursor = db.get_db().cursor()
        query = '''
            INSERT INTO OrganizerReviews (rating, comments, written_by, being_reviewed)
            VALUES (%s, %s, %s, %s)
            '''
        cursor.execute(query, (rating, comments, attendee_id, organizer_id))
        # actualy mkae the change
        db.get_db().commit()
        review_id = cursor.lastrowid
        
        the_response = make_response(jsonify({
            'message': 'Review created successfully',
            'review_id': review_id,
            'rating': rating,
            'comments': comments,
            'written_by': attendee_id,
            'being_reviewed': organizer_id
        }))
        the_response.status_code = 201
    except Exception as error:
        print(error)
        the_response = make_response(jsonify({'error': 'Failed to create review'}), 500)
    return the_response

#------------------------------------------------------------
# Output a txt file that an attendee can use to add a event to their calendar
@attendee.route('/<id>/calendar/<eventId>', methods=['PUT'])
def put_attendee_calendar(id, eventId):
    current_app.logger.info(f'PUT /attendee/<id>/calendar/<eventId> route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT e.event_id, e.name, e.start_time, e.end_time, e.location
        FROM Events e
        JOIN Event_Attendance er ON e.event_id = er.event_id
        JOIN Attendees a ON er.attendee_id = a.attendee_id
        WHERE e.approved_by IS NOT NULL
        AND er.attendee_id = %s
        AND e.event_id = %s
        '''
    cursor.execute(query, (id, eventId))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    
    return the_response