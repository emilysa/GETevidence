from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'proj.settings')

# instantiate Celery object
myapp = Celery(include=[
                        'framework.file_process.remove_a'
                        'framework.tasker.tasks'
                        ])

# import celery config file
myapp.config_from_object('celeryconfig')
myapp.config_from_object('django.conf:settings')
myapp.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@myapp.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

if __name__ == '__main__':
    celery.start()
