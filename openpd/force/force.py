'''
Author: your name
Date: 2021-01-31 21:33:31
LastEditTime: 2021-01-31 21:34:48
LastEditors: your name
Description: In User Settings Edit
FilePath: /openpd/openpd/force/force.py
'''
class Force(object):
    def __init__(self, force_id, force_group) -> None:
        super().__init__()
        self.force_id = force_id
        self.force_group = force_group

    def getForceGroup(self):
        return self.force_group

    def setForceGroup(self, force_group):
        self.force_group = force_group