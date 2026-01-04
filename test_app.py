from os import getenv
from dotenv import load_dotenv
import pytest
from fastapi.testclient import TestClient
from sqlmodel import create_engine, Session, SQLModel, StaticPool
from api import app, get_one_session, Task

load_dotenv()

if getenv("TEST_DATABASE_URL") is None:
    raise ValueError("TEST_DATABASE_URL env var cannot be None ... please create it.")

test_engine = create_engine(
    getenv("TEST_DATABASE_URL"),
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
)


def get_one_test_session():
    with Session(test_engine) as session:
        yield session


app.dependency_overrides[get_one_session] = get_one_test_session

client = TestClient(app)


@pytest.fixture(autouse=True)  # autouse is VERY IMPORTANT.
def db_operations():
    SQLModel.metadata.create_all(test_engine)
    with Session(test_engine) as session:
        tasks = [
            Task(id=1, title=" messy TITLE ", description=" something "),
            Task(id=3, title=" another TITLE", description="", completed=True),
            Task(title="something"),
        ]
        session.add_all(tasks)
        session.commit()
    yield
    SQLModel.metadata.drop_all(test_engine)


def test_create_one_task():
    request = client.post(
        getenv("API_URL"),
        json={"title": " messy TITLE ", "description": " some description "},
    )
    data = request.json()

    assert request.status_code == 200
    assert data["id"] is not None
    assert data["title"] == "Messy title"
    assert data["description"] == " some description "
    assert not data["completed"]


def test_read_one_task():
    request = client.get(f'{getenv("API_URL")}3')
    data = request.json()
    assert request.status_code == 200
    assert data["title"] == " another TITLE"
    assert data["description"] == ""
    assert data["completed"]


def test_read_all_tasks():
    request = client.get(f"{getenv("API_URL")}")
    data = request.json()
    assert request.status_code == 200
    assert len(data) == 3
    assert data[2]["title"] == "something"
    assert data[2]["id"] == 4


def test_update_one_task():
    request = client.patch(f"{getenv('API_URL')}1", json={"title": "UPDATED title"})
    data = request.json()

    assert request.status_code == 200
    assert data["title"] == "Updated title"
    assert data["description"] == " something "
    assert not data["completed"]


def test_delete_one_task():
    request = client.delete(f'{getenv("API_URL")}1')
    data = request.json()

    assert request.status_code == 200
    assert data["status"] == "ok"
