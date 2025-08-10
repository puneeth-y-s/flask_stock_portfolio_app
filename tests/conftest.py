import os
from project import create_app
import pytest
from project.models import Stock, Base, User
from sqlalchemy import create_engine

@pytest.fixture(scope='module')
def test_client():
    # Set the Testing configuration prior to creating the Flask application
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as testing_client:
        # Establish an application context before accessing the logger and database
        with flask_app.app_context():

            # Create engine from app config
            engine = create_engine(flask_app.config['SQLALCHEMY_DATABASE_URI'])

            # Create the database and the database table(s)
            Base.metadata.create_all(bind=engine)

        yield testing_client  # this is where the testing happens!

        with flask_app.app_context():
            Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope='module')
def new_stock():
    stock = Stock('AAPL', '16', '406.78')
    return stock

@pytest.fixture(scope="module")
def new_user():
    user = User('johndoe@gmail.com', "passw0rd")
    return user