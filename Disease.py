# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 22:51:34 2016

@author: Russ.Clay
"""
import random

class Disease:
    def __init__(self):
        self.transRate = round(random.uniform(.1, .2), 3) # transmission rate of the disease
        self.sickValue = round(random.uniform(-20, -17), 3) # number of health points decrimented at each time period from an agent who is infected
        self.sickTime = round(random.uniform(3, 5), 3) # length of time that the disease lasts in an infected individual
        self.contagPeriod = random.randint(1, 3) # contagious period for the disease - currently unused
        self.visibility = round(random.uniform(0,1), 3)
        
    def getTransRate(self):
        return self.transRate
        
    def getSickValue(self):
        return self.sickValue
        
    def getSickTime(self):
        return self.sickTime
        
    def getContagPeriod(self):
        return self.contagPeriod
        
    def getVisibility(self):
        return self.visibility