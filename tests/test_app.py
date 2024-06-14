from http import HTTPStatus

from fastapi.testclient import TestClient

from fastapi_zero.app import app

client = TestClient(app)  # Arrange


def test_read_root_deve_retornar_ok_e_ola_mundo():
    response = client.get('/')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_navegar_page1_deve_retornar_mensagem_lendo_pagina1():
    response = client.get('/page1')  # Act
    assert response.status_code == HTTPStatus.OK  # Assert
    assert response.json() == {'message': 'Lendo Página 1'}  # Assert
