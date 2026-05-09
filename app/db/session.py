from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///./dev.db")

SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind = engine)

# we dont call session here as session will be created even if we import it and cause the dataleaking...


#To organize your code professionally, use sessionmaker to create a central "factory" that produces pre-configured sessions,
#then use the with statement to ensure each session is safely closed after use. This pattern separates your database configuration (the Engine) from your application logic (the Session),
#making your code cleaner and preventing connection leaks.

#-----[example code]----- 

#from sqlalchemy import create_engine
#from sqlalchemy.orm import sessionmaker, Session

# 1. Setup: Create the 'Factory' (Do this once)
#engine = create_engine("sqlite:///myapp.db")
#SessionLocal = sessionmaker(bind=engine)

# 2. Usage: Get a session from the factory whenever needed
#with SessionLocal() as session:
#    new_user = User(name="Bob")
#    session.add(new_user)
#    session.commit() 
# Session is automatically closed here!

