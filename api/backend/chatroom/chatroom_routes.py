from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db


chatroom = Blueprint('chatroom', __name__)

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
    # get data from request
    the_data = request.json
    current_app.logger.info(f'Received data: {the_data}')
    content = the_data['content']
    sender = the_data['sender'] 
    cursor = db.get_db().cursor()
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