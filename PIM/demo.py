import os
import requests
import pandas as pd
import openpyxl
import re
import math

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import sys
from bs4 import BeautifulSoup
from CountrySelector import CountrySelector
from FileBrowser import FileBrowser
from progressBar import ProgressBar
import urllib
country_websites = pd.read_excel('website_data.xlsx')
country_websites_dict = country_websites.set_index('Country').to_dict()['Url']

class Demo(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        # Ensure our window stays in front and give it a title
        self.button = None
        self.setWindowFlags(Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("PIM Image Download")
        self.setFixedSize(440, 300)

        # Create and assign the main (vertical) layout.
        vlayout = QVBoxLayout()
        hlayout = QHBoxLayout()
        self.setLayout(vlayout)
        self.countryListPanel(vlayout)
        self.fileBrowserPanel(vlayout)
        self.radio = QRadioButton("PNG 4000 dpi", self)
        self.radio.toggled.connect(self.pngOrJpg)
        hlayout.addWidget(self.radio)
        # vlayout.addWidget(self.radio)
        self.file_format = 'jpg'
        self.link_ending = '_1500_jpg'
        self.radio = QRadioButton("JPG 1500 dpi", self)
        self.radio.setChecked(True)
        self.radio.toggled.connect(self.pngOrJpg)
        # vlayout.addWidget(self.radio)
        hlayout.addWidget(self.radio)
        vlayout.addStretch()
        self.addButtonPanel(hlayout)
        self.addExitButtonPanel(hlayout)
        vlayout.addLayout(hlayout)
        self.progressBar(vlayout)


        self.show()

    # --------------------------------------------------------------------

    def progressBar(self, parent_layout):

        vlayout = QVBoxLayout()
        self.progressBarWidget = ProgressBar('Select country')
        vlayout.addWidget(self.progressBarWidget)
        self.progressBarWidget.setGeometry(50, 100, 250, 30)
        self.progressBarWidget.setValue(0)
        vlayout.addStretch()
        parent_layout.addLayout(vlayout)

    def countryListPanel(self, parent_layout):

        vlayout = QHBoxLayout()
        self.countryListWidget = CountrySelector('Select country', country_websites_dict)
        vlayout.addWidget(self.countryListWidget)
        vlayout.addStretch()
        parent_layout.addLayout(vlayout)

    def fileBrowserPanel(self, parent_layout):
        vlayout = QVBoxLayout()

        self.fileFB = FileBrowser('Select Reference List', FileBrowser.OpenFile)
        self.dirFB = FileBrowser('Save in folder', FileBrowser.OpenDirectory)

        vlayout.addWidget(self.fileFB)
        vlayout.addWidget(self.dirFB)

        vlayout.addStretch()
        parent_layout.addLayout(vlayout)

    # --------------------------------------------------------------------
    def addButtonPanel(self, parentLayout):
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        self.button = QPushButton("OK")
        self.button.clicked.connect(self.buttonAction)
        hlayout.addWidget(self.button)
        parentLayout.addLayout(hlayout)

    def addExitButtonPanel(self, parentLayout):
        hlayout = QHBoxLayout()
        hlayout.addStretch()
        self.button = QPushButton("Exit")
        self.button.clicked.connect(self.buttonExit)
        hlayout.addWidget(self.button)
        parentLayout.addLayout(hlayout)

    def pngOrJpg(self):

        if self.sender().text() == 'PNG 4000 dpi':
            self.link_ending = '_4000_png'
            self.file_format = 'png'
        else:
            self.link_ending = '_1500_jpg'
            self.file_format = 'jpg'



    # --------------------------------------------------------------------
    def buttonAction(self):
        a = urllib.request.getproxies()
        proxies = {'http': 'http://gateway.schneider.zscaler.net:80',
                   'https': 'http://gateway.schneider.zscaler.net:80'}

        value = 0
        self.refs_path = self.fileFB.getPaths()
        try:
            self.refs_path = os.path.abspath(self.refs_path[0])

        except IndexError:
            dialog = QMessageBox(parent=self, text="Please select reference file!")
            dialog.setWindowTitle("System message")
            ret = dialog.exec()
            return

        self.destination_path = self.dirFB.getPaths()
        try:
            self.destination_path = os.path.abspath(self.destination_path[0])
        except IndexError:
            dialog = QMessageBox(parent=self, text="Please select destination folder!")
            dialog.setWindowTitle("System message")
            ret = dialog.exec()
            return
        try:
            ref_data = pd.read_excel(self.refs_path, header=None)
        except ValueError:
            print('Select Excel file with references in first column')
            return
        not_found_counter = 0
        for ref in ref_data.values:
            value += math.ceil(100 / len(ref_data))
            link = f'https://eref.se.com{self.countryListWidget.downloadURL}/product/{ref[0]}'
            try:
                try:
                    soup_data = BeautifulSoup(requests.get(link).content, 'html.parser')
                except:
                    soup_data = BeautifulSoup(requests.get(link, proxies=proxies).content, 'html.parser')
                    pass
                doc_url_soup = soup_data.find('img', {'class': 'thumbnail'})
                doc_url = doc_url_soup['src']
                doc_id = re.search(r'(Doc_Ref=)(.+)(&p)', doc_url)[2]
                img_download_url = f'https://download.schneider-electric.com/files?p_Doc_Ref={doc_id}&p_File_Type=rendition{self.link_ending}&default_image=DefaultProductImage.png'
                try:
                    img_file = requests.get(img_download_url).content
                except:
                    img_file = requests.get(img_download_url, proxies=proxies).content
                    pass
                with open(f"{self.destination_path}\\{ref[0]}.{self.file_format}", 'wb') as handler:
                    handler.write(img_file)

                self.progressBarWidget.setValue(int(value))
            except TypeError:
                not_found_counter += 1
                continue
            except ValueError:
                not_found_counter += 1
                continue
        if not_found_counter != 0:
            dialog = QMessageBox(parent=self, text=f'{not_found_counter} references not found')
            dialog.setWindowTitle("System message")
            ret = dialog.exec()
        else:
            dialog = QMessageBox(parent=self, text='All product images were successfully downloaded')
            dialog.setWindowTitle("System message")
            ret = dialog.exec()

    def buttonExit(self):
        sys.exit(0)