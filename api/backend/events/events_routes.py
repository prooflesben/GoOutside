
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
events = Blueprint('events', __name__)

#------------------------------------------------------------
# Get the stats for a given event
@events.route('/', methods=['GET'])
def event_root():
    return "events route works"

@events.route('/all', methods=['GET'])
def get_events():
    cursor = db.get_db().cursor()
    
    query = """
    SELECT *
    FROM Events
    """
  
    cursor.execute(query, (event_id,))
    theData = cursor.fetchall()
    
    if not theData:
        return make_response(jsonify({"error": "event not found"}), 404)
    response = make_response(jsonify(theData))
    response.status_code = 200
    return response


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
  
    
    

