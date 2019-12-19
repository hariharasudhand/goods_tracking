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
import FileChooserWidget
import data_grid
import json
from kivy.uix.scrollview import ScrollView
from data_grid import DataGrid
from kivy.clock import mainthread

import sqlite3

class Display(BoxLayout):
    #Window.fullscreen = 'auto'
    pass
class Popup_Success(FloatLayout):
    pass

def show_popup():
    show = Popup_Success() # Create a new instance of the P class 

    popupWindow = Popup(title="Data Saved Successfully!!", content=show, size_hint=(None,None),size=(250,150)) 
    # Create the popup window

    popupWindow.open() # show the popup

class Screen_Index(Screen):
    pass

class Screen_Main(Screen):
    supplier = ObjectProperty(None)
    partno = ObjectProperty(None)
    description = ObjectProperty(None)
    ginno = ObjectProperty(None)
    date = ObjectProperty(None)
    quantity = ObjectProperty(None)
    
    @mainthread
    def on_enter(self):
        #Grid
        data_json = open('data/data.json')
        data = json.load(data_json)
        header = ['Supplier Name', 'Address', 'Model', 'Material Code','Description','Stock Volume','Date','Action']
        col_size = [0.1, 0.5, 0.2, 0.2]
        #body_alignment = ["center", "left", "right", "right"]
        body_alignment = ["center", "center", "center", "center","center", "center", "center", "center"]
        #print(data)
        grid = DataGrid(header, data, body_alignment, col_size)
        grid.rows = 10

        scroll = ScrollView(size_hint=(1, 1), size=(400, 500000), scroll_y=0, pos_hint={'center_x':.5,        'center_y':.5})
        scroll.add_widget(grid)
        scroll.do_scroll_y = True
        scroll.do_scroll_x = False
        for rowData in data:
            grid.add_row(rowData, body_alignment, col_size,self)
        tableCanvas = self.ids.tableID
        tableCanvas.add_widget(scroll)

    def btn(self):
        con = sqlite3.connect("MaterialDB.db")
        cur = con.cursor()
        
        try:
            sqliteConnection = sqlite3.connect('MaterialDB.db')
            cursor = sqliteConnection.cursor()
            supplier = self.supplier.text
            partno = self.partno.text
            description = self.description.text
            ginno = self.ginno.text
            date = self.date.text
            quantity = self.quantity.text
    

            sqlite_insert_query = """INSERT INTO `materialtest`
                          ('SupplierName', 'PatNo', 'Description', 'GINNo', 'Date','Quantity') 
                           VALUES 
                          (?,?,?,?,?,?)"""
            
            data_tuple = (supplier, partno, description, ginno, date, quantity)
            count = cursor.execute(sqlite_insert_query, data_tuple)
            sqliteConnection.commit()
    
            cursor.close()
            show_popup()


        except sqlite3.Error as error:
               print("Failed to insert data into sqlite table", error)
        finally:
           if (sqliteConnection):
               sqliteConnection.close()
                       
        self.supplier.text = ""
        self.description.text = ""
        self.partno.text = ""
        self.ginno.text = ""
        self.date.text = ""
        self.quantity.text = ""
    
class Screen_Search(Screen):
    pass

class Screen_Print(Screen):
    pass

class Add_Supplier(Screen):
    pass

class Upload_Supplier(Screen):
    pass

class MenuApp(App):
    def build(self):
        return Display()

if __name__ == '__main__':
    MenuApp().run()
