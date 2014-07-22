from __future__ import absolute_import
from datetime import datetime
import os

from celery import shared_task
from django.conf import settings

@shared_task
def timestamp():
    LOGFILE = os.path.join(settings.MEDIA_ROOT, 'stamped_log_file.txt')
    with open(LOGFILE, 'a') as logfile:
        datetime_str = str(datetime.now()) + '\n'
        logfile.write(datetime_str)
