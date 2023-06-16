from logging import getLogger, FileHandler, Formatter

log = getLogger('database_log')
log.setLevel('DEBUG')

log_handler = FileHandler('main.log', 'a+')
log_handler.setFormatter(Formatter("%(name)s %(asctime)s %(levelname)s %(message)s"))


log.addHandler(log_handler)
