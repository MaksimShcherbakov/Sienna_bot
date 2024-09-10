from sqlalchemy import create_engine, Column, Integer, Boolean, String
from sqlalchemy.orm import scoped_session, declarative_base, sessionmaker

from constants import DATABASE_URL

engine = create_engine(DATABASE_URL)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    name = Column(String)
    admin = Column(Boolean, default=False)

Base.metadata.create_all(bind=engine)