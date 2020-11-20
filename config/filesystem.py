import os, sys
import json
from os import path
from config.config import bcolors, app
import getpass
import platform
import json
import subprocess

folder_path = os.getcwd()
path_service_logfile = '{}/.mycro'.format(folder_path)

def mycrojson():
    if path.isfile('{}/mycro.json'.format(folder_path)):
        with open('{}/mycro.json'.format(folder_path)) as json_file:
            data = json.load(json_file)
            return(data)
    else:
        app.logger.info(bcolors.FAIL+'mycro.json file does not exist'+bcolors.ENDC)
        sys.exit()
        return None
    
def updateMycroJson(obj):
    with open('{}/mycro.json'.format(folder_path), "w") as jsonFile:
        json.dump(obj, jsonFile,indent=4)


class Switcher(object):
    def __init__(self):
        self._value = None 
        self._name = None

    def get(self, argument, value, name):
        """Dispatch method"""
        self._value = value
        self._name = name
        method = getattr(self, str(argument), lambda: app.logger.info(bcolors.FAIL+'filesystem > Switcher > Invalid Method'+bcolors.ENDC))
        return method()
 
    def unit(self):
        file = open("/etc/systemd/system/{}.service".format(self._name.replace(' ','_')), "a")
        file.write("[Unit]\n")
        [file.write("{key}={value}\n".format(key,value)) for key, value in self._value.items()]
        
        file.write("\n")
        file.close()
        return True
 
    def install(self):
        file = open("/etc/systemd/system/{}.service".format(self._name.replace(' ','_')), "a")
        file.write("[Install]\n")
        [file.write("{key}={value}\n".format(key,value)) for key, value in self._value.items()]

        file.write("\n")
        file.close()
        return True
 
    def service(self):
        file = open("/etc/systemd/system/{}.service".format(self._name.replace(' ','_')), "a")
        file.write("[Service]\n")
        [file.write("{key}={value}\n".format(key,value)) for key, value in self._value.items()]

        file.write("\n")
        file.close()
        return True


def makeDaemon(name): 
    if name:

        if platform.system() != 'Linuxs':
            switcher = Switcher()
            mycro_json = mycrojson()
            mycro_json['daemon']['name'] = name.replace(' ','_')
            file = open("{}.service".format(name.replace(' ','_')), "w")
            file.write("")
            file.close()
            for key, value in mycro_json['daemon'].items():
                if key != 'name':
                    (switcher.get(key, value, name))
            # daemon_reload = subprocess.run(["systemctl daemon-reload"], check=True)
            # enable_daemon = subprocess.run(["ifconfig"], check=True)
            # if enable_daemon.returncode:
            #     print(enable_daemon.returncode)

            
            
        else:
            app.logger.info(bcolors.WARNING+'We cannot run this script on windows, try on Linux'+bcolors.ENDC)

        updateMycroJson(mycro_json)
    else:
        app.logger.info(bcolors.WARNING+'Please, write the name of the daemon using parameter "-n" '+bcolors.ENDC)

def Mycro(argument):
    switcher = mycrojson()
    return switcher.get(argument, "ERROR['Mycro'] > {} Invalid key '{}'".format(bcolors.FAIL,argument,bcolors.ENDC))

def init():
    if os.path.exists(path_service_logfile):
        pass
    else:
        os.mkdir(path_service_logfile)
        os.mkdir(path_service_logfile+'/logs')
    return True
    # if not os.path.exists('/tmp/test'):

