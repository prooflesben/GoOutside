
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
organizer = Blueprint('organzier', __name__)

#------------------------------------------------------------
# Get allreviews for an organizer
@organizer.route('/organizers', methods=['GET'])
def get_organizers():
    try:
        current_app.logger.info(f'GET /attendee/<id>/bookmarks route')

        cursor = db.get_db().cursor()
        query = '''
            SELECT * 
            FROM OrganizerReviews;
            '''
        cursor.execute(query)
        
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
    except Exception as error:
        print(error)
        print("hello")
        the_response = make_response()  
        the_response.status_code = 500
    return the_response

#------------------------------------------------------------
# Get all non flagged reviews for an organizer with info like the organzier name and reviewer name
@organizer.route('/organizers/<id>/events/reviews', methods=['GET'])
def get_organizers_reviews(id):
    print("getting the organizer reviews")
    try:
        current_app.logger.info(f'GET /attendee/<id>/bookmarks route')

        cursor = db.get_db().cursor()
        query = '''
            SELECT orev.rating, orev.org_review_id, orev.comments, orev.written_by, O.name,A.first_name, A.last_name
            FROM OrganizerReviews orev
                JOIN Organizer O on O.organizer_id = orev.being_reviewed
                JOIN Attendees A on A.attendee_id = orev.written_by
            WHERE orev.flagged_by IS NULL AND orev.org_review_id = {0}
            ORDER BY orev.being_reviewed
            '''
        cursor.execute(query.format(id))
        
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
    except Exception as error:
        print(error)      
        print("hey") 
        the_response = make_response()  
        the_response.status_code = 500    
    
    return the_response

