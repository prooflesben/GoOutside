from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


chatroom = Blueprint('chatroom', __name__)

# Create a new chat room
@chatroom.route('/<int:sponsor_id>/<int:organizer_id>', methods=['POST'])
def create_chat_room(sponsor_id, organizer_id):
    current_app.logger.info(f'POST /chatroom/{sponsor_id}/{organizer_id} route')
    
    try:
        cursor = db.get_db().cursor()
        
        # First check if chat room already exists
        check_query = '''
            SELECT 1 FROM ChatRooms 
            WHERE sponsor_id = %s AND organizer_id = %s
        '''
        cursor.execute(check_query, (sponsor_id, organizer_id))
        if cursor.fetchone():
            return make_response(jsonify({"message": "Chat room already exists"}), 200)
        
        # Create new chat room
        query = '''
            INSERT INTO ChatRooms (sponsor_id, organizer_id)
            VALUES (%s, %s)
        '''
        cursor.execute(query, (sponsor_id, organizer_id))
        db.get_db().commit()
        
        response = make_response(jsonify({
            "message": "Chat room created successfully",
            "sponsor_id": sponsor_id,
            "organizer_id": organizer_id
        }))
        response.status_code = 201
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error creating chat room: {e}")
        return make_response(jsonify({"error": str(e)}), 500)

# get entire chat history for a specific chatroom (sponsor-organizer pair)
@chatroom.route('/<int:sponsor_id>/<int:organizer_id>/messages', methods=['GET'])
def get_chat_history(sponsor_id, organizer_id):
    current_app.logger.info(f'GET /chatroom/{sponsor_id}/{organizer_id}/messages route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT m.message_id, m.content, m.organizer_id, m.sponsor_id, m.sender, m.created_at
        FROM Messages m
        WHERE m.sponsor_id = %s AND m.organizer_id = %s
        ORDER BY m.created_at ASC
    '''
    
    cursor.execute(query, (sponsor_id, organizer_id))
    messages = cursor.fetchall()
    
    response = make_response(jsonify(messages))
    response.status_code = 200
    return response

# add new msg to chatroom
@chatroom.route('/<int:sponsor_id>/<int:organizer_id>/messages', methods=['POST'])
def add_message(sponsor_id, organizer_id):
    current_app.logger.info(f'POST /chatroom/{sponsor_id}/{organizer_id}/messages route')
    
    try:
        # First check if chat room exists
        cursor = db.get_db().cursor()
        check_query = '''
            SELECT 1 FROM ChatRooms 
            WHERE sponsor_id = %s AND organizer_id = %s
        '''
        cursor.execute(check_query, (sponsor_id, organizer_id))
        if not cursor.fetchone():
            # Create chat room if it doesn't exist
            create_query = '''
                INSERT INTO ChatRooms (sponsor_id, organizer_id)
                VALUES (%s, %s)
            '''
            cursor.execute(create_query, (sponsor_id, organizer_id))
            db.get_db().commit()
        
        # get data from request
        the_data = request.json
        current_app.logger.info(f'Received data: {the_data}')
        content = the_data['content']
        sender = the_data['sender'] 
        
        query = '''
            INSERT INTO Messages (content, organizer_id, sponsor_id, sender)
            VALUES (%s, %s, %s, %s)
        '''
        cursor.execute(query, (content, organizer_id, sponsor_id, sender))
        db.get_db().commit()

        message_id = cursor.lastrowid
        response = make_response(jsonify({
            "message": "Message successfully sent",
            "message_id": message_id,
            "content": content,
            "organizer_id": organizer_id,
            "sponsor_id": sponsor_id,
            "sender": sender
        }))
        response.status_code = 200
        return response
        
    except Exception as e:
        current_app.logger.error(f"Error sending message: {e}")
        return make_response(jsonify({"error": str(e)}), 500) 