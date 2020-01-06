import unittest

from services.SupplierService import SupplierService

class TestSupplier(unittest.TestCase):
    service = SupplierService()

    def test_list_supplier(self):
        self.assertNotEqual(len(self.service.getAllSuppliers()), 201)

    def test_search_supplier(self):
        self.assertEqual(len(self.service.serachSupplier('Pune')), 27)

    def test_get_one_supplier(self):
        self.assertEqual(len(self.service.getOneSupplier(200)), 1)

    def test_get_one_supplier_id_name(self):
        self.assertNotEqual(len(self.service.serachIdName('Pune')), 20)

    def test_insert_data(self):
        inData = ('test supplier','sample address','model123', 'code2837','material details',18,'ACTIVE')
        self.assertTrue(self.service.insertSupplier(inData))

    def test_update_data(self):
        inData = ('test supplier','sample address','model123', 'code2837','material details',30,'ACTIVE',200)
        self.assertTrue(self.service.updateSupplier(inData))

if __name__ == '__main__':
    unittest.main()


