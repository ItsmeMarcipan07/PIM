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

class ProgressBar(QProgressBar):

    def __init__(self, title):
        QProgressBar.__init__(self)
        layout = QVBoxLayout()
        self.setLayout(layout)
