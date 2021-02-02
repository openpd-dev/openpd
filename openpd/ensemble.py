'''
Author: your name
Date: 2021-01-31 21:30:06
LastEditTime: 2021-01-31 21:43:47
LastEditors: your name
Description: In User Settings Edit
FilePath: /openpd/openpd/system.py
'''
from .force import *

class Ensemble(object):
    def __init__(self) -> None:
        super().__init__()

    def addForce(self, force:Force):
        pass