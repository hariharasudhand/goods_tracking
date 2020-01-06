class UIUtils():

    clipData = 0
    supplierList = []

    def __init__(self):
        pass

    @staticmethod
    def searchTable(data,x):
        matchRow = []
        for i in range(len(data)):
            for j in range(len(data[i])):
                #print("checking  at ", i, ", ", j)
                #print(data[i][j])
                if (str(data[i][j]).startswith(x)):
                    #print("n Found at ", i, ", ", j)
                    matchRow.append(i)
        #print("matchRow = %s " % matchRow)
        return matchRow

    def isStringEmpty(myString):
        return not (myString and myString.strip())

    @staticmethod
    def setSupplierList(supData):
        supplierList.append(supData[1]+"("+supData[0]+")")

    @staticmethod
    def getSupplierList():
        return supplierList

    @staticmethod
    def resetSupplierList():
        supplierList = []
        return supplierList