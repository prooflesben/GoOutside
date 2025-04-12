
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
def get_events():
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
      
