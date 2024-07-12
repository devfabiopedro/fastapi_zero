from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


# (users) LN: 32,50,52,55,56,57,59
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


# (users) LN: 69, 70, 71
def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [], 'total': 0}


# (users) LN: 105,111, 112, 113, 114, 115, 117 / (auth) LN:29,31,37,43,45
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


# (users) LN: 128,134,135,137
def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


# (users) LN: 82,84,89
def test_get_one_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


# (users) LN: 85
def test_if_user_not_exist_404(client, user):
    response = client.get('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND


# (users) LN: 39,40
def test_create_new_user_verify_if_username_exists(client, user):
    new_user_data = {
        'username': user.username,
        'email': 'newteste@test.com',
        'password': 'newpassword',
    }
    response = client.post('/users', json=new_user_data)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Username already exists'}


# (users) LN:44,45
def test_create_new_user_verify_if_email_exists(client, user):
    new_user_data = {
        'username': 'NewTeste',
        'email': user.email,
        'password': 'newpassword',
    }
    response = client.post('/users', json=new_user_data)
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Email already exists'}


# (users) LN: 106
def test_update_user_with_wrong_user(client, other_user, token):
    response = client.put(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


# (users) LN: 129
def test_delete_user_with_wrong_user(client, other_user, token):
    response = client.delete(
        f'/users/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Not enough permissions'}


# [ Outros Testes ]
def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema], 'total': 1}


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


def test_if_user_not_found_on_delete_403(client, token):
    response = client.delete(
        '/users/0', headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_when_generate_token_if_incorrect_user(client, user):
    wrong_username = 'carmen'

    response = client.post(
        '/auth/token',
        data={'username': wrong_username, 'password': user.password},
    )
    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'detail': 'Forbidden'}


def test_read_users_empty(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [], 'total': 0}
