from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
admin = Blueprint('admin', __name__)



@admin.route('/ping', methods=['GET'])
def ping():
    return "hi"

#------------------------------------------------------------
# Get all admins
@admin.route('/', methods=['GET'])
def testing():
    current_app.logger.info(f'GET /admin route')
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT *
            FROM Admin
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


@admin.route('/announcement', methods=['POST'])
def admin_create_announment():
    # In a POST request, there is a 
    # collecting data from the request object 
    try:
        # get data
        the_data = request.json
        current_app.logger.info(f'Received data: {the_data}')
        event_id = the_data['event_id']
        description = the_data['description']
        query = '''
            INSERT INTO Admin_Announcement(event_id, description)
            VALUES (%s, %s);
        '''
        
        # Execute the query
        connection = db.get_db()
        cursor = connection.cursor()
        cursor.execute(query, (event_id, description))
        connection.commit()
        
        # Create a successful response
        response = make_response(jsonify({"message": "Announcement created successfully"}), 200)
    
    except Exception as error:
        current_app.logger.error(f"Error creating announcement: {error}")
        response = make_response(jsonify({"error": str(error)}), 500)
    
    return response

#------------------------------------------------------------
# Get all announcements
@admin.route('/announcements', methods=['GET'])
def get_all_announcements():
    try:
        current_app.logger.info(f'GET /admin/announcements route')
        cursor = db.get_db().cursor()
        query = '''
            SELECT e.name AS event_name, e.start_time as event_time, e.location, e.description, a.description AS message
            FROM Events e
            JOIN Admin_Announcement a ON e.event_id = a.event_id
            WHERE e.start_time > NOW()
            ORDER BY e.start_time ASC
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
# Admin approve an event
@admin.route("/<int:admin_id>/event/<int:event_id>", methods=["PUT"])
def approve_event(admin_id, event_id):
    try:
        current_app.logger.info(
            f"PUT /admin/{admin_id}/event/{event_id}/approve route"
        )
        cursor = db.get_db().cursor()
        query = """
            UPDATE Events
            SET approved_by = %s
            WHERE event_id = %s
        """
        cursor.execute(query, (admin_id, event_id))
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response(
                jsonify({"message": "Event not found"}), 404
            )

        return make_response(
            jsonify(
                {
                    "message": "Event approved",
                    "event_id": event_id,
                    "approved_by": admin_id,
                }
            ),
            200,
        )

    except Exception as err:
        return make_response(jsonify({"error": "Internal server error"}), 500)
    


#------------------------------------------------------------
# Flag a bad review
# NOTE: admin_id is a string, so we need to check if it's 'null'
@admin.route("/<admin_id>/organizer_review/<int:review_id>", methods=["PUT"])
def flag_organizer_review(admin_id, review_id):
    try:
        cursor = db.get_db().cursor()
        
        # Handle unflagging (when admin_id is 'null')
        if admin_id.lower() == 'null':
            query = """
                UPDATE OrganizerReviews
                SET flagged_by = NULL
                WHERE org_review_id = %s
            """
            cursor.execute(query, (review_id,))
        else:
            # Handle flagging with a specific admin_id
            try:
                admin_id_int = int(admin_id)
                query = """
                    UPDATE OrganizerReviews
                    SET flagged_by = %s
                    WHERE org_review_id = %s
                """
                cursor.execute(query, (admin_id_int, review_id))
            except ValueError:
                return make_response(jsonify({"error": "Invalid admin_id format"}), 400)
            
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response(jsonify({"message": "Review not found"}), 404)

        return make_response(jsonify({
            "message": "Review updated successfully",
            "review_id": review_id,
            "flagged_by": None if admin_id.lower() == 'null' else int(admin_id)
        }), 200)

    except Exception as err:
        current_app.logger.error(f"Error updating review: {err}")
        return make_response(jsonify({"error": "Internal server error"}), 500)



