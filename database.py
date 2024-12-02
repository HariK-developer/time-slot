from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from config import db_settings
from urllib.parse import quote_plus


SQL_ALCHEMY_DATABASE_URL = f"postgresql://{db_settings.db_username}:{quote_plus(db_settings.db_password)}@{db_settings.db_host}:{db_settings.db_port}/{db_settings.db_name}"

# * Database engine instance to connect
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, pool_size=100, max_overflow=-1)

# * Instance of this SessionLocal will be a database session
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

# * Database models are created by inheriting this class,
# * Inheriting the class allows sqlalchemy to migrate new models to database automatically
Base = declarative_base()


# * path operations can use this function as dependency to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
