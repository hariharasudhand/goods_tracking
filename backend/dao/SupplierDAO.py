import csv

from backend.dao.Queries import getAllSuppliersQuery, updateSupplierQuery, searchSuppliersQuery
from backend.dao.Queries import selectOneSupplierQuery, insertSupplierQuery
from backend.dao.util import Util

class SupplierDAO():

    def __init__(self):
        self.util = Util()
        self.conn = self.util.getMysqlConnection()
        self.cur = self.conn.cursor()


    def getAllSuppliers(self):
        try:
            self.cur.execute(getAllSuppliersQuery())
            r = self.cur.fetchall()
            return self.util.processRecords(r)
        except Exception as ex:
            print("Error selecting all records: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def getSupplier(self, supId):
        try:
            self.cur.execute(selectOneSupplierQuery(), (supId,))
            r = self.cur.fetchall()
            return self.util.processRecords(r)
        except Exception as ex:
            print("Error selecting one record: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def searchSuppliers(self, filter):
        try:
            self.cur.execute(searchSuppliersQuery(filter))
            r = self.cur.fetchall()
            return self.util.processRecords(r)
        except Exception as ex:
            print("Error searching record: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def searchIdName(self, filter):
        r = []
        for row in self.searchSuppliers(filter):
            retVal = row[0], row[1]
            r.append(retVal)
        return r

    def insertSupplier(self, sup):
        try:
            self.cur.execute(insertSupplierQuery(), sup)
            return self.cur.rowcount
        except Exception as ex:
            print("Error in data insertion: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def updateSupplier(self, sup):
        try:
            self.cur.execute(updateSupplierQuery(), sup)
            return self.cur.rowcount
        except Exception as ex:
            print("Error in data update: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def addAllSupplier(self,file_path):
        print ("File ready to read %s" % file_path)
        rowcount = 0
        try:
            with open(file_path, 'r') as f:
                reader = csv.reader(f)
                for row in reader:
                    self.cur.execute(insertSupplierQuery(), row)
                    rowcount += rowcount
                self.conn.commit()
            return rowcount
        except Exception as ex:
            print("Data insert Error: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

