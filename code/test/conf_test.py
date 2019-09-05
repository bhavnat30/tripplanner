import pytest
from project.models import User
 
 
@pytest.fixture(scope='module')
def new_user():
    user = User('bhavnathakur@gmail.com', 'FlaskPython!')
    return user