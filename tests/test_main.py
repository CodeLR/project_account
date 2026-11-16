from fastapi.testclient import TestClient
from main import app

client=TestClient(app)


def test_me_without_token():
    response=client.get("/user/me")
    assert response.status_code==401

def test_login_profile():
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "string"
        }
    )

    assert response.status_code == 200

    access_tok = response.json()["access_token"]

    assert isinstance(access_tok, str)
    assert len(access_tok) > 0

def test_me_with_token():
    response = client.post(
            "/auth/login",
            json={
                "email": "user@example.com",
                "password": "string"
            }
        )
    access_tok = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_tok}"}
    profile_response = client.get("/user/me", headers=headers)
    assert profile_response.status_code == 200


def test_date_profile():
    response = client.post(
                "/auth/login",
                json={
                    "email": "user@example.com",
                    "password": "string"
                }
            )
    access_tok = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_tok}"}
    profile_response=client.get("/user/me",headers=headers)
    assert profile_response.json()["name"]=="string"
    assert response.status_code == 200


def test_login_wrong_password():
    response=client.post("/auth/login",
                     json={"email":"user@example.com",
                           "password":"wrong_password_123"})
    assert response.status_code == 401

def test_login_unknown_user():
    response=client.post("/auth/login",
                         json={"email":"unknown@example.com",
                               "password":"kick"})
    assert response.status_code == 401


def test_me_with_invalid_token():
    headers = {"Authorization": "Bearer fake_token"}
    profile_response = client.get("/user/me", headers=headers)
    assert profile_response.status_code == 401


def test_me_returns_user_data():
    
    profile_response=client.post("/auth/login",
                                 json={
                        "email": "user@example.com",
                        "password": "string"
                    })
    access_tok = profile_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {access_tok}"}
    response=client.get("/user/me",headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "user@example.com"

   
def test_login_token_type():
    response=client.post("/auth/login",
                                 json={
                        "email": "user@example.com",
                        "password": "string"
                    })
    assert response.status_code == 200
    assert response.json()["token_type"]=="bearer"
    assert isinstance(response.json()["access_token"], str)
    assert len(response.json()["access_token"]) > 0
    


def test_refresh_token():
    response=client.post("/auth/login",
                                 json={
                        "email": "user@example.com",
                        "password": "string"
                    })
    assert response.status_code == 200
    refresh_token=response.json()["refresh_token"]
    refresh_response=client.post("/auth/refresh",
                                 json={
    "refresh_token": refresh_token})
    assert refresh_response.status_code == 200
    refresh_token_new=refresh_response.json()["refresh_token"]
    refresh_access_token=refresh_response.json()["access_token"]
    assert isinstance(refresh_response.json()["access_token"], str)
    assert len(refresh_token_new) > 0
    assert len(refresh_access_token) > 0


def test_logout():
    response = client.post(
        "/auth/login",
        json={
            "email": "user@example.com",
            "password": "string"
        }
    )
    assert response.status_code == 200
    refresh_token_new = response.json()["refresh_token"]
    response_by_logout = client.post(
        "/auth/logout",
        json={"refresh_token": refresh_token_new}
    )
    assert response_by_logout.status_code == 200