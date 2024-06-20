from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app

client = TestClient(app)  # Arrange


def test_read_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_olamundo_deve_retornar_template_html_escrito_Ola_Mundo():
    response = client.get('/olamundo')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert "Olá Mundo!" in response.text
