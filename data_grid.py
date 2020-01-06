import kivy
import urllib3
import json
import pprint
import functools
from uiutils import UIUtils

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import  ListProperty
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

from functools import partial
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput

Builder.load_string('''
# define how clabel looks and behaves
<CLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos

<HeaderLabel>:
  canvas.before:
    Color:
      rgb: self.bgcolor
    Rectangle:
      size: self.size
      pos: self.pos
'''
)

class CLabel(ToggleButton):
	bgcolor = ListProperty([1,1,1])

class HeaderLabel(Label):
	bgcolor = ListProperty([0.108,0.476,0.611])

counter = 0

class DataGrid(GridLayout):
	gird_selected_row = 0

	def add_row(self, row_data, row_align, cols_size, instance,**kwargs):
		global counter

		self.rows += 1
		#self.rows = 2
		##########################################################
		def change_on_press(self):
			childs = self.parent.children
			#print(childs)
			print("inside DataGrid self id : %s" % self.id)
			rowID = str(self.id)
			rowID = str(rowID).split("row_")[1].split("_col")[0]
			#there may be a better way to do this
			DataGrid.gird_selected_rows = rowID
			print("inside DataGrid selected Row: %s" % DataGrid.gird_selected_rows)
			#row_0_col_0
			for ch in childs:
				chid = str(ch.id)
				if chid.startswith("row_"+str(rowID)+"_col_"):
						if ch.state == "normal":
							ch.state="down"
						else:
							ch.state="normal"



		def change_on_release(self):
			if self.state == "normal":
				self.state = "down"
			else:
				self.state = "normal"
		##########################################################
		n = 0
		for item in row_data:
            
			cellvalue = "[color=000000]"+ str(item) +" [/color]"

			cell = CLabel(text=cellvalue,
										background_normal="static/background_normal.png",
										background_down="static/background_pressed.png",
										halign=row_align[n],
										markup=True,
										on_press=partial(change_on_press),
										on_release=partial(change_on_release),
										text_size=(0, None),
										size_hint_x=cols_size[n], 
										size_hint_y=None,
										height=60,
										id=("row_" + str(self.counter) + "_col_" + str(n)))
			cell_width = Window.size[0] * cell.size_hint_x
			cell.text_size=(cell_width - 30, None)
			cell.texture_update()
			self.add_widget(cell)
			n+=1
			#print(item)
		self.counter += 1


	def filt_row(self,data,sText,instance, **kwargs):
		#print("Searching for %s " % sText)
		childs = self.parent.children

		for ch in childs:
			for ch1 in ch.children:
				if ch1.id != "Header_Label":
					chid = str(ch1.id)
					matchRows = UIUtils.searchTable(data,sText)
					#print(matchRows)
					for rowID in matchRows:
						#row_0_col_0
						if not chid.startswith("row_"+str(rowID)+"_col_"):
							#print("removing %s" % chid)
							#print("row_"+str(rowID)+"_col_")
							self.remove_widget(ch1)

	def remove_row(self,n_cols,instance, **kwargs):
		print("n_cols ----------------- "+str(n_cols))
		childs = self.parent.children
		selected = 0
		for ch in childs:
			for c in reversed(ch.children):
				if c.id != "Header_Label":
					if c.state == "down":
						self.remove_widget(c)
						#print (str(c.id) + '   -   ' + str(c.state))
						selected += 1
		if selected == 0:
			for ch in childs:
				count_01 = n_cols
				count_02 = 0
				count = 0
				while (count < n_cols):
					if n_cols != len(ch.children):
						for c in ch.children:
							if c.id != "Header_Label":
								#print ("Length: " + str(len(ch.children)))
								#print ("N_cols: " + str(n_cols + 1))
								self.remove_widget(c)
								count += 1
								break
							else:
								break
					else:
						break

	def select_all(self,instance,**kwargs):
		#print("******* inside select all ****")
		childs = self.parent.children
		for ch in childs:
			for c in ch.children:
				if c.id != "Header_Label":
					c.state = "down"

	def unselect_all(self, instance, **kwargs):
		childs = self.parent.children
		for ch in childs:
			for c in ch.children:
				if c.id != "Header_Label":
					c.state = "normal"

	def show_log(self, instance, **kwargs):
		childs = self.parent.children
		for ch in childs:
			for c in ch.children:
				if c.id != "Header_Label":
					print (str(c.id) + '   -   ' + str(c.state) +  '   -   ' + str(c.text))
		
	def __init__(self, header_data, body_data, b_align, cols_size, **kwargs):
		super(DataGrid, self).__init__(**kwargs)
		#reset table row counter
		self.counter = 0
		self.size_hint_y=None
		self.bind(minimum_height=self.setter('height'))
		self.cols = len(header_data)
		self.rows = len(body_data) + 1
		#self.rows = 2
		self.spacing = [1,1]
		n = 0
		for hcell in header_data:
			header_str = "[b]" + str(hcell) + "[/b]"
			self.add_widget(HeaderLabel(text=header_str, 
																	markup=True, 
																	size_hint_y=None,
																	height=60,
																	id="Header_Label",
																	size_hint_x=cols_size[n]))
			n+=1


#add_row_btn = Button(text="Add Row", on_press=pp)
#del_row_btn = Button(text="Delete Row", on_press=partial(grid.remove_row, len(header)))
#upt_row_btn = Button(text="Update Row")
#slct_all_btn = Button(text="Select All", on_press=partial(grid.select_all))
#unslct_all_btn = Button(text="Unselect All", on_press=partial(grid.unselect_all))

#show_grid_log = Button(text="Show log", on_press=partial(grid.show_log))

###
def modal_insert(self):
	lbl1 = Label(text='ID', id="lbl")
	lbl2 = Label(text='Nome', id="lbl")
	lbl3 = Label(text='Preco', id="lbl")
	lbl4 = Label(text='IVA', id="lbl")
	txt1 = TextInput(text='000', id="txtinp")
	txt2 = TextInput(text='Product Name', id="txtinp")
	txt3 = TextInput(text='123.45', id="txtinp")
	txt4 = TextInput(text='23', id="txtinp")

	insertion_grid = GridLayout(cols=2)
	insertion_grid.add_widget(lbl1)
	insertion_grid.add_widget(txt1)
	insertion_grid.add_widget(lbl2)
	insertion_grid.add_widget(txt2)
	insertion_grid.add_widget(lbl3)
	insertion_grid.add_widget(txt3)
	insertion_grid.add_widget(lbl4)
	insertion_grid.add_widget(txt4)
	# create content and assign to the view
	
	content = Button(text='Close me!')

	modal_layout = BoxLayout(orientation="vertical")
	modal_layout.add_widget(insertion_grid)

	def insert_def(self):
		input_list = []
		for text_inputs in reversed(self.parent.children[2].children):
			if text_inputs.id == "txtinp":
				input_list.append(text_inputs.text)
		#print( input_list)
		grid.add_row(input_list, body_alignment, col_size, self)
		# print view
		# view.dismiss		


	insert_btn = Button(text="Insert", on_press=insert_def)	
	modal_layout.add_widget(insert_btn)
	modal_layout.add_widget(content)

	view = ModalView(auto_dismiss=False)

	view.add_widget(modal_layout)
	# bind the on_press event of the button to the dismiss function
	content.bind(on_press=view.dismiss)
	insert_btn.bind(on_release=view.dismiss)
	
	view.open()

add_custom_row = Button(text="Add Custom Row", on_press=modal_insert)

###
def json_fill(self):
	for d in data:
		print (d)
		grid.add_row(d, body_alignment, col_size, self)

#json_fill_btn = Button(text="JSON fill", on_press=partial(json_fill))

#btn_grid = BoxLayout(orientation="vertical")
#btn_grid.add_widget(json_fill_btn)
#btn_grid.add_widget(add_row_btn)
#btn_grid.add_widget(del_row_btn)
#btn_grid.add_widget(upt_row_btn)
#btn_grid.add_widget(slct_all_btn)
#btn_grid.add_widget(unslct_all_btn)
#btn_grid.add_widget(show_grid_log)
#btn_grid.add_widget(add_custom_row)


#root.add_widget(btn_grid)




class MainApp(App):
	def build(self):
		# grid = DataGrid(header, data, body_alignment, col_size)
		# interface = Interface()
		# print Window.size
		# return grid
		return root

if __name__=='__main__':
	MainApp().run()
