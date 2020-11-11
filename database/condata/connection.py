import urllib.parse
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import os
import configparser
# from mysql.connector import (connection)
# import MySQLdb 
import pyodbc


config = configparser.ConfigParser()
config.read('.env')
configurate = config['DATABASE']
# test = 'DB_CONNECTION' in configurate#config['DATABASE']['DB_CONNECTION']
# db_connection = str(configurate.get('DB_CONNECTION'))


DB_CONNECTION = str(configurate.get('DB_CONNECTION'))
DB_DRIVER = str(configurate.get('DB_DRIVER'))
DB_HOST = str(configurate.get('DB_HOST'))
DB_DATABASE = str(configurate.get('DB_DATABASE'))
DB_USERNAME = str(configurate.get('DB_USERNAME'))
DB_PASSWORD = str(configurate.get('DB_PASSWORD'))


class connection_string():
    def __init__(self,db_driver=DB_DRIVER,db_host=DB_HOST,db_database=DB_DATABASE,db_user=DB_USERNAME,db_password=DB_PASSWORD, action=True):
        self.__db_driver = db_driver
        self.__db_host = db_host
        self.__db_database = db_database
        self.__db_user = db_user
        self.__db_password = db_password
        self.__action = action

    def mssql(self):

        return 'DRIVER={'+ self.__db_driver+'};SERVER='+self.__db_host+';DATABASE='+self.__db_database+';UID='+self.__db_user+';PWD='+self.__db_password

    def postgres(self):

        return 'DRIVER={'+ self.__db_driver+'};SERVER='+self.__db_host+';DATABASE='+self.__db_database+';UID='+self.__db_user+';PWD='+self.__db_password+';PORT=5432'
        
    def mysql(self):
        """Para realizar la conexion a la base de datos se utiliza el modulo MySQLdb, en la carpeta storage se puede ver varios instaladores, los cuales puedes instalarlos con 'pip install (the_file_name.whl) y tambien hay un link con un tutorial de como hacerlo'.
        
        para realizar la conexion utilice cnxn = MySQLdb.connect(return_conection_string('mysql',db_database='crud'))"""
        host=self.__db_host
        user=self.__db_user
        passwd=self.__db_password
        db=self.__db_database
        connect_timeout = "connect_timeout='10000'"

        return (host,user,passwd,db)

    
def ping():
    try:
        conexion  = pyodbc.connect(return_conection_string(argument='postgres', db_database='food'),autocommit=True,timeout=1000) #Le digo que cierre automaticamente la conexion
        print("Base de datos conectada...")
        return True
    except Exception as err:
        print('error al conectar a la base de datos >>> ' + str(err))
        return False



def return_conection_string(argument,db_database=None):
    """argument is required 'mssql' or 'mysql' and define the db_database if necessary \n
    · para conectarte a SQL SERVER importa 'return_conection_string' y utiliza por ejemplo 'cnxn = pyodbc.connect(return_conection_string('mssql',db_database='database_name'))' \n
    · para conectarte a MySQL importa 'return_conection_string' y utiliza por ejemplo 'cnxn = MySQLdb.connect(return_conection_string('mysql',db_database='database_name'))'
    """
    switcher = {
        'mssql': connection_string(db_database=db_database if db_database is not None else DB_DATABASE ).mssql,
        'postgres': connection_string(db_database=db_database if db_database is not None else DB_DATABASE ).postgres,
        'mysql': connection_string(db_database=db_database if db_database is not None else DB_DATABASE ).mysql,
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "Invalid 'DB_CONNECTION' in the file .conf or the argument")
    return func()
    # Execute the function


# return_conection_string('mysql',db_database='crud')
