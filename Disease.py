# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:51:34 2016

@author: Russ.Clay
"""
import random

class Disease:
    def __init__(self):
        self.transRate = round(random.uniform(.3, .9), 3)
        self.sickValue = round(random.uniform(-22, -5), 3)
        self.sickTime = round(random.uniform(4, 13), 3)
        
    def getTransRate(self):
        return self.transRate
        
    def getSickValue(self):
        return self.sickValue
        
    def getSickTime(self):
        return self.sickTime