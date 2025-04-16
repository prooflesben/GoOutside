
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
event_categories = Blueprint('event_categories', __name__)

#------------------------------------------------------------
# Get all the event categories
@event_categories.route('/', methods=['GET'])
def get_event_categories():
    cursor = db.get_db().cursor()
    query = """
    SELECT *
    FROM Event_Categories
    """
    cursor.execute(query)
    data = cursor.fetchall()
    if not data:
        return make_response(jsonify({}), 200)
    return data

#------------------------------------------------------------
# Add a new event cateogry
@event_categories.route('/', methods=['POST'])
def add_event_category():
    # get name and description from request body
    body = request.get_json()
    name = body.get('name')
    description = body.get('description')
    

    cursor = db.get_db().cursor()

    # check if name exists:
    query = """
    SELECT *
    FROM Event_Categories
    WHERE name = %s
    """
    cursor.execute(query, (name))
    data = cursor.fetchall()
    if data:
        return make_response(jsonify({"error" : "event category already exists"}), 404)

    query = """
    INSERT Event_Categories (name, description)
    VALUES
    (%s, %s)
    """
    cursor.execute(query, (name, description))
    db.get_db().commit()
    query = """
    SELECT *
    FROM Event_Categories
    """

    cursor.execute(query)
    data = cursor.fetchall()
    if not data:
        return make_response(jsonify({"error" : "unable to add event category"}), 404)
    return data

