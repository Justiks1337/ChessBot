import os
from logging import getLogger, FileHandler, Formatter, basicConfig

basicConfig(level='DEBUG')

log_handler = FileHandler(os.path.join(os.path.dirname(__file__), 'main.log'), 'a+')
log_handler.setFormatter(Formatter("%(name)s %(asctime)s %(levelname)s %(message)s %(exc_info)s %(lineno)s"))

log = getLogger('django_log')
log.addHandler(log_handler)
log.setLevel('DEBUG')

asyncio_log = getLogger('asyncio')
asyncio_log.setLevel('DEBUG')
asyncio_log.addHandler(log_handler)

log.info('logging successful started')
