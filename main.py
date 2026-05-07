from app.db.base import Base
from app.db.session import SessionLocal , engine
from app.models.user import User

Base.metadata.create_all(engine)

session = SessionLocal()

try:
    user = User(email="test@example.com",full_name="Test User")
    session.add(user)
    session.commit()
    first_user = session.query(User).first()
    print("email = ",first_user.email)
    print("created_at  = ",first_user.created_at)
    print("name = ",first_user.full_name)
finally:
    session.close()