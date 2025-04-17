from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
organizer_reviews = Blueprint('organizer_reviews', __name__)

#------------------------------------------------------------

#------------------------------------------------------------



#Get all orginizer reviews
@organizer_reviews.route('/', methods=['GET'])
def get_all_organizer_reviews():
    current_app.logger.info(f'GET /admin route')
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT *
            FROM OrganizerReviews
            '''
        cursor.execute(query)
        theData = cursor.fetchall()
        
        the_response = make_response(jsonify(theData))
        the_response.status_code = 200
    except Exception as error:
        print(error)      
        the_response = make_response()  
        the_response.status_code = 500  
    return the_response

#------------------------------------------------------------
# Delete a specific organizer review
@organizer_reviews.route('/<int:review_id>', methods=['DELETE'])
def delete_reviews_by_organizer(review_id):
    try:
        cursor = db.get_db().cursor()
        query = '''
            DELETE FROM OrganizerReviews
            WHERE org_review_id = %s
        '''
        cursor.execute(query, (review_id,))
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response(jsonify({"message": "No reviews found for this organizer"}), 404)

        return make_response(jsonify({
            "message": f"Deleted {cursor.rowcount} review(s) written by organizer {review_id}"
        }), 200)
    
    except Exception as error:
        current_app.logger.error(f"Error deleting organizer reviews: {error}")
        return make_response(jsonify({"error": "Internal server error"}), 500)