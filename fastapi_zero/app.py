from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import Message

app = FastAPI(title='FastAPI do Zero')


@app.get(
    '/',
    tags=['Endpoint Raiz'],
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
def read_root():
    return {'message': 'Olá Mundo!'}


@app.get(
    '/olamundo',
    tags=['Endpoint Olá Mundo HTML'],
    status_code=status.HTTP_200_OK,
    response_class=HTMLResponse,
)
def ola_mundo_html():
    return """
    <html>
        <head>
            <title>Nosso Olá Mundo</title>
        </head>
        <body>
            <h2>Olá Mundo!</h2>
        </body>
    </html>
    """
