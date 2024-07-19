from http import HTTPStatus


# (app) LN: 20
def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


# (app) LN: 29
def test_olamundo_deve_retornar_template_html_escrito_Ola_Mundo(client):
    response = client.get('/olamundo')
    assert response.status_code == HTTPStatus.OK
    assert 'Olá Mundo!' in response.text
