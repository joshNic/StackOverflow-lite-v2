import os
import pytest
from app.views import app as create_app
import json
from app.database.db_operations import DbOperations
from app.database.db_connection import DbConnection
from instance.config import TestingConfig

@pytest.fixture
def app():
    app = create_app
    app.config.from_object(TestingConfig)
    # path = os.path.dirname(__file__)+'/databasetest.ini'
    # section = 'postgresqltest'
    # DbConnection(path, section)
    return app



