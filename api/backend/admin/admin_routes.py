
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
# Get all bookmarks for an attendee
@admin.route('/', methods=['GET'])
def testing():
    current_app.logger.info(f'GET /admin route')
    try:
        cursor = db.get_db().cursor()
        query = '''
            SELECT *
            FROM Admin_Announcement
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