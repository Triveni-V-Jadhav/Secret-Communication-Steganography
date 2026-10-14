import pytest
from app import create_app, db
from app.models.user import User

@pytest.fixture
def client():
    app = create_app("testing")
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_user_registration(client):
    res = client.post("/auth/register", data={
        "username": "testuser",
        "email": "testuser@securecomm.local",
        "role": "USER",
        "password": "Password123!",
        "confirm_password": "Password123!"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Registration successful" in res.data
    
    # Duplicate username prevention
    res_dup = client.post("/auth/register", data={
        "username": "testuser",
        "email": "different@securecomm.local",
        "role": "USER",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    assert b"already taken" in res_dup.data

def test_user_authentication(client):
    # Setup user
    client.post("/auth/register", data={
        "username": "loginuser",
        "email": "loginuser@securecomm.local",
        "role": "USER",
        "password": "Password123!",
        "confirm_password": "Password123!"
    })
    
    # Valid login
    res = client.post("/auth/login", data={
        "username": "loginuser",
        "password": "Password123!"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Welcome back, loginuser" in res.data
    
    # Log out so subsequent request isn't already authenticated
    client.get("/auth/logout")
    
    # Invalid password
    res_bad = client.post("/auth/login", data={
        "username": "loginuser",
        "password": "WrongPassword!"
    })
    assert b"Invalid credentials" in res_bad.data

def test_protected_routes(client):
    # Unauthenticated user redirected
    res = client.get("/dashboard", follow_redirects=True)
    assert res.status_code == 200
    assert b"Please authenticate" in res.data or b"Secure Login" in res.data
