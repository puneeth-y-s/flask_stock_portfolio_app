from flask import Flask, render_template
import os
from project.db import init_db

# ----------------------------
# Application Factory Function
# ----------------------------

# def register_app_callbacks(app):
#     @app.before_request
#     def app_before_request():
#         print('Calling before_request() for the Flask application...')

    # @app.after_request
    # def app_after_request(response):
    #     print(f'response header is {response.headers}')
    #     return response

#     @app.teardown_request
#     def app_teardown_request(error=None):
#         print('Calling teardown_request() for the Flask application...')

#     @app.teardown_appcontext
#     def app_teardown_appcontext(error=None):
#         print('Calling teardown_appcontext() for the Flask application...')

def register_error_pages(app):
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404
    
    @app.errorhandler(405)
    def method_not_allowed(e):
        return render_template('405.html'), 405

def register_blueprints(app):
    # Import the blueprints
    from project.stocks import stocks_blueprint
    from project.users import users_blueprint

    # Since the application instance is now created, register each Blueprint
    # with the Flask application instance (app)
    app.register_blueprint(stocks_blueprint)
    app.register_blueprint(users_blueprint, url_prefix='/users')

def create_app():
    app = Flask(__name__)

    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    init_db(app.config['SQLALCHEMY_DATABASE_URI'])

    register_blueprints(app)

    # register_app_callbacks(app)

    register_error_pages(app)

    return app