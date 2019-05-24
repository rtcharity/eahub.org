import environ
import pytest


env = environ.Env()


#@pytest.fixture(scope="session", params=env.list("BROWSERS"))
#def session_capabilities(request, session_capabilities):
#    session_capabilities["browserName"] = request.param
#    return session_capabilities
