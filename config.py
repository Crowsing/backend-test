from environs import Env

env = Env()

env.read_env()

with env.prefixed("TEST_APP_"):
    CORS_HEADERS = 'Content-Type'
    OPENAI_API_KEY = env.str("OPENAI_API_KEY")
    MAX_TOKENS = env.int("MAX_TOKENS", 500)
    MODEL = env.str("MODEL", "gpt-3.5-turbo-instruct")

    class BaseConfig(object):
        PROJECT = "test-py"
        DEBUG = False
        TESTING = False
        SECRET_KEY = env.str("SECRET_KEY")

    class TestConfig(BaseConfig):
        DEBUG = True
        TESTING = True
        PRESERVE_CONTEXT_ON_EXCEPTION = False
        WTF_CSRF_ENABLED = False

