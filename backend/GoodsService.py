from backend.dao.GoodsDAO import GoodsDAO

class GoodsService():
    def __init__(self):
        self.dao = GoodsDAO()

    def getAllGoods(self):
        return self.dao.getAllGoods()

    def getOneGoods(self, id):
        return self.dao.getGoods(id)

    def searchGoods(self, filter):
        return self.dao.searchGoods(filter)

    def serachIdName(self, filter):
        return self.dao.searchIdName(filter)

    def insertGoods(self, goodsData):
        return self.dao.insertGoods(goodsData)

    def updateGoods(self, goodsData):
        return '{0} record updated successfully'.format(self.dao.updateGoods(goodsData))
