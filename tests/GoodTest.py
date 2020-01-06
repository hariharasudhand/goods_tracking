import unittest

from services.GoodsService import GoodsService

class GoodsTestCase(unittest.TestCase):
    service = GoodsService()

    def test_list_goods(self):
        self.assertNotEqual(len(self.service.getAllGoods()), 201)

    def test_search_goods(self):
        self.assertTrue(self.service.serachGoods('Pune'))

    def test_get_one_goods(self):
        self.assertTrue(self.service.getOneGoods(1))

    def test_get_one_goods_id_name(self):
        self.assertNotEqual(len(self.service.serachIdName('Pune')), 20)

    def test_insert_data(self):
        inData = (200,'abc123','Pune','gin34876',18,'ACTIVE')
        self.assertTrue(self.service.insertGoods(inData))

    def test_update_data(self):
        inData = (200, 'abc123','Pune','code2837',30,'ACTIVE','some reason','note-283',1)
        self.assertTrue(self.service.updateGoods(inData))


if __name__ == '__main__':
    unittest.main()
