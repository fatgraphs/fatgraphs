import pytest
from be.server import create_app
from be.server import Base
from sqlalchemy import Table, Column, Integer, String

# Those are magically injected into the tests, just import a fixture and make sure the test parameter name
# matches with its name

@pytest.fixture
def app():
    return create_app("test")


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    """
    Provide a clean database to each test
    :param app:
    :return:
    """
    from be.server import SessionLocal

    with app.app_context():
        db = SessionLocal()
        Base.metadata.drop_all(db.bind)
        if not "tg_vertex_metadata" in Base.metadata.tables:
            Table(
                 "tg_vertex_metadata",
                Base.metadata,
                Column('id', Integer, primary_key=True),
                Column('vertex', String()),
                Column('type', String()),
                Column('label', String()),
                Column('description', String())
            )
        if not "tg_account_type" in Base.metadata.tables:
            Table(
                "tg_account_type",
               Base.metadata,
               Column('vertex', String(), primary_key=True),
               Column('type', String())
            )

        Base.metadata.create_all(db.bind)
        yield db
        db.commit()
        Base.metadata.drop_all(db.bind)
        db.close()


def assert_lists_equal(expected, actual):
    assert len(actual) == len(expected)
    assert all([a == b for a, b in zip(actual, expected)])
