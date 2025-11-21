import pytest
from src.flask_learn.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"Log In" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b"href='/update/1'" in response.data


@pytest.mark.parametrize(
    ('path', 'method'),
    (
        ('/create', 'POST'),
        ('/update/1', 'POST'),
        ('/delete/1', 'DELETE'),
    ),
)
def test_login_required(client, path, method):
    if method == 'POST':
        response = client.post(path)
    else:
        response = client.delete(path)
    assert response.headers["Location"] == "/auth/login"


@pytest.mark.parametrize(
    ('path', 'method'),
    (
        ('/update/2', 'POST'),
        ('/delete/2', 'DELETE'),
    ),
)
def test_exists_required(client, auth, path, method):
    auth.login()
    if method == 'POST':
        response = client.post(path)
    else:
        response = client.delete(path)
    assert response.status_code == 403
