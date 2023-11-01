import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

password_location = os.environ.get("POSTGRES_PASSWORD_LOC")
in_docker = os.environ.get("IN_DOCKER") == "True"

if in_docker:
    with open(password_location) as f:
        db_password = f.read()
else:
    db_password = os.environ.get("POSTGRES_PASSWORD")

db_host = os.environ.get("DOCKER_HOST", "localhost")

# SQLALCHEMY_DATABASE_URL = "sqlite:///../sql_app.db"
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )

SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:{db_password}@{db_host}/openodha"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
