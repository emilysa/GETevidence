###Clone the Git repository###
Navigate to the directory you want to have the code in, and clone the repository with: `git clone git://github.com/emilysa/SummerProject`
###Install pip, virtualenv, and virtualenvwrapper###
(Root user action) Install pip:  `sudo apt-get install python-pip`
(Root user action) Use pip to install virtualenv and virtualenvwrapper: `sudo pip install virtualenv virtualenvwrapper`
###Set up virtualenv and virtualenvwrapper###
Make a directory to store your virtual environments: `mkdir ~/.virtualenvs`
To make virtualenv and virtualenvwrapper commands work in future terminals, add the following to your bashrc (or zshrc, as appropriate): `export WORKON_HOME=$HOME/.virtualenvs ~/.virtualenvs` and `source /usr/local/bin/virtualenvwrapper.sh`.
###Make a virtual environment and install required Python packages###
If you open a new terminal you should now be able to access the virtualenvwrapper commands listed below.
If you aren't familiar with pip and virtualenv: these are standard aspects of Python development, greatly facilitating package management. Whenever working on this software you should do so within the virtual environment (e.g. after performing step 2 below).
Create a new virtual environment for working on this code: `mkvirtualenv summer`
Start using this virtual environment: `workon summer`
###Pip Install###
There are Python Packages outlined in the requirements.txt file.  Install them.  Make sure your virtualenv is running and you're in the requirements.txt level of the directory first (workon summer if it’s not) then: `pip install -r requirements.txt`
###RabbitMQ###
What: Celery requires a message broker. This broker acts a middleman sending and receiving messages to Celery workers who in turn process tasks as they receive them. Celery recommends using RabbitMQ.  RabbitMQ is open source message broker software (sometimes called message-oriented middleware) that implements the Advanced Message Queuing Protocol (AMQP).

Installation/Server: `sudo apt-get install rabbitmq-server`
Ubuntu automatically begins running a rabbit server in the background once this is installed.  If you want the server to be in the foreground, you will need to stop the original server and start a new server in the foreground.
Starting the server is as simple as: rabbitmq-server (runs in the foreground), or you can start it in the background with rabbitmq-server -detached. To stop the server use rabbitmqctl stop.
###Celery###
What: Celery is an asynchronous Python task queue/job queue based on distributed message passing.

Installation/Launch:
Celery was already installed at the beginning as one of the Python Packages in the requirements.txt file.
To launch Celery from the project/directory, run `celery -A celery worker -l debug`
Or to launch Celery in the background, run `celery multi start testing -l info`
###Django###
What: Django is a high-level Python Web framework that encourages rapid development and clean, pragmatic design.

Installation/Launch:
Django was already installed at the beginning, since it was included in the requirements.txt file.
At this point, you are going to want to sync the database which you can do with `python manage.py syncdb`
You can run the Django server with `python manage.py runserver 0.0.0.0:8000`. This is the development server and works with virtualenv as it opens all the ports.
