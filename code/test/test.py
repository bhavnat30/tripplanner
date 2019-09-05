from project.models import User
 
 
def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, authenticated, and role fields are defined correctly
    """
    user = User('bhavnathakur@gmail.com', 'FlaskPython!')
    assert new_user.email == 'bhavnathakur@gmail.com'
    assert new_user.hashed_password != 'FlaskPython!'
    assert not new_user.authenticated
    assert new_user.role == 'user'