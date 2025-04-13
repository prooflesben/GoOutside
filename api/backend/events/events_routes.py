
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
events = Blueprint('events', __name__)

#------------------------------------------------------------
# Get the details for all the events
@events.route('/', methods=['GET'])
def get_all_events():
    cursor = db.get_db().cursor()
    query = """
    SELECT *
    FROM Events
    """
    
    cursor.execute(query)
    data = cursor.fetchall()
    
    if not data:
        return make_response(jsonify({}), 200)
    return data

#------------------------------------------------------------
# Get the details for a single event
@events.route('/<int:event_id>', methods=['GET'])
def get_event(event_id):
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

@events.route('/search/<string:location>/<string:category>/<string:date>', methods=['GET'])
def search_events(location, category, date):
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

#------------------------------------------------------------
# Get the stats for a given event
@events.route('/<int:event_id>/stats', methods=['GET'])
def get_event_popularity_stats(event_id):
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
        return make_response(jsonify({"error": "event not found"}), 404)
    return data[0]
     
#------------------------------------------------------------
# Get the boomarks for a given event
@events.route('/<int:event_id>/stats/popularity', methods=['GET'])
def get_event_bookmarks(event_id):
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
      

#------------------------------------------------------------
# Gets the announcments for this event
@events.route('/<int:event_id>/announcement', methods=['GET'])
def get_event_announcements(event_id):
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

#------------------------------------------------------------
# Make a new announcments for the given event (return updated announcement)
@events.route('/<int:event_id>/announcement', methods=['POST'])
def make_event_announcements(event_id):
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