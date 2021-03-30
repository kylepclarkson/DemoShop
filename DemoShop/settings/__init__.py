from .base import *

env_name = os.getenv('ENV_NAME', 'local')

if env_name == 'prod':
    from .live import *
else:
    from .local import *
