from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./dev.db")

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)

# we dont call session here as session will be created even if we import it and cause the dataleaking...

print(sessionmaker)