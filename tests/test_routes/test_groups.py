"""
Main API Group Tests - with TestDB in Test Environment
"""

import json
import pytest
from app.db.repositories import grouprepository

#pytestmark = pytest.mark.asyncio


@pytest.fixture(scope='module')
def test_request_group():
    return {
        'name': 'test post name',
        'description': 'test post description'
    }


@pytest.fixture(scope='module')
def test_group():
    return {
        'id': 1,
        'name': 'test get name',
        'description': 'test get description'
    }


def test_create_group(test_app, monkeypatch, test_request_group):
    async def mock_post(group):
        return 1

    monkeypatch.setattr(grouprepository, 'create', mock_post)

    response = test_app.post(
        '/api/v1/groups/', data=json.dumps(test_request_group))

    assert response.status_code == 201
    assert response.json()['id'] > 0
    assert response.json()['name'] == test_request_group['name']
    assert response.json()['description'] == test_request_group['description']


def test_create_group_invalid_data(test_app):
    response = test_app.post('/api/v1/groups/', data=json.dumps({
        'name': 'test invalid',
    }))
    assert response.status_code == 422

    response = test_app.post('/api/v1/groups/', data=json.dumps({
        'name': '',
        'description': '',
    }))
    assert response.status_code == 422


def test_get_group(test_app, monkeypatch, test_request_group, test_group):
    async def mock_get(id):
        return test_group

    async def mock_post(group):
        return 1

    monkeypatch.setattr(grouprepository, 'create', mock_post)
    monkeypatch.setattr(grouprepository, 'get', mock_get)

    post_response = test_app.post(
        '/api/v1/groups/', data=json.dumps(test_request_group))
    response = test_app.get(
        "/api/v1/groups/{}".format(post_response.json()['id']))
    assert response.status_code == 200
    assert response.json()['id'] > 0
    assert response.json()['name'] == test_request_group['name']
    assert response.json()['description'] == test_request_group['description']


def test_remove_group_by_incorrect_id(test_app):
    response = test_app.delete('/api/v1/groups/-1')
    assert response.status_code == 204


def test_remove_group_unstable(test_app):
    response = test_app.delete('/api/v2/groups/1')
    assert response.status_code == 404


def test_create_group_unstable(test_app, test_request_group):
    response = test_app.post(
        '/api/v2/groups/', data=json.dumps(test_request_group))
    assert response.status_code == 404


def test_ping(test_app):
    response = test_app.get('/api/v1/groups/ping')
    assert response.status_code == 200
    assert response.json() == {'ping': 'pong'}
