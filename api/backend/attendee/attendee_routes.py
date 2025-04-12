
from flask import Blueprint
from flask import request
from flask import jsonify
from flask import make_response
from flask import current_app
from backend.db_connection import db

#------------------------------------------------------------
# Create a new Blueprint object, which is a collection of 
# routes.
attendee = Blueprint('attendee', __name__)


#------------------------------------------------------------
# Get all bookmarks for an attendee
@attendee.route('/attendee/<id>/bookmarks', methods=['GET'])
def get_attendee_bookmarks(id):
    current_app.logger.info(f'GET /attendee/<id>/bookmarks route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT e.event_id, e.event_name, e.event_date, e.event_location
        FROM event e
        JOIN event_bookmarks eb ON e.event_id = eb.event_id
        JOIN attendee a ON eb.attendee_id = a.attendee_id
        WHERE e.approved_by IS NOT NULL
        ORDER BY e.event_date DESC
        '''
    cursor.execute(query, (id,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Add events to an external calendar
@attendee.route('/attendees/{id}/calendar', methods=['PUT'])
def update_attendee_calendar(id):
    current_app.logger.info(f'PUT /attendees/{id}/calendar route')

    cursor = db.get_db().cursor()
    query = '''
        SELECT e.event_id, e.event_name, e.event_date, e.event_location
        FROM event e
        JOIN event_bookmarks eb ON e.event_id = eb.event_id
        JOIN attendee a ON eb.attendee_id = a.attendee_id
        WHERE e.approved_by IS NOT NULL
        ORDER BY e.event_date DESC
        '''
    cursor.execute(query, (id,))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response


#------------------------------------------------------------
# Update customer info for customer with particular userID
#   Notice the manner of constructing the query.
@attendee.route('/customers', methods=['PUT'])
def update_customer():
    current_app.logger.info('PUT /customers route')
    cust_info = request.json
    cust_id = cust_info['id']
    first = cust_info['first_name']
    last = cust_info['last_name']
    company = cust_info['company']

    query = 'UPDATE customers SET first_name = %s, last_name = %s, company = %s where id = %s'
    data = (first, last, company, cust_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'customer updated!'

#------------------------------------------------------------
# Get customer detail for customer with particular userID
#   Notice the manner of constructing the query. 
@attendee.route('/customers/<userID>', methods=['GET'])
def get_customer(userID):
    current_app.logger.info('GET /customers/<userID> route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT id, first_name, last_name FROM customers WHERE id = {0}'.format(userID))
    
    theData = cursor.fetchall()
    
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    return the_response

#------------------------------------------------------------
# Makes use of the very simple ML model in to predict a value
# and returns it to the user
@attendee.route('/prediction/<var01>/<var02>', methods=['GET'])
def predict_value(var01, var02):
    current_app.logger.info(f'var01 = {var01}')
    current_app.logger.info(f'var02 = {var02}')

    returnVal = predict(var01, var02)
    return_dict = {'result': returnVal}

    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response