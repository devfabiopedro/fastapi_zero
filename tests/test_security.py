from http import HTTPStatus

import jwt
import pytest
from fastapi import HTTPException
from freezegun import freeze_time
from jwt import decode

from fastapi_zero.security import (
    Session,
    create_access_token,
    get_current_user,
    settings,
)


# (security) LN: 61
def test_jwt_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token-invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


# (security) LN: 71
@pytest.mark.asyncio()
async def test_user_not_found_in_db(session: Session):
    token = jwt.encode(
        {'sub': 'Carmem'}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(session=session, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'


# (security) LN: 58,60,63,
@pytest.mark.asyncio()
async def test_missing_sub_in_token(session: Session):
    token = jwt.encode(
        {}, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )  # Token sem sub

    with pytest.raises(HTTPException) as excinfo:
        await get_current_user(session=session, token=token)

    assert excinfo.value.status_code == HTTPStatus.UNAUTHORIZED
    assert excinfo.value.detail == 'Could not validate credentials'


# (security) LN: 64
def test_token_with_expired_time_dont_refresh(client, user):
    with freeze_time('2023-07-14 12:00:00'):
        response = client.post(
            '/auth/token',
            data={'username': user.email, 'password': user.clean_password},
        )
        assert response.status_code == HTTPStatus.OK
        token = response.json()['access_token']

    with freeze_time('2023-07-14 12:31:00'):
        response = client.post(
            '/auth/refresh_token',
            headers={'Authorization': f'Bearer {token}'},
        )
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json() == {'detail': 'Could not validate credentials'}


# [ Outros Testes ]
def test_jwt():
    data = {'test': 'test'}
    token = create_access_token(data)

    decoded = decode(token, settings.SECRET_KEY, algorithms=['HS256'])

    assert decoded['test'] == data['test']
    assert decoded['exp']  # Testa se o valor de exp foi adicionado ao token


def test_get_token(client, user):
    response = client.post(
        '/auth/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert 'access_token' in token
    assert 'token_type' in token
