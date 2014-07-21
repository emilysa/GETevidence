from __future__ import absolute_import

"""
In this directory, run:
   celery -A stamp_log worker -l debug

Then in python in the same directory:
   from stamp_log import stamp_with_datetime
   stamp_with_datetime.delay()

This writes the timestamp to "stamp_log_file.txt"
in this same directory.
"""

from celery import Celery
from datetime import datetime

LOGFILE = 'stamp_log_file.txt'

myapp = Celery('stamp_log', backend='amqp', broker='amqp://localhost')

@myapp.task
def stamp_with_datetime():
    with open(LOGFILE, 'a') as logfile:
        datetime_str = str(datetime.now()) + '\n'
        logfile.write(datetime_str)
