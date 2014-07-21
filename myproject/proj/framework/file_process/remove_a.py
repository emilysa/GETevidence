import re
from celery import Celery
INPUT_TEXT = "file.txt"

myapp = Celery('remove_a', backend='amqp', broker='amqp://localhost')

b_file = open(INPUT_TEXT, 'r')
line = b_file.next()

newfile = open("bnn.txt", 'w')

@myapp.task
def remove_letter():
    for line in b_file:
        if 'a' in line:
            removed = line.replace("a", "")
            print removed
            newfile.write(removed)
    newfile.close()
