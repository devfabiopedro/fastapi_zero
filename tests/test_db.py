from sqlalchemy import select
from sqlalchemy.orm import Session

from fastapi_zero.database import get_session
from fastapi_zero.models import Todo, User


def test_create_user(session):
    new_user = User(username='alice', password='secret', email='teste@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'


def test_create_todo(session, user: User):
    todo = Todo(
        title='Test Todo',
        description='Test Desc',
        state='draft',
        user_id=user.id,
    )
    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))

    assert todo in user.todos


# (database) LN:10,11
def test_get_session(session, engine, mocker):
    mocker.patch('fastapi_zero.database.engine', engine)

    session_generator = get_session()
    generated_session = next(session_generator)

    assert isinstance(generated_session, Session)
    assert generated_session.bind.url == engine.url
    session_generator.close()
