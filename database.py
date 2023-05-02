from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

# postgre sql database connection
user = "postgres"
# password: mysecretpassword
password = "mysecretpassword"
# database: oslab
database = "oslab"
# host: 172.17.0.4
host = "172.17.0.4"
# port: 5432

SQLALCHEMY_DATABASE_URL = f"postgresql://{user}:{password}@{host}/{database}"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
