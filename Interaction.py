# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 13:08:29 2016

@author: Russ.Clay
"""

class Interaction:
    def __init__(self, agent1, agent2):
        self.agent1 = agent1
        self.agent2 = agent2
        self.agent1StartVal = None
        self.agent1EndVal = None
        self.agent2StartVal = None
        self.agent2EndVal = None
        
# --- Accessor Functions
    def getAgent1(self):
        return self.agent1
        
    def getAgent2(self):
        return self.agent2
                
    def getAgent1StartVal(self):
        return self.agent1StartVal
        
    def getAgent1EndVal(self):
        return self.agent1EndVal
        
    def getAgent2StartVal(self):
        return self.agent2StartVal
        
    def getAgent2EndVal(self):
        return self.agent2EndVal
        
# --- Additional Functions
                
    def deadCheck(self):
        check1 = self.agent1.getDeadValue()
        check2 = self.agent2.getDeadValue()
        
        if(check1 or check2):
            return True
        else: return False
   
       
    def setStartVals(self):                
        self.agent1StartVal = self.agent1.getValue()
        self.agent2StartVal = self.agent2.getValue()
        
    def setEndVals(self):        
        self.agent1EndVal = self.agent1.getValue()
        self.agent2EndVal = self.agent2.getValue()
        
