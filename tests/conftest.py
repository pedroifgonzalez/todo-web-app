import os

import pytest
from db.sqlalchemy_database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='function')
def test_db_session():
    """Creates a test database session"""
    test_database_url = 'sqlite:///./test_db_app.db'

    engine = create_engine(test_database_url, connect_args={'check_same_thread': False})
    Base.metadata.create_all(bind=engine)
    yield sessionmaker(autocommit=False, autoflush=False, bind=engine)()

    os.remove('test_db_app.db')
