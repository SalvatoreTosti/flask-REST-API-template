import os
import base64
from app import app, db
import test.setup as setup

TEST_DB = "test.db"


def test_setup(testCase):
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    app.config["DEBUG"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), TEST_DB
    )
    testCase.app = app.test_client()
    db.drop_all()
    db.create_all()
    setup.run()
    testCase.assertEqual(app.debug, False)


def generate_auth_header(username, password):
    byte_string = str(username + ":" + password).encode()
    return {
        "content-type": "application/json",
        "Authorization": "Basic {}".format(
            base64.b64encode(byte_string).decode("utf8")
        ),
    }
