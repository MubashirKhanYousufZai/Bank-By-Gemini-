import pytest
from fastapi.testclient import TestClient
from main import app
import database as db_utils
import os

# Fixture to set up and tear down the test database
@pytest.fixture(autouse=True)
def test_db():
    # Use a separate test database
    test_db_file = "test_bank.db"
    # Link the main db connection to the test db
    db_utils.get_db_connection = lambda: (
        conn := db_utils.sqlite3.connect(test_db_file),
        conn.__setattr__('row_factory', db_utils.sqlite3.Row),
        conn
    )[-1]
    
    # Initialize the database with fresh data for each test
    db_utils.init_db()
    
    yield
    
    # Clean up the test database file
    db_utils.get_db_connection().close()
    os.remove(test_db_file)

client = TestClient(app)

def test_get_accounts():
    response = client.get("/api/accounts")
    assert response.status_code == 200
    data = response.json()
    assert "Ali" in data
    assert "Mubashir" in data
    assert "Aliyan" in data
    assert data["Ali"]["balance"] == 5000

def test_successful_transfer():
    response = client.post(
        "/api/transfer",
        json={"sender": "Ali", "receiver": "Me", "amount": 1000},
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully transferred 1000.0 from Ali to Me."}

    accounts = db_utils.get_accounts()
    assert accounts["Ali"]["balance"] == 4000
    assert accounts["Me"]["balance"] == 2000

def test_insufficient_funds():
    response = client.post(
        "/api/transfer",
        json={"sender": "Me", "receiver": "Ali", "amount": 2000},
    )
    assert response.status_code == 400
    assert "Insufficient funds" in response.json()["detail"]

def test_sender_not_found():
    response = client.post(
        "/api/transfer",
        json={"sender": "NonExistent", "receiver": "Me", "amount": 100},
    )
    assert response.status_code == 400
    assert "Sender 'NonExistent' not found" in response.json()["detail"]

def test_receiver_not_found():
    response = client.post(
        "/api/transfer",
        json={"sender": "Ali", "receiver": "NonExistent", "amount": 100},
    )
    assert response.status_code == 400
    assert "Receiver 'NonExistent' not found" in response.json()["detail"]

def test_same_sender_receiver():
    response = client.post(
        "/api/transfer",
        json={"sender": "Ali", "receiver": "Ali", "amount": 100},
    )
    assert response.status_code == 400
    assert "Sender and receiver cannot be the same" in response.json()["detail"]

def test_negative_amount():
    response = client.post(
        "/api/transfer",
        json={"sender": "Ali", "receiver": "Me", "amount": -100},
    )
    assert response.status_code == 400
    assert "Transfer amount must be positive" in response.json()["detail"]

def test_zero_amount():
    response = client.post(
        "/api/transfer",
        json={"sender": "Ali", "receiver": "Me", "amount": 0},
    )
    assert response.status_code == 400
    assert "Transfer amount must be positive" in response.json()["detail"]
