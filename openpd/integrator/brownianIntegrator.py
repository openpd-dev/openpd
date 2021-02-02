'''
Author: Zhenyu Wei
Date: 2021-01-31 20:04:00
LastEditTime: 2021-01-31 21:25:43
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: /openpd/openpd/integrator/bd.py
'''
class BrownianIntegrator:
    def __init__(self, dumpping_factor, temperature, interval) -> None:
        self.dumpping_factor = dumpping_factor
        self.temperature = temperature
        self.interval = interval

    def step(self, num_steps):
        pass