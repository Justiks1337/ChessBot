from logging import getLogger, Formatter, FileHandler
from os import path

log = getLogger(path.join(path.dirname(__file__), 'django_log'))
log.setLevel('DEBUG')

log_handler = FileHandler(path.join(path.dirname(__file__), 'main.log'), 'a+')
log_handler.setFormatter(Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))


log.addHandler(log_handler)
