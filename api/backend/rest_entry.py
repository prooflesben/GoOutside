from flask import Flask

from backend.db_connection import db
from backend.attendee.attendee_routes import attendee
from backend.organizer.organizer_routes import organizer
from backend.sponsors.sponsor_routes import sponsors
from backend.chatroom.chatroom_routes import chatroom # remove api
from backend.events.events_routes import events
from backend.event_categories.event_categories_routes import event_categories
from backend.admin.admin_routes import admin
import os
from dotenv import load_dotenv

def create_app():
    print("🚧d ENV DEBUG:", dict(os.environ))
    app = Flask(__name__)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup 
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session 
    # cookie and can be used for any other security related needs by 
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # # these are for the DB object to be able to connect to MySQL. 
    #app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_USER'] = os.getenv('DB_USER').strip()
    app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_ROOT_PASSWORD').strip()
    app.config['MYSQL_DATABASE_HOST'] = os.getenv('DB_HOST').strip()
    app.config['MYSQL_DATABASE_PORT'] = int(os.getenv('DB_PORT').strip())
    app.config['MYSQL_DATABASE_DB'] = os.getenv('DB_NAME').strip()  # Change this to your DB name

    # Initialize the database object with the settings above. 
    app.logger.info('current_app(): starting the database connection')
    db.init_app(app)


    # Register the routes from each Blueprint with the app object
    # and give a url prefix to each
    app.logger.info('current_app(): registering blueprints with Flask app object.')   
    app.register_blueprint(attendee, url_prefix='/attendee')
    app.register_blueprint(organizer, url_prefix='/organizer')
    app.register_blueprint(events, url_prefix='/events')
    app.register_blueprint(sponsors, url_prefix='/sponsor')
    app.register_blueprint(chatroom, url_prefix='/chatroom')
    app.register_blueprint(event_categories, url_prefix='/event_categories')
    app.register_blueprint(admin, url_prefix='/admin')
    # Don't forget to return the app object
    return app

