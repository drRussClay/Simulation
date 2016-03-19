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
        if self.pair[0]["Family"] == self.pair[1]["Family"]:
            newResult = self.famInteract(posVal, avoidVal)
        else:
            if self.pair[0]["Group"] == self.pair[1]["Group"]:
                newResult = self.ingroupInteract(posVal, avoidVal)
            else: newResult = self.outgroupInteract(posVal, avoidVal)
        
        return newResult
        
    def famInteract(self, posVal, avoidVal):
        randSeed = random.uniform(0,1)
        
        p1Interact = .95 + (self.pair[0]["Agent"].getOpenness() * .05)
        p2Interact = .95 + (self.pair[1]["Agent"].getOpenness() * .05)
        
        if (p1Interact < randSeed):
            newResult=self.avoidResult(avoidVal)
        else: 
            if(p2Interact < randSeed):
                newResult=self.avoidResult(avoidVal)
            else: newResult=self.interactResult(posVal)
            
        return newResult        
        
    def ingroupInteract(self, posVal, avoidVal):
        randSeed = random.uniform(0,1)
        
        p1Interact = .75 + (self.pair[0]["Agent"].getOpenness() * .25)
        p2Interact = .75 + (self.pair[1]["Agent"].getOpenness() * .25)
        
        if (p1Interact < randSeed):
            newResult=self.avoidResult(avoidVal)
        else: 
            if(p2Interact < randSeed):
                newResult=self.avoidResult(avoidVal)
            else: newResult=self.interactResult(posVal)
            
        return newResult 
        
        
    def outgroupInteract(self, posVal, avoidVal):
        randSeed = random.uniform(0,1)
        
        p1Interact = self.pair[0]["Agent"].getOpenness() 
        p2Interact = self.pair[1]["Agent"].getOpenness() 
        
        if (p1Interact < randSeed):
            newResult=self.avoidResult(avoidVal)
        else: 
            if(p2Interact < randSeed):
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
