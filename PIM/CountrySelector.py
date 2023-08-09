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

country_websites = pd.read_excel('website_data.xlsx')
country_websites_dict = country_websites.set_index('Country').to_dict()['Url']

class CountrySelector(QWidget):

    def __init__(self, title, country_website_base):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.downloadURL = '/ww/en/'

        self.label = QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(130)
        self.label.setFont(QFont("Arial"))
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.label)

        self.countryList = QComboBox()
        self.countryList.addItems(country_websites_dict.keys())

        self.countryList.currentIndexChanged.connect(self.setCountry)
        layout.addWidget(self.countryList)
        layout.addStretch()

    def setCountry(self, i):
        self.downloadURL = list(country_websites_dict.values())[i]

    def setLabelWidth(self, width):
        self.label.setFixedWidth(width)
        # --------------------------------------------------------------------

    def setlineEditWidth(self, width):
        self.lineEdit.setFixedWidth(width)

    def setlineEditWidth(self, width):
        self.lineEdit.setFixedWidth(width)
