'''
Author: your name
Date: 2021-01-31 21:46:06
LastEditTime: 2021-01-31 21:46:54
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /openpd/openpd/force/torsionforce.py
'''
from . import Force

class PDFFTorsionForce(Force):
    def __init__(self) -> None:
        super().__init__()