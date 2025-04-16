from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
sponsors = Blueprint('sponsors', __name__)


#------------------------------------------------------------

# will return sponsor ids and names from this
@sponsors.route('/', methods=['GET'])
def get_sponsors():
    current_app.logger.info(f'GET /sponsors route')
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT *
            FROM Sponsors
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

# will return sponsor ids and names from this, will pass thru via json
@sponsors.route('/', methods=['POST'])
def post_sponsor():
    current_app.logger.info(f'POST /sponsors route')
    try:
        # get data
        the_data = request.json
        current_app.logger.info(f'Received data: {the_data}')
        name = the_data['name']
        email = the_data['email']
        phone = the_data.get('phone')
        approved_by = the_data['approved_by']
        query = '''
            INSERT INTO Sponsors (name, email, phone, approved_by)
            VALUES (%s, %s, %s, %s)
        '''
        
        cursor = db.get_db().cursor()
        cursor.execute(query, (name, email, phone, approved_by))
        db.get_db().commit()

        sponsor_id = cursor.lastrowid
        response = make_response(jsonify({"sponsor_id": sponsor_id}))
        response.status_code = 200
    except Exception as error:
        print(error)      
        response = make_response()  
        response.status_code = 500
    
    return response




# adds the sponsor of a given event
@sponsors.route('/<int:sponsor_id>/events/<int:event_id>', methods=['PUT'])
def link_sponsor(sponsor_id, event_id):
    try:
        current_app.logger.info(f'PUT link /sponsors/{sponsor_id}/events/{event_id} route')
        cursor = db.get_db().cursor()
        query = '''
            UPDATE Events
            SET sponsor_by = %s
            WHERE event_id = %s
        '''
        cursor.execute(query, (sponsor_id, event_id))
        # saves the modification
        db.get_db().commit()
        the_response = make_response(jsonify({'message': 'Sponsor updated'}))
        the_response.status_code = 200
    except Exception as error:
        print(error)      
        response = make_response()  
        response.status_code = 500
    return the_response
    

# removes the sponsor of a given event
@sponsors.route('/<int:sponsor_id>/events/<int:event_id>', methods=['DELETE'])
def unlink_sponsor(sponsor_id, event_id):
    try:
        current_app.logger.info(f'DELETE /sponsors/{sponsor_id}/events/{event_id} route')
        cursor = db.get_db().cursor()
        query = '''
            UPDATE Events
            SET sponsor_by = NULL
            WHERE event_id = %s
        '''
        cursor.execute(query, (event_id,))
        db.get_db().commit()
        response = make_response(jsonify({'message': 'Sponsor removed'}), 200)
    except Exception as error:
        print(error)      
        response = make_response()  
        response.status_code = 500
    return response


# Gets all of the sponsors that have a review rating higher than a certain amount
@sponsors.route('/reviews/<int:min_rating>', methods=['GET'])
def get_filtered_sponsor_reviews(min_rating):
    try:
        current_app.logger.info(f'GET /reviews<int: min_rating>')
        cursor = db.get_db().cursor()
        query = '''
            SELECT s.name AS sponsor_name, AVG(sr.rating) AS avg_rating
            FROM Sponsors s
            JOIN SponsorReviews sr ON s.sponsor_id = sr.being_reviewed
            GROUP BY s.sponsor_id
            HAVING AVG(sr.rating) >= %s
            ORDER BY avg_rating DESC;
            '''
        cursor.execute(query, (min_rating))
        theData = cursor.fetchall()
        response = make_response(jsonify(theData))
        response.status_code = 200
    except Exception as error:
        print(error)      
        response = make_response()  
        response.status_code = 500
    return response


# will add a review for a sponsor from an organizer
@sponsors.route('/reviews', methods=['POST'])
def add_organizer_review_on_sponsor():
    try:
        current_app.logger.info('POST /reviews route')
        the_data = request.json
        current_app.logger.info(f'Received data: {the_data}')
        rating = the_data['rating']
        sponsor_id = the_data['sponsor_id']
        organizer_id = the_data['organizer_id']
        comments = the_data.get('comments', '')

        query = '''
            INSERT INTO SponsorReviews (rating, written_by, being_reviewed, comments)
            VALUES (%s, %s, %s, %s)
        '''
        
        cursor = db.get_db().cursor()
        cursor.execute(query, (rating, organizer_id, sponsor_id, comments))
        db.get_db().commit()

        review_id = cursor.lastrowid

        response = make_response(jsonify({
            "message": "Review successfully created",
            "review_id": review_id,
            "rating": rating,
            "sponsor_id": sponsor_id,
            "organizer_id": organizer_id,
            "comments": comments
        }))
        response.status_code = 200
    except Exception as error:
        print(error)      
        response = make_response()  
        response.status_code = 500
    return response

# retreives all of the reviews for a sposnor
@sponsors.route('/<int:sponsor_id>/reviews', methods=['GET'])
def get_sponsor_reviews(sponsor_id):
    try:
        current_app.logger.info(f'GET /sponsors/:id/reviews route')
        cursor = db.get_db().cursor()
        query = '''
            SELECT *
            FROM SponsorReviews
            WHERE being_reviewed = {0}
            '''
        cursor.execute(query.format(sponsor_id))
        theData = cursor.fetchall()
        
        response = make_response(jsonify(theData))
        response.status_code = 200
    except Exception as error:
        print(error)      
        response = make_response()  
        response.status_code = 500
    return response



# get all the sponsor events_stats
@sponsors.route('/<int:sponsor_id>/events/stats', methods=['GET'])
def get_sponsor_event_stats(sponsor_id):
    try:
        cursor = db.get_db().cursor()
        query = """
            SELECT 
                e.name,
                s.clicks,
                s.impressions,
                (s.clicks + s.impressions) AS engagement
            FROM Events e
            JOIN Stats s ON e.event_id = s.event_id
            WHERE e.sponsor_by = %s
            ORDER BY engagement DESC;
        """
        cursor.execute(query, (sponsor_id,))
        data = cursor.fetchall()
       
        if not data:
            return make_response(jsonify({"message": "No sponsored events found"}), 404)

        return make_response(jsonify(data), 200)

    except Exception as error:
        return make_response(jsonify({"error": "Internal server error"}), 500)

