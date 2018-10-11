import flask
import pytest
from rest.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def post_primes(client, start, end):
    return client.post('/primes', data=dict(
        start_num=start,
        end_num=end
    ))


def test_primes(client):
    rv = post_primes(client, 4, 11)
