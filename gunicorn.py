"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count
from os import environ
import logging

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


def max_workers():
    return 4 #cpu_count()


#SSL
# keyfile = "ssl.key"
# certfile = "ssl.crt"
# ssl_version = "TLS"

#Security
limit_request_line = 4094
limit_request_fields = 100

#Server Socket
bind = 'localhost:7000'

#Server Mechanics
preload_app = True
daemon = False
user = 'root'

#Debugging
reload = True 
reload_extra_files = []

#Logging
accesslog = 'accesslog.txt'
errorlog = "logfile.txt"
loglevel = 'info' #debug info warning error critical
capture_output= False
logger_class = "gunicorn.glogging.Logger"
# syslog_addr = "tcp://HOST:PORT" #for TCP sockets
syslog = True
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"' #https://docs.gunicorn.org/en/latest/settings.html#access-log-format

#Worker Processes
max_requests = 1000
worker_class = 'eventlet' #pip install gunicorn[eventlet]
workers = max_workers()

def when_ready(server):
    logging.info(bcolors.OKGREEN+'Gunicorn is running in '+bcolors.ENDC)
    

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
