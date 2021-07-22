import pytest
from be.server import create_app
from be.server import Base

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
        Base.metadata.create_all(db.bind)
        yield db
        db.commit()
        Base.metadata.drop_all(db.bind)
        db.close()

