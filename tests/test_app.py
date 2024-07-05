from http import HTTPStatus

import jwt
import pytest
from fastapi import HTTPException

from fastapi_zero.schemas import UserPublic
from fastapi_zero.security import Session, get_current_user, settings


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_olamundo_deve_retornar_template_html_escrito_Ola_Mundo(client):
    response = client.get('/olamundo')
    assert response.status_code == HTTPStatus.OK
    assert 'Olá Mundo!' in response.text


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'alice',
        'email': 'alice@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [], 'total': 0}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema], 'total':1}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_if_user_not_found_on_put_403(client, token):
    response = client.put(
        '/users/0',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'john',
            'email': 'john@example.com',
            'password': '2mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_one_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_if_user_not_found_on_delete_403(client, token):
    response = client.delete(
        '/users/0', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_if_user_not_exist_404(client, user):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_create_new_user_verify_if_username_exists(client, user):
    new_user_data = {
        'username': user.username,
        'email': 'newteste@test.com',
        'password': 'newpassword',
    }
    response = client.post('/users', json=new_user_data)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Username already exists'}


def test_create_new_user_verify_if_email_exists(client, user):
    new_user_data = {
        'username': 'NewTeste',
        'email': user.email,
        'password': 'newpassword',
    }
    response = client.post('/users', json=new_user_data)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Email already exists'}


@pytest.mark.asyncio()
async def test_user_not_found_in_db(session: Session):
    token = jwt.encode(
        {'sub': 'Carmem'}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(session=session, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'


@pytest.mark.asyncio()
async def test_missing_sub_in_token(session: Session):
    token = jwt.encode(
        {}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )  # Token sem sub

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(session=session, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'


def test_when_generate_token_if_incorrect_email(client, user):
    wrong_email = 'carmen@email.com'

    response = client.post(
        '/auth/token',
        data={'username': wrong_email, 'password': user.password},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_when_generate_token_if_incorrect_password(client, user):
    wrong_pass = 'passwrong'

    response = client.post(
        '/auth/token', data={'username': user.email, 'password': wrong_pass}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Incorrect email or password'}


def test_read_users_empty(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json() == {'users': [], 'total': 0}