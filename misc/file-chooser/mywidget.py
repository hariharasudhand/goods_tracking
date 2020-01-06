#Imports Kivy

from kivy.config import Config

Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')
Config.set('graphics', 'left', 100)
Config.set('graphics', 'top',  100)
Config.write()

from kivy.app import App

from kivy.clock import Clock
from kivy.uix.scatter import Scatter
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.properties import ListProperty, ObjectProperty, BooleanProperty, StringProperty
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooser
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.checkbox import CheckBox
from kivy.uix.scrollview import ScrollView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.effects.dampedscroll import DampedScrollEffect
from kivy.uix.spinner import Spinner
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.popup import Popup
from kivy.uix.carousel import Carousel

from kivy.lang import Builder
from kivy.factory import Factory

from time import gmtime, strftime

class Screen2(Screen):
	pass

class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)

class MyWidget(TabbedPanelItem):
	isShown = BooleanProperty(False)
	isShown2 = BooleanProperty(False)
	pathsOK = BooleanProperty(False)
	paths1OK = BooleanProperty(False)
	paths2OK = BooleanProperty(False)

	weights = StringProperty()

	epochs = 0

	#wasFocused = {}

	#written_text_prop = ""

	check_ref = {}
	textinput_ref = {}
	param_values = {}
	#textinput_ref_inv = {}

	spinner_choices = ["GPU_count", "Images / GPU", "Number of classes", "Image_min_dim", "Image_max_dim", "RPN_anchors_scales", "Train_ROIS / image", "Steps per epoch", "Validation steps"]
	default_values = [1, 8, 2, 256, 256, 1337, 32, 100, 5]

	counter = 0
	for choice in spinner_choices:
		param_values[choice] = default_values[counter]
		counter += 1

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content,size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		self.dismiss_popup()

	def gogogo(self, *args):
		pb = self.ids["bar"]
		if args[0] != "clock call":
			pb.value = 0
		pb.value += 1
		if pb.value < 100:
			Clock.schedule_once(lambda dt: self.gogogo("clock call"), 0.1)
			print(pb.value)
		print("Done")

	def weightsOK(self, *args):
		poppy = args[0]
		text = args[1].text

		if text != "OK":
			args[1].background_color = [1,0,0,1]
		else:
			args[1].background_color = [0,1,0,1]
			poppy.dismiss()
			self.weights = text

	def epochsOK(self, *args):
		poppy = args[0]
		text = args[1].text
		try:
			int(text)
			args[1].background_color = [0,1,0,1]
			print("Leggo for {} epochs".format(text))
			poppy.dismiss()
			self.epochs = int(text)
		except ValueError as e:
			args[1].background_color = [1,0,0,1]

	def threedeespinnah(self, *args):
		choice = args[1]
		if choice == "Other":
			content = BoxLayout(orientation='vertical',size_hint_y=None, height=self.minimum_height, spacing=30, padding=[30,30])
			b = Button(text="OK", size_hint_y=None, height=30)
			t = TextInput(hint_text="Your path here", multiline=False, size_hint_y=None, height=30, unfocus_on_touch=True)

			content.add_widget(t)
			content.add_widget(b)

			b.bind(on_press=lambda *args:self.weightsOK(p, t))

			p = Popup(title='Enter the path of your weights', content=content, auto_dismiss=False, size_hint_y=None, height=210, size_hint_x=None, width=300)

			p.open()

	def threedeespinnah2(self, *args):
		choice = args[1]
		if choice == "Other":
			content = BoxLayout(orientation='vertical',size_hint_y=None, height=self.minimum_height, spacing=30, padding=[30,30])
			b = Button(text="OK", size_hint_y=None, height=30)
			t = TextInput(hint_text="Number of epochs here", multiline=False, size_hint_y=None, height=30, unfocus_on_touch=True)

			content.add_widget(t)
			content.add_widget(b)

			b.bind(on_press=lambda *args:self.epochsOK(p, t))

			p = Popup(title='Enter the number of epochs you want', content=content, auto_dismiss=False, size_hint_y=None, height=210, size_hint_x=None, width=300)

			p.open()

	def checkpaths(self, iden, *args):
		bouton = args[0]
		log = self.ids["log"]
		scroll = self.ids["scroll"]
		input2 = self.ids["input2"]
		labels_added = []
		if iden == "2":
			if input2.text == "OK":
				bouton.text = "All good"
				log.add_widget(Label(text=strftime("%H:%M:%S (+2)", gmtime()) + "  Validation data: path OK!", size_hint_y=None, height=30, id=str(22)))
				labels_added.append(Label(text=strftime("%H:%M:%S", gmtime()) + "  Validation data: path OK!", size_hint_y=None, height=30, id=str(22)))
				self.paths2OK = True
			else:
				bouton.text = "Nope"
				log.add_widget(Label(text=strftime("%H:%M:%S (+2)", gmtime()) + "  Validation data: path error", size_hint_y=None, height=30, id=str(22)))
				labels_added.append(Label(text=strftime("%H:%M:%S (+2)", gmtime()) + "  Validation data: path error", size_hint_y=None, height=30, id=str(22)))
				self.paths2OK = False

		scroll.scroll_to(labels_added[-1])

		if self.paths2OK or self.paths1OK:
			self.pathsOK = True
		else:
			self.pathsOK = False

	def checkValues(self, *args):
		log = self.ids["log"]
		for param, widg in self.textinput_ref.items():
			if widg.focus:
				#self.wasFocused[widg] = True
				item = widg
				written_text = item.text
				if written_text == '':
					item.background_color = [1,1,1,1]
					pass
				try:
					if written_text != '':
						item.background_color = [0, 1, 0, 1]
						int(written_text)
						self.param_values[param] = written_text
						log.add_widget(Label(text=strftime("%H:%M:%S (+2) : ", gmtime()) + "{} set to {}".format(param, written_text), size_hint_y=None, height=30, color=[0,0.5,1,1]))
						#written_text_prop = written_text
				except ValueError as e:
					item.background_color = [1,0,0,1]
					log.add_widget(Label(text=strftime("%H:%M:%S (+2) : ", gmtime()) + "{} must be an integer".format(param), size_hint_y=None, height=30, color=[1,0,0,1]))



	def buttonValidation(self, *args):
		s = ""
		pop = args[0]
		pop.dismiss()
		log = self.ids["log"]
		params = self.ids["parameters"]
		babies = params.children
		sizeBaby = len(babies)

		if babies:
			for l in range(sizeBaby):
				params.remove_widget(babies[sizeBaby-1-l])
				l+=1

		chosen = []
		for idxs, wgt in self.check_ref.items():
			if wgt.active:
				if not chosen:
					s += " " +idxs
				else:
					s += " - " + idxs
				chosen.append(idxs)

		log.add_widget(Label(text="Added:" +s, size_hint_y=None, height=30))

		for c in chosen:
			params.add_widget(Label(text=c, size_hint_y=None, height=30))
			params.add_widget(Label(text=str(self.param_values[c]), size_hint_y=None, height=30))
			inputerino = TextInput(size_hint_y=None, height=30, multiline=False, unfocus_on_touch=True)

			self.textinput_ref[c] = inputerino
			#self.textinput_ref_inv[inputerino] = c
			#self.wasFocused[inputerino] = False

			params.add_widget(inputerino)
			inputerino.bind(text=lambda *args:self.checkValues())
			#inputerino.bind(on_text_validate=lambda *args:self.enterpls())


	def popupSettings(self, *args):
		list_of_choices = []
		list_chosen = []

		number_content = len(self.spinner_choices)
		contentF = ScrollView(do_scroll_x=False, size_hint_y=None, height=400)
		content = GridLayout(rows=number_content+1, cols=2, size_hint_y=None, height=self.minimum_height, spacing=30)

		for y in self.spinner_choices:
			content.add_widget(Label(text=y + " (Current value: {})".format(self.param_values[str(y)]), size_hint_y=None, height=30, size_hint_x=None, width=300))

			checkmate = CheckBox(size_hint_y=None, height=30)

			self.check_ref[y] = checkmate

			content.add_widget(checkmate)


		b = Button(text="OK", size_hint_y=None, height=30)

		content.add_widget(Label(text="Click here when you are done -> ", size_hint_y=None, height=30))
		content.add_widget(b)
		contentF.add_widget(content)

		p = Popup(title='Choose the parameters you want to change', content=contentF, auto_dismiss=False, size_hint_y=None, height=500, size_hint_x=None, width=500)
		b.bind(on_press=lambda *args:self.buttonValidation(p))
		p.open()

	def launchMapnik(self, *args):
		content = BoxLayout(orientation="vertical", size_hint_y=None, height=self.minimum_height, spacing=20)
		grid = BoxLayout(size_hint_y=None, height=self.minimum_height, spacing=20)

		t = TextInput(hint_text="CSV file here", size_hint_y=None, height=40)
		clean = Button(text="Clean the images?", size_hint_y=None, height=40)
		validate = Button(text="Launch", size_hint_y=None, height=40)

		grid.add_widget(Label(text="CSV file > ", size_hint_y=None, height=40))
		grid.add_widget(t)

		content.add_widget(grid)
		content.add_widget(clean)
		content.add_widget(validate)

		p = Popup(title='Mapnik launch configuration', content=content, auto_dismiss=False, size_hint_y=None, height=500, size_hint_x=None, width=500)
		p.open()


class TheJamApp(App):
	def build(self):
		return Builder.load_file("TheJam.kv")
		#return MyWidget()

if __name__ == "__main__":
	Window.size=(768, 930)
	TheJamApp().run()