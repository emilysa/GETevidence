from celery import Celery
from datetime import datetime

LOGFILE = 'stamp_log_file.txt'

myapp = Celery('stamp_log', backend='amqp', broker='amqp://localhost')

@myapp.task
def stamp_with_datetime():
    with open(LOGFILE, 'a') as logfile:
        datetime_str = str(datetime.now()) + '\n'
        logfile.write(datetime_str)
