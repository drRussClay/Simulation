# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:20:30 2016

@author: Russ.Clay
"""

import random

class Agent:
    def __init__(self):
        self.ID = None
        self.openness = round(random.uniform(0, 1), 3)
        self.value = 75
        self.deadVal = False
        self.numTransmitted = 0
        self.numConnections = 3 #round(random.gauss(100.00, 21.45)) # should ensure that 99% of the population has a number of connections below 150 (the Dunbar number)
        self.connections = None
        self.disease = False
        self.diseaseType = None
        self.diseaseTime = None
        self.immunity = False
          
# --- Accessor Functions
    def getID(self):
        return self.ID
        
    def getOpenness(self):
        return self.openness
        
    def getDiffValue(self):
        return self.diffVal
        
    def getValue(self):
        return self.value
               
    def getDeadValue(self):
        return self.deadVal
        
    def getNumTransmitted(self):
        return self.numTransmitted
        
    def getNumConnects(self):
        return self.numConnections
        
    def getConnections(self):
        return self.connections
        
    def getDisease(self):
        return self.disease
        
    def getDiseaseTime(self):
        return self.diseaseTime
        
    def getDiseaseType(self):
        return self.diseaseType
        
    def getImmunity(self):
        return self.immunity
        
# --- Additional Functions
    def setID(self, num):
        self.ID = num
        
    def setConnections(self, network):
        for newConnect in range (0, len(network.matrix[self.ID])):
            if network.matrix[self.ID][newConnect] == 1:
                self.connections.append(newConnect)
            else: pass
                
    def setDisease(self, disease):
        self.disease = True
        self.diseaseType = disease
        self.diseaseTime = 0   
        
    def noImmunity(self, agent):
        if not(self.disease):
            return self.checkIntPartner(agent)
        else: return False
    
    def checkDiseaseTime(self):
        if self.diseaseTime > self.diseaseType.getSickTime():
            self.immunity = True
            self.disease = False
            self.diseaseTime = None
        else: self.updateValue(self.diseaseType.getSickValue())
    
    def checkIntPartner(self, agent):
        if agent.getDisease():
            diseaseType = agent.getDiseaseType()
            randVal = random.random()
            if randVal < diseaseType.getTransRate():
                newDiseaseBundle = [self.ID, diseaseType]
                agent.numTransmitted += 1
                return newDiseaseBundle
            else: return False
        else: return False
            
    def updateDisease(self, agent):
        if self.immunity:
            self.disease = False
            self.diseaseTime = None
            return False
        else: return self.noImmunity(agent)
        
    def updateValue(self, newVal):
        if newVal < 0:
            self.value = self.value + newVal
        else:
            diff = 100.00 - self.value
            self.value = self.value + (newVal*(diff/100))
