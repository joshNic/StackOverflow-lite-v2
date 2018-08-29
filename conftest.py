import pytest
from app.views import app as create_app
import json


@pytest.fixture
def app():
    app = create_app
    app.debug = True
    return app
