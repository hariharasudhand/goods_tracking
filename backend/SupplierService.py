from backend.dao.SupplierDAO import SupplierDAO

class SupplierService():
    def __init__(self):
        self.dao = SupplierDAO()

    def getAllSuppliers(self):
        return self.dao.getAllSuppliers()

    def getOneSupplier(self, supId):
        return self.dao.getSupplier(supId)

    def searchSuppliers(self, filter):
        return self.dao.searchSuppliers(filter)

    def serachIdName(self, filter):
        return self.dao.searchIdName(filter)

    def loadSuppliers(self,file_path):
        return self.dao.addAllSupplier(file_path)

    def insertSupplier(self, supplierData):
        return self.dao.insertSupplier(supplierData)

    def updateSupplier(self, supplierData):
        return '{0} record updated successfully'.format(self.dao.updateSupplier(supplierData))


#service = SupplierService()
#suppliers = service.loadSuppliers()
#suppliers = service.searchSuppliers('Pune')
#suppliers = service.getOneSupplier(200)
#suppliers = service.getAllSuppliers()
#suppliers = service.serachIdName('Pune')


#suppliers = service.insertSupplier(('test supplier','sample address','model123', 'code2837','material details',18,'ACTIVE'))
#suppliers = service.updateSupplier(('test supplier','sample address','model123', 'code2837','material details',30,'ACTIVE',200))

#print('Final Result: ', len(suppliers))