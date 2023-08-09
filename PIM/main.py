import os
import requests
import pandas as pd
import openpyxl
import re
import math
import urllib

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

import sys
from bs4 import BeautifulSoup
from demo import Demo


# ========================================================
if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    demo = Demo()  # <<-- Create an instance
    demo.show()
    sys.exit(app.exec())
