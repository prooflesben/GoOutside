
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

#------------------------------------------------------------
# Get the stats for a given event
@events.route('/events/<int:event_id>/stats', methods=['GET'])
def get_event_popularity_stats(event_id):
    cursor = db.get_db().cursor()
    
    query = """
    SELECT clicks, impressions
    FROM Stats
    WHERE event_id = %s
    LIMIT 1;
    """
  
    cursor.execute(query, (event_id,))
    theData = cursor.fetchall()
	
    if not theData:
        return make_response(jsonify({"error": "event not found"}), 404)
    row = theData[0]
    data = { "clicks": row[0], "impressions": row[1] }

      
    response = make_response(jsonify(data))
    response.status_code = 200
    return response
    
    

