import kivy

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from backend.SupplierService import SupplierService

import os

class FileChooserWidget(BoxLayout):

    service = SupplierService()

    def open(self, path, filename):
        with open(os.path.join(path, filename[0])) as f:
            print ("File ready to read %s" % filename[0])
            self.service.loadSuppliers(filename[0])

    def selected(self, filename):
            print ("selected: %s" % filename[0])


class FileChooserApp(App):
    def build(self):
        return FileChooserWidget()

if __name__ == '__main__':
    FileChooserApp().run()