import kivy
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
import FileChooserWidget,ComboEdit
import data_grid
import json
from kivy.uix.scrollview import ScrollView
from data_grid import DataGrid
from kivy.clock import mainthread
from backend.SupplierService import SupplierService
from backend.GoodsService import GoodsService
from kivy.properties import ListProperty
from uiutils import UIUtils
import functools

class Display(BoxLayout):
    #Window.fullscreen = 'auto'
    background_color = ListProperty([176,215,243])
    supplierList = []

class Popup_Success(FloatLayout):
    pass

def show_popup():
    show = Popup_Success() # Create a new instance of the P class 
    popupWindow = Popup(title="Data Saved Successfully!!", content=show)
    # Create the popup window
    popupWindow.open() # show the popup

class Screen_Index(Screen):
    pass

class Screen_Main(Screen):
    supplier = ObjectProperty(None)
    service = SupplierService()
    grid = ObjectProperty(None)
    data = []
    header = ['ID','Supplier Name', 'Address', 'Model', 'Material Code','Description','Stock Volume','Date','Action']
    body_alignment = ["center","center", "center", "center", "center","center", "center", "center", "center"]
    col_size = [0.1,0.3, 0.2, 0.3, 0.4,0.5, 0.2, 0.2, 0.2]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## get data from DB ##
        self.data = self.service.getAllSuppliers()
        self.grid = DataGrid(self.header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 50
        #reset the supplier cache list and add new items
        Display.supplierList = []
        for rowData in self.data:
            self.grid.add_row(rowData, self.body_alignment, self.col_size,self)
            Display.supplierList.append(str(rowData[1])+"("+str(rowData[0])+")")
            #print(str(rowData[1])+"("+str(rowData[0])+")")
            #print(Display.supplierList)

    @mainthread
    def on_enter(self):
        tableCanvas = self.ids.tableID
        #print(tableCanvas.width)
        #print(tableCanvas.height)
        tableCanvas.add_widget(self.grid)

    def search(self):
        #print("inside search method %s" % self.txtsearch.text)
        #print(self.grid)
        sText = self.txtsearch.text
        newData = []
        if UIUtils.isStringEmpty(sText):
            #print("text is empty")
            newData = self.data
        else:
            newData = self.service.searchSuppliers(sText)
            #print("text is **NOT *** empty %s" % newData)
        self.grid.select_all(self)
        self.grid.remove_row(len(self.header),self)
        for rowData in newData:
            #print(rowData)
            self.grid.add_row(rowData, self.body_alignment, self.col_size,self)

    def viewSupplier(self):
        rowIndex = int(DataGrid.gird_selected_rows)

        print(DataGrid.gird_selected_rows)
        self.ids.supLabel.text = "Edit Supplier (Supplier ID) : "+str(self.data[rowIndex][0])
        self.ids.txtSupID.text = str(self.data[rowIndex][0])
        self.txtsupplier.text = self.data[rowIndex][1]
        self.txtaddress.text = self.data[rowIndex][2]
        self.txtmodel.text = self.data[rowIndex][3]
        self.txtmatCode.text = self.data[rowIndex][4]
        self.txtmatDesc.text = self.data[rowIndex][5]
        self.txtstock.text = str(self.data[rowIndex][6])
        self.ids.newSupScreen.collapse = False;

    def saveSupplier(self):
        supData = []
        supData.append(self.txtsupplier.text)
        supData.append(self.txtaddress.text)
        supData.append(self.txtmodel.text)
        supData.append(self.txtmatCode.text)
        supData.append(self.txtmatDesc.text)
        if UIUtils.isStringEmpty(self.txtstock.text):
            supData.append(0)
        else:
            supData.append(int(self.txtstock.text))

        # txtSupID is a hidden field with supplierID
        # is that field is empty, it is new supplier insert
        if UIUtils.isStringEmpty(self.txtSupID.text):
            self.service.insertSupplier(supData)
        else:
            #attach the supplier id and push for update
            supData.append(self.txtSupID.text)
            self.service.updateSupplier(supData)
            #After updated , reset label and hidden text field to default value
            self.ids.supLabel.text = "Add New Supplier"
            self.ids.txtSupID.text = ''
            self.txtsupplier.text= ''
            self.txtaddress.text = ''
            self.txtmodel.text= ''
            self.txtmatCode.text= ''
            self.txtmatDesc.text= ''
            self.txtstock.text = ''
            show_popup()
            self.ids.supplierListScreen.collapse = False;



class Screen_Search(Screen):
    service = GoodsService()
    grid = ObjectProperty(None)
    data = []
    header = ['ID','Supplier ID','Supplier Name', 'Part No', 'Description', 'Gin No','Goods Date','Quantity','Status']
    body_alignment = ["center","center","center", "center", "center", "center","center", "center", "center"]
    col_size = [0.1,0.1,0.3, 0.2, 0.3, 0.2,0.2, 0.1, 0.1]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        ## get data from DB ##
        self.data = self.service.getAllGoods()
        self.grid = DataGrid(self.header, self.data, self.body_alignment, self.col_size)
        self.grid.rows = 50
        for rowData in self.data:
            self.grid.add_row(rowData, self.body_alignment, self.col_size,self)

    @mainthread
    def on_enter(self):
        print("##Bug01: onEnter")
        tableCanvas1 = self.ids.goodsTableID
        print("##Bug01: onEnter")
        tableCanvas1.add_widget(self.grid)
        self.txtsupplier.values = Display.supplierList

    def searchGR(self):
        #print("inside search method %s" % self.goodstxtsearch.text)
        #print(self.grid)
        sText = self.goodstxtsearch.text
        newData = []
        if UIUtils.isStringEmpty(sText):
            print("text is empty")
            newData = self.data
        else:
            newData = self.service.searchGoods(sText)
            #print("text is **NOT *** empty %s" % newData)
        self.grid.select_all(self)
        self.grid.remove_row(len(self.header),self)
        for rowData in newData:
            #print(rowData)
            self.grid.add_row(rowData, self.body_alignment, self.col_size,self)

    def viewGR(self):
        print("DataGrid.gird_selected_rows %s" % DataGrid.gird_selected_rows)
        rowIndex = int(DataGrid.gird_selected_rows)
        #sm.supplier_id,sm.supplier_name,gr.part_no,gr.description,gr.gin_no,gr.goodsdate,gr.quantity,gr.status
        #print(DataGrid.gird_selected_rows)
        #(1, 4, 'Poly plastics', '2', 'yydyydyd', '2', datetime.date(2019, 12, 31), 3, 'ACTIVE')
        self.txtGID.text = str(self.data[rowIndex][0])
        self.grLabel.text = "Edit Goods Received (Supplier ID) : "+str(self.data[rowIndex][1])
        #self.txtsupplier.text
        self.txtpartNo.text = str(self.data[rowIndex][3])
        self.txtpartDesc.text = str(self.data[rowIndex][4])
        self.txtGno.text = str(self.data[rowIndex][5])
        self.txtQt.text  = str(self.data[rowIndex][6])

        print(self.data[rowIndex])
        self.ids.newGoodsScreen.collapse = False;

    def saveGR(self):
        GRData = []
        supplierID = str(self.txtsupplier.text)
        supplierID = supplierID.split('(', 1)[1].split(')')[0]
        print(" -------- %s" % supplierID)
        GRData.append(self.txtpartNo.text)
        GRData.append(self.txtpartDesc.text)
        GRData.append(self.txtGno.text)
        GRData.append(self.txtQt.text)

        # txtGID is a hidden field with supplierID
        # is that field is empty, it is new supplier insert
        if UIUtils.isStringEmpty(self.txtGID.text):
            GRData.append(int(supplierID))
            self.service.insertGoods(GRData)
        else:
            #attach the supplier id and push for update
            #GRData.append(self.txtGID.text)
            GRData.append(int(self.txtGID.text))
            GRData.append(int(supplierID))
            self.service.updateGoods(GRData)
            #After updated , reset label and hidden text field to default value
            self.grLabel.text = "Edit Goods"
            self.ids.txtGID.text = ''
            self.txtsupplier.text= ''
            self.txtpartNo.text = ''
            self.txtpartDesc.text= ''
            self.txtGno.text= ''
            self.txtQt.text= ''
        show_popup()
        self.ids.goodsListScreen.collapse = False;

class Screen_Print(Screen):
    pass

class Add_Supplier(Screen):
    pass

class Upload_Supplier(Screen):
    pass

class MainApp(App):
    def build(self):
        return Display()

if __name__ == '__main__':
    MainApp().run()
