"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ,path
from config.filesystem import Mycro
import os
import json
import logging

folder_path = os.getcwd()
mycro = Mycro('gunicorn')

if path.isfile(f'{folder_path}/mycro.json'):
    with open(f'{folder_path}/mycro.json') as json_file:
        data = json.load(json_file)
        try:
            mycro = data['gunicorn']
        except Exception as err:
            app.logger.info(bcolors.FAIL+'Key "gunicorn" does not exist, error: '+str(err)+bcolors.ENDC)
else:
    app.logger.info(bcolors.FAIL+'mycro.json file does not exist'+bcolors.ENDC)
    sys.exit()

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#SSL
# keyfile = "ssl.key"
# certfile = "ssl.crt"
# ssl_version = "TLS"

#Security
limit_request_line = mycro.get('limit_request_line')
limit_request_fields = mycro.get('limit_request_fields')

#Server Socket
bind = '{}:{}'.format(mycro.get('host'),mycro.get('port'))

#Server Mechanics
preload_app = mycro.get('preload_app')
daemon = mycro.get('daemon')
user = mycro.get('user')

#Debugging
reload = mycro.get('reload')
reload_extra_files = mycro.get('reload_extra_files')

#Logging
accesslog = mycro.get('accesslog')
errorlog = mycro.get('errorlog')
loglevel = mycro.get('loglevel') #debug info warning error critical
capture_output= mycro.get('capture_output')
logger_class = mycro.get('logger_class')
# syslog_addr = "tcp://HOST:PORT" #for TCP sockets
syslog = mycro.get('syslog')
access_log_format = mycro.get('access_log_format') #https://docs.gunicorn.org/en/latest/settings.html#access-log-format

#Worker Processes
max_requests = mycro.get('max_requests')
worker_class = mycro.get('worker_class') #pip install gunicorn[eventlet]
workers = mycro.get('workers')

def when_ready(server):
    logging.info('{} Gunicorn is running on http://{} {}'.format(bcolors.OKGREEN,bind,bcolors.ENDC))

def on_starting(server):
    logging.info(bcolors.OKGREEN+'Initializing Gunicorn'+bcolors.ENDC)

def on_reload(server):
    logging.info(bcolors.OKGREEN+'Restoration of the gunicorn process has been performed...'+bcolors.ENDC)

def pre_request(worker, req):
    worker.log.debug("%s %s" % (req.method, req.path))

def worker_exit(server, worker):
    logging.info(bcolors.WARNING+f'Worker exiting {worker}'+bcolors.ENDC)

def on_exit(server):
    logging.info(bcolors.WARNING+f'Process finished successfully'+bcolors.ENDC)
