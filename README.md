SummerProject
=============
Welcome to Emily's Django rewrite of GET-Evidence, a work in progress. 
This is a summer project to recreate the functionality of the current GET-Evidence.

Installation
------------
These instructions were written for Ubuntu Linux.

### Clone the Git repository ###

* Navigate to the directory you want to have the code in, and clone the 
repository with: `git clone git://github.com/emilysa/SummerProject`.

### Install pip, virtualenv, and virtualenvwrapper ###

1. **(Root user action)** Install pip: `sudo apt-get install python-pip` 
2. **(Root user action)** Use pip to install virtualenv and virtualenvwrapper: `sudo pip install virtualenv virtualenvwrapper`.

### Set up virtualenv and virtualenvwrapper ###

1. Make a directory to store your virtual environments: `mkdir ~/.virtualenvs`
2. To make virtualenv and virtualenvwrapper commands work in future terminals, add the 
following to your bashrc (or zshrc, as appropriate): 
`export WORKON_HOME=$HOME/.virtualenvs` and
`source /usr/local/bin/virtualenvwrapper.sh`.

### Make a virtual environment and install required Python packages ###

If you open a new terminal you should now be able to access the virtualenvwrapper commands listed below.

If you aren't familiar with pip and virtualenv: these are standard aspects of Python development,
greatly facilitating package management. Whenever working on this software you should do so within
the virtual environment (e.g. after performing step 2 below).

1. Create a new virtual environment for working on this code: `mkvirtualenv summer`
2. Start using this virtual environment: `workon summer`
3. Navigate to top directory in this project. (One of the subdirectories
should be "requirements".) Install the Python packages required for development with 
`pip install -r requirements/dev.txt`.

### Set up rabbitmq###

Celery requires a message broker. This broker acts a middleman sending and receiving messages to Celery workers
who in turn process tasks as they receive them.  Celery recommends using RabbitMQ.

1. Install RabbitMQ: `sudo apt-get install rabbitmq-server`
2. Once installed, starting the server is as simple as: `rabbitmq-server` or you can start it in the background
with `rabbitmq-server -detached`.  To stop the server use `rabbitmqctl-stop`

### Launch Celery ###

To launch celery, from the project/directory run:

1. `celery -A framework.celery.celery worker -l debug` or 
2. `celery multi start testing -l info` to run celery in the background.

You **should** be able to run the program at this point, but this project is still in progress so is not yet functional.
