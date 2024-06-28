from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import User
from fastapi_zero.schemas import Message, UserList, UserPublic, UserSchema

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
    tags=['Olá Mundo HTML'],
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
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Username already exists',
            )
        elif db_user.email == user.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Email already exists',
            )

    db_user = User(
        username=user.username, password=user.password, email=user.email
    )
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get(
    '/users/',
    tags=['Listar todos os Usuários'],
    status_code=status.HTTP_200_OK,
    response_model=UserList,
)
def read_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return {'users': users}


@app.get(
    '/users/{user_id}',
    tags=['Listar um Usuário'],
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
def read_one_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where((User.id == user_id)))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    return user


@app.put(
    '/users/{user_id}',
    tags=['Alterar dados do Usuário'],
    status_code=status.HTTP_200_OK,
    response_model=UserPublic,
)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    db_user.username = user.username
    db_user.password = user.password
    db_user.email = user.email
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete(
    '/users/{user_id}',
    tags=['Exclusão de Usuário'],
    status_code=status.HTTP_200_OK,
    response_model=Message,
)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='User not found'
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'User deleted'}
