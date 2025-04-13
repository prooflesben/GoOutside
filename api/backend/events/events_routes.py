
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
# Get the stats for a given event
@events.route('/', methods=['GET'])
def event_root():
    return "events route works"

@events.route('/<int:event_id>', methods=['GET'])
def get_events(event_id):
    cursor = db.get_db().cursor()
    query = """
    SELECT *
    FROM Events
    WHERE event_id = %s
    """
    cursor.execute(query, (event_id,))
    data = cursor.fetchall()
    if not data:
        return make_response(jsonify({"error": "event not found"}), 404)
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
      
