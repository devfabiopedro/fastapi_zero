from sqlalchemy import func, select

from fastapi_zero.models import User


def test_create_user(session):
    new_user = User(
        username='alice',
        password='secret',
        email='teste@test',
        updated_at=func.now(),
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'alice'))

    assert user.username == 'alice'
