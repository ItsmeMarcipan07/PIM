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

class FileBrowser(QWidget):
    OpenFile = 0
    OpenFiles = 1
    OpenDirectory = 2
    SaveFile = 3

    def __init__(self, title, mode=OpenFile):
        QWidget.__init__(self)
        layout = QHBoxLayout()
        self.setLayout(layout)
        self.enable = False
        self.browser_mode = mode
        self.filter_name = ' Excel files (*.xlsx; *.xls)'
        self.dirpath = QDir.currentPath()

        self.label = QLabel()
        self.label.setText(title)
        self.label.setFixedWidth(130)
        self.label.setFont(QFont("Arial"))
        self.label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.label)

        self.lineEdit = QLineEdit(self)
        self.lineEdit.setFixedWidth(180)
        layout.addWidget(self.lineEdit)

        self.button = QPushButton('Browse')
        self.button.clicked.connect(self.getFile)
        layout.addWidget(self.button)
        layout.addStretch()

        self.filepaths = []

    def setMode(mode):
        self.mode = mode

    # --------------------------------------------------------------------
    # For example,
    #    setFileFilter('Images (*.png *.xpm *.jpg)')
    def setFileFilter(text):
        self.filter_name = text
        # --------------------------------------------------------------------

    def setDefaultDir(path):
        self.dirpath = path

    # --------------------------------------------------------------------
    def getFile(self):
        if self.browser_mode == FileBrowser.OpenFile:
            self.filepaths.append(QFileDialog.getOpenFileName(self, caption='Choose File',
                                                              directory=self.dirpath,
                                                              filter=self.filter_name)[0])
        elif self.browser_mode == FileBrowser.OpenDirectory:
            self.filepaths.append(QFileDialog.getExistingDirectory(self, caption='Choose Directory',
                                                                   directory=self.dirpath))
        else:
            return

        if len(self.filepaths) == 0:
            return
        else:
            self.lineEdit.setText(self.filepaths[0])
            return True
            # --------------------------------------------------------------------

    def setLabelWidth(self, width):
        self.label.setFixedWidth(width)
        # --------------------------------------------------------------------

    def setlineEditWidth(self, width):
        self.lineEdit.setFixedWidth(width)

    # --------------------------------------------------------------------
    def getPaths(self):
        return self.filepaths

    def on_text_changed(self):
        self.button.setEnabled(bool(self.lineEdit.text()))