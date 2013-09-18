from .settings import *  # noqa

TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = os.path.join(BASE_DIR, os.pardir)
TEST_DISCOVER_ROOT = os.path.join(TEST_DISCOVER_TOP_LEVEL, 'tests')

INSTALLED_APPS += (
    'tests',
)

REST_FRAMEWORK['TEST_REQUEST_DEFAULT_FORMAT'] = 'json'
