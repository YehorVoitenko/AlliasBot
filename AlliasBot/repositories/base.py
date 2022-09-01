from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite://', echo=True, future=True)

Session = sessionmaker(bind=engine)
Base = declarative_base()
