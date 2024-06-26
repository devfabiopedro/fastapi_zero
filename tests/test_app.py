from http import HTTPStatus

from fastapi_zero.schemas import UserPublic


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
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user):
    response = client.put(
        '/users/1',
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
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}


def test_if_user_not_found_on_put_404(client, user):
    response = client.put(
        '/users/2',
        json={
            'username': 'john',
            'email': 'john@example.com',
            'password': '2mynewpassword',
        },
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_one_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()
    response = client.get('/users/1')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_if_user_not_found_on_delete_404(client, user):
    response = client.delete('/users/2')
    assert response.status_code == HTTPStatus.NOT_FOUND


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
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Username already exists'}


def test_create_new_user__verify_if_email_exists(client, user):
    new_user_data = {
        'username': 'NewTeste',
        'email': user.email,
        'password': 'newpassword',
    }
    response = client.post('/users', json=new_user_data)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Email already exists'}
