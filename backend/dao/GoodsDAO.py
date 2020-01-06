
from backend.dao.Queries import getAllGoodsQuery, updateGoodsQuery, searchGoodsQuery
from backend.dao.Queries import selectOneGoodsQuery, insertGoodsQuery
from backend.dao.util import Util

class GoodsDAO():

    def __init__(self):
        self.util = Util()
        self.conn = self.util.getMysqlConnection()
        self.cur = self.conn.cursor()


    def getAllGoods(self):
        try:
            self.cur.execute(getAllGoodsQuery())
            r = self.cur.fetchall()
            return self.util.processRecords(r)
        except Exception as ex:
            print("Error selecting all records: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def getGoods(self, id):
        try:
            self.cur.execute(selectOneGoodsQuery(), (id,))
            r = self.cur.fetchall()
            return self.util.processRecords(r)
        except Exception as ex:
            print("Error selecting one record: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def searchGoods(self, filter):
        try:
            self.cur.execute(searchGoodsQuery(filter))
            r = self.cur.fetchall()
            return self.util.processRecords(r)
        except Exception as ex:
            print("Error searching record: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def searchIdName(self, filter):
        r = []
        for row in self.searchGoods(filter):
            retVal = row[0], row[1]
            r.append(retVal)
        return r

    def insertGoods(self, sup):
        try:
            self.cur.execute(insertGoodsQuery(), sup)
            return self.cur.rowcount
        except Exception as ex:
            print("Error in data insertion: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

    def updateGoods(self, sup):
        try:
            self.cur.execute(updateGoodsQuery(), sup)
            return self.cur.rowcount
        except Exception as ex:
            print("Error in data update: {}".format(str(ex)))
        # finally:
        #     self.cur.close()
        #     self.conn.close()

