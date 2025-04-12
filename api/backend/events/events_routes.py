
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
attendee = Blueprint('events', __name__)


#------------------------------------------------------------
# Get the stats for a given event
@app.route('/events/<int:event_id>/stats', methods=['GET'])
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
    cursor = db.get_db().cursor()
    
    query = """
    SELECT e.name AS name, COUNT(*) AS bookmarks
    FROM Events_Bookmarks eb
    JOIN Events e ON e.event_id = eb.event_id
    WHERE e.event_id = %s
    GROUP BY e.event_id, e.name
    LIMIT 1;
    """
   
    cursor.execute(query, (event_id,))
    theData = cursor.fetchall()
    
    
    if not theData:
	    return make_response(jsonify({"error": "event not found"}), 404)
    
    row = theData[0]
    data = { "name": row[0], "bookmarks": row[1] }
      
    response = make_response(jsonify(data))
    response.status_code = 200
    return response

