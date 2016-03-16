# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 15:26:17 2016

@author: Russ.Clay
"""
"Rules Engine"

import random

class Rules:
    def __init__(self, pair):
        self.pair = pair        
# --- Accessor Functions
        
    def getPair(self):
        return self.pair
        
# --- Additional Methods        
         
    def gameResult(self, posVal, avoidVal):
        agent1 = self.pair[0]
        agent2 = self.pair[1]
        
        p1Play = .5
        p2Play = .5
        randSeed = random.random()
        
        if (p1Play < randSeed):
            newResult=self.avoidResult(avoidVal)
        else: 
            if(p2Play < randSeed):
                newResult=self.avoidResult(avoidVal)
            else: newResult=self.interactResult(posVal)
                
        return newResult
    
    def avoidResult(self, avoidVal):
        avoid1=random.gauss(avoidVal, .1)
        avoid2=random.gauss(avoidVal, .1)
        return ["Avoid", avoid1, avoid2]
               
    def interactResult(self, posVal):
        interact1=random.gauss(posVal, .1)
        interact2=random.gauss(posVal, .1)
        return ["Interact", interact1, interact2]
