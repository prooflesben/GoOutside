
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
        admin_announcement_id = the_data['admin_announcement_id']
        event_id = the_data['event_id']
        description = the_data['description']
        query = '''
            INSERT INTO Admin_Announcement(admin_announcement_id, event_id, description)
            VALUES (%s, %s, %s);
        '''
        
        # Execute the query
        connection = db.get_db()
        cursor = connection.cursor()
        cursor.execute(query, (admin_announcement_id, event_id, description))
        connection.commit()
        
        # Create a successful response
        response = make_response(jsonify({"message": "Announcement created successfully"}), 200)
    
    except Exception as error:
        current_app.logger.error(f"Error creating announcement: {error}")
        response = make_response(jsonify({"error": str(error)}), 500)
    
    return response

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
# Delete an event
@admin.route("/<int:admin_id>/event/<int:event_id>", methods=["DELETE"])
def delete_event_as_admin(admin_id, event_id):
    """
    DELETE /admin/<admin_id>/event/<event_id>
    Currently we don't validate admin_id against permissions—just logs it.
    """
    try:
        current_app.logger.info(
            f"DELETE /admin/{admin_id}/event/{event_id} route"
        )
        cursor = db.get_db().cursor()
        query = """
            DELETE FROM Events
            WHERE event_id = %s
        """
        cursor.execute(query, (event_id,))
        db.get_db().commit()

        if cursor.rowcount == 0:
            return make_response(
                jsonify({"message": "Event not found"}), 404
            )

        return make_response(
            jsonify({"message": "Event deleted", "event_id": event_id}), 200
        )

    except Exception as err:
        current_app.logger.error(f"Error deleting event: {err}")
        return make_response(jsonify({"error": "Internal server error"}), 500)





