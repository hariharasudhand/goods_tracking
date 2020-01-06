import mysql.connector

from mysql.connector import errorcode

class Util():

    def __init__(self):
        pass

   # def getPostgresConnection(self):
   #     try:
   #         self.conn = psycopg2.connect(dbname='postgres', host='localhost',
   #                                      port='5432', user='postgres', password='postgres')
   #         self.conn.autocommit = True
   #         return self.conn
   #     except Exception as ex:
   #         print("DB Connection error: {}".format(str(ex)))

    def getMysqlConnection(self):
        try:
            self.conn = mysql.connector.connect(user='tataadmin', password='pass#word#123',
                                                                           host='localhost',
                                                                           database='tatadb',port='8889')
            self.conn.autocommit = True
            return self.conn
        except Exception as ex:
            print("DB Connection error: {}".format(str(ex)))       

    def processRecords(self, rowSets):
        results = []
        for row in rowSets:
            results.append(row)
        return results