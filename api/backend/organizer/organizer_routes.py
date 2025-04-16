
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
organizer = Blueprint('organzier', __name__)

#------------------------------------------------------------
# Get allreviews for an organizer
@organizer.route('/', methods=['GET'])
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
@organizer.route('/<id>/contact-info', methods=['GET'])
def get_organizers_contact_info(id):
    print("getting the organizer contact info")
    try:
        current_app.logger.info(f'GET organizers/<id>/contact-info')

        cursor = db.get_db().cursor()
        query = '''
            SELECT o.name, o.email, o.phone, o.organizer_id
            FROM Organizer o
            WHERE o.organizer_id = {0};
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


#------------------------------------------------------------
# Get all non flagged reviews for an organizer with info like the organzier name and reviewer name
@organizer.route('/<id>/reviews', methods=['GET'])
def get_organizers_reviews(id):
    print("getting the organizer reviews")
    try:
        current_app.logger.info(f'GET /organizers/<id>/events/reviews')

        cursor = db.get_db().cursor()
        query = '''
                SELECT orev.rating, orev.org_review_id, orev.comments, orev.written_by, O.name, A.first_name, A.last_name
                FROM OrganizerReviews orev
                    JOIN Organizer O on O.organizer_id = orev.being_reviewed
                    JOIN Attendees A on A.attendee_id = orev.written_by
                WHERE orev.flagged_by IS NULL AND orev.org_review_id = {0}
                ORDER BY orev.being_reviewed;
                '''
        cursor.execute(query.format(id))
        
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500    
    
    return the_response


#------------------------------------------------------------
# Get all non flagged reviews for an organizer with info like the organzier name and reviewer name
@organizer.route('/<id>/highest-engagement', methods=['GET'])
def get_organizers_highest_engagement (id):
    print("getting the organizer reviews")
    try:
        current_app.logger.info(f'GET /organizers/<id>/highest-engagement')

        cursor = db.get_db().cursor()
        query = '''
                SELECT *
                FROM Stats s 
                    JOIN Events e ON s.event_id = e.event_id
                WHERE e.organized_by = {0}
                ORDER BY (s.clicks + s.impressions)
                LIMIT 1;
                '''
        cursor.execute(query.format(id))
        
        theData = cursor.fetchall()
        cleanData = [{k: v for k, v in row.items() if k != 'event_id'} for row in theData]

        the_response = make_response(jsonify(cleanData))
        the_response.status_code = 200
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500    
    
    return the_response


#------------------------------------------------------------
# Get average rating for an organizer
@organizer.route('/<int:id>/stats/average-rating', methods=['GET'])
def get_organizers_average_rating (id):
    try:
        cursor = db.get_db().cursor()
        query = '''
                SELECT AVG(CAST(rating AS UNSIGNED)) AS average_rating
                FROM OrganizerReviews
                WHERE being_reviewed = %s
                '''
        cursor.execute(query, (id))
        
        theData = cursor.fetchall()

        the_response = make_response(jsonify(theData))
        the_response.status_code = 200

    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500    
    
    return the_response




