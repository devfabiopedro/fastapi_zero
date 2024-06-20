from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse

from fastapi_zero.schemas import (
    Message,
    UserDB,
    UserList,
    UserPublic,
    UserSchema,
)

app = FastAPI(title='FastAPI do Zero')


database = []


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


@app.post(
    '/users/',
    tags=['Criar Usuário'],
    status_code=status.HTTP_201_CREATED,
    response_model=UserPublic,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(**user.model_dump(), id=len(database) + 1)

    database.append(user_with_id)

    return user_with_id


@app.get(
    '/users/',
    tags=['Listar Usuários'],
    status_code=status.HTTP_200_OK,
    response_model=UserList,
)
def read_users():
    return {'users': database}


@app.put('/users/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    del database[user_id - 1]

    return {'message': 'User deleted'}
