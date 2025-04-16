from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db
import logging

import traceback

# Setup basic logging configuration
logging.basicConfig(level=logging.DEBUG)

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
events = Blueprint('events', __name__)
    
#------------------------------------------------------------
# Get the details for all the events with the sponsor name and organizer name
@events.route('/', methods=['GET'])
def get_all_events_clean():
    try: 
        cursor = db.get_db().cursor()
        query = """
        SELECT 
            e.*,
            s.name AS sponsor_name,
            o.name AS organizer_name
        FROM Events e
        JOIN Sponsors s ON e.sponsor_by = s.sponsor_id
        JOIN Organizer o ON e.organized_by = o.organizer_id;
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        if not data:
            return make_response(jsonify({}), 200)
        return data
    except Exception as error:
       # Log the error with traceback
        logging.error("Error occurred: %s", str(error))
        logging.error("Stack trace: %s", traceback.format_exc())
        
        # Return a generic error response
        the_response = make_response(jsonify({"error": "Internal server error"}))
        the_response.status_code = 500
        return the_response
    
    
#------------------------------------------------------------
# Get the details for all the events with no sponsor
@events.route('/no-sponsor', methods=['GET'])
def get_all_unsponsored_events():
    try: 
        cursor = db.get_db().cursor()
        query = """
        SELECT 
            e.*,
            o.name AS organizer_name
        FROM Events e
        JOIN Organizer o ON e.organized_by = o.organizer_id
        WHERE e.sponsor_by IS NULL;
        """
        
        cursor.execute(query)
        data = cursor.fetchall()
        
        if not data:
            return make_response(jsonify({}), 200)
        return data
    except Exception as error:
       # Log the error with traceback
        logging.error("Error occurred: %s", str(error))
        logging.error("Stack trace: %s", traceback.format_exc())
        
        # Return a generic error response
        the_response = make_response(jsonify({"error": "Internal server error"}))
        the_response.status_code = 500
        return the_response

@events.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
    if request.method == 'GET':
        try: 
            cursor = db.get_db().cursor()
            query = """
            SELECT *
            FROM Events
            WHERE event_id = %s
            """
            
            cursor.execute(query, (event_id,))
            data = cursor.fetchall()
            
            if not data:
                return make_response(jsonify({}), 200)
            return data
        except Exception as error:
            print(error)      
            the_response = make_response()  
            the_response.status_code = 500 
            return the_response 

@events.route('/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    try:
        current_app.logger.info(f'DELETE /events/{event_id} route')
        cursor = db.get_db().cursor()
        query = """
                DELETE FROM Events
                WHERE event_id = %s
                """
        cursor.execute(query, (event_id,))
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response(jsonify({"message": "Event not found"}), 404)
        
        response = make_response(jsonify({'message': 'Event removed'}), 200)
    except Exception as error:
        print(f"Error handling event {event_id}: {error}")
        return make_response(jsonify({"error": "Internal server error"}), 500)
    return response


#------------------------------------------------------------
# Search for events by location, category, and date
@events.route('/search/<string:location>/<string:category>/<string:date>', methods=['GET'])
def search_events(location, category, date):
    try:
        # test with http://localhost:4000/events/search/Central%20Park/Music/2025-05-01
        cursor = db.get_db().cursor()
        query = """
        SELECT * 
        FROM Events
        WHERE location = %s AND category_name = %s AND DATE(start_time) = %s
        """
        cursor.execute(query, (location, category, date))
        data = cursor.fetchall()
        if not data:
            return make_response(jsonify({"error": "no event found matching search query"}), 404)
        return data
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500
        return the_response 

#------------------------------------------------------------
# Get the stats for a given event
@events.route('/<int:event_id>/stats', methods=['GET'])
def get_event_popularity_stats(event_id):
    try:
        cursor = db.get_db().cursor()
        
        query = """
        SELECT clicks, impressions
        FROM Stats
        WHERE event_id = %s
        LIMIT 1;
        """
    
        cursor.execute(query, (event_id,))

        data = cursor.fetchall()
        if not data:
            return make_response(jsonify({"clicks": 0, "impressions": 0}), 200)
        return data[0]
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500 
     
#------------------------------------------------------------
# Get the boomarks for a given event
@events.route('/<int:event_id>/stats/popularity', methods=['GET'])
def get_event_bookmarks(event_id):
    try:
        cursor = db.get_db().cursor()
        
        query = """
        SELECT e.name AS name, COUNT(*) AS bookmarks
        FROM Event_Bookmarks eb
        JOIN Events e ON e.event_id = eb.event_id
        WHERE e.event_id = %s
        GROUP BY e.event_id, e.name
        LIMIT 1;
        """
    
        cursor.execute(query, (event_id,))
        data = cursor.fetchall()
        
        if not data:
            return make_response(jsonify({"error": "event not found"}), 404)
        return data[0]
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500 
        return the_response
      

#------------------------------------------------------------
# Get the names of people attending a given event
@events.route('/<int:event_id>/attendance', methods=['GET'])
def get_event_attendance(event_id):
    try:
        cursor = db.get_db().cursor()
        
        query = """
        SELECT a.first_name, a.last_name
        FROM Event_Attendance ea
        JOIN Attendees a ON a.attendee_id = ea.attendee_id
        WHERE ea.event_id = %s
        """
    
        cursor.execute(query, (event_id,))
        data = cursor.fetchall()
        
        if not data:
            return make_response(jsonify({"error": "event not found"}), 404)
        return data
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500 
        return the_response


#------------------------------------------------------------
# Gets the announcments for this event
@events.route('/<int:event_id>/announcement', methods=['GET'])
def get_event_announcements(event_id):
    try:
        cursor = db.get_db().cursor()
        
        query = """
        SELECT e.name, a.description
        FROM Event_Announcement a
        JOIN Events e ON e.event_id = a.event_id
        WHERE a.event_id = %s
        """

        cursor.execute(query, (event_id,))
        data = cursor.fetchall()
        if not data:
            return make_response(jsonify([]), 200)
        return data
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500 
        return the_response

#------------------------------------------------------------
# Make a new announcments for the given event (return updated announcement)
@events.route('/<int:event_id>/announcement', methods=['POST'])
def make_event_announcements(event_id):
    try:
        # get description from request body
        body = request.get_json()
        description = body.get('description')

        cursor = db.get_db().cursor()

        query = """
        INSERT Event_Announcement (event_id, description)
        VALUES
        (%s, %s)
        """
        cursor.execute(query, (event_id, description))
        db.get_db().commit()
        query = """
        SELECT description
        FROM Event_Announcement 
        WHERE event_id = %s
        """

        cursor.execute(query, (event_id,))
        data = cursor.fetchall()
        if not data:
            return make_response(jsonify({"error" : "enable to make announcement"}), 404)
        return data
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500 
        return the_response
