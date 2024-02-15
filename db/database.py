from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from configs import Database


SQLALCHEMY_DATABASE_URL = Database.DATABASE_URL
engine_config = {
    "url": SQLALCHEMY_DATABASE_URL,
    "pool_size": 10,
    "max_overflow": 0,
    "echo": True,
}

engine = create_engine(**engine_config)
session_config = {"autoflush": True, "bind": engine, "echo": True}
SessionLocal = sessionmaker(**session_config)
session = scoped_session(sessionmaker(bind=engine))
session.expunge_all()

Base = declarative_base()
Base.query = session.query_property()
