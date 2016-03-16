# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:15:33 2016

@author: Russ.Clay
"""
from Agent import Agent
import igraph
import random


class Population:
    "The Population class defines and updates a population of agents"
    
    def __init__(self, popLimit, dRisk, iProb, disease, xConnects, minFam, maxFam, igConnectLow, igConnectHigh):
        self.agents = igraph.Graph(directed = False)
        self.minFam = minFam
        self.maxFam = maxFam
        self.igConnectLow = igConnectLow
        self.igConnectHigh = igConnectHigh
        self.dRisk = dRisk
        self.iProb = iProb
        self.disease = disease
        self.popLimit = popLimit
        self.popSize = 0
        self.numFamilies = 0
        self.initialSick = None
        self.initialImmune = None
        self.finalSick = None
        self.finalImmune = None
        self.numDied = None
        self.initialGraph = None
        self.xConnects = xConnects
        self.families = []
        
# --- Accessor Functions
               
    def getAgents(self):
        return self.agents
        
    def getAgent(self, ID):
        selectedAgent = self.agents.vs.find(Index = str(ID))
        return selectedAgent["Agent"]
                
    def getVS(self):
        return self.agents.vs
        
    def getES(self):
        return self.agents.es
    
    def getMinFam(self):
        return self.minFam
        
    def getMaxFam(self):
        return self.maxFam
        
    def getIGConnectLow(self):
        return self.igConnectLow
        
    def getIGConnectHigh(self):
        return self.igConnectHigh
        
    def get_dRisk(self):
        return self.dRisk
    
    def get_iProb(self):
        return self.iProb
        
    def getDisease(self):
        return self.disease
                      
    def getSize(self):
        return self.popSize
        
    def getPopLimit(self):
        return self.popLimit
        
    def getNumFamilies(self):
        return self.numFamilies
       
    def getInitialSick(self):
        return self.initialSick
        
    def getInitialImmune(self):
        return self.initialImmune
        
    def getFinalSick(self):
        return self.finalSick
        
    def getFinalImmune(self):
        return self.finalImmune
                    
    def getNumDied(self):
        return self.numDied
        
    def getMaxConnects(self):
        return self.maxConnects
        
    def getInitialGraph(self):
        return self.initialGraph
              
                        
# --- Additional Functions
    def setPop(self):
        
        self.addFamilies()
        self.addIngroupConnects()
        self.addOutgroupConnects()
            
    
    def addFamilies(self):
        
        while self.popSize < self.popLimit:
            if len(self.agents.vs) == 0:
                startVert = 0
            else: startVert = len(self.agents.vs)
            
            popLeft = self.popLimit - self.popSize
            newVerts = random.randint(self.minFam, self.maxFam)
            if newVerts < popLeft:
                addVerts = newVerts
            else: addVerts = popLeft
              
            self.agents.add_vertices(addVerts)
            endVert = len(self.agents.vs)
            newFam = []
            groupNum = random.randint(1,2)
            
            for i in range(startVert, endVert):
                newAgent = Agent()
                newAgent.setDisease(self.dRisk, self.disease, self.iProb)
                newAgent.setID(i)
                self.agents.vs(i)["Agent"] = newAgent
                self.agents.vs(i)["Index"] = str(i)
                self.agents.vs(i)["Status"] = "H"
                self.agents.vs(i)["Family"] = str(self.numFamilies)
                if groupNum == 1:
                    self.agents.vs(i)["Group"] = "A"
                else: self.agents.vs(i)["Group"] = "B"
                newFam.append(i)
                print "Added agent " + str(i)
                
            
            for i in range(startVert, endVert-1):
                for j in range(i+1, endVert):
                    self.agents.add_edge(i, j)
                    self.agents.es(len(self.agents.es)-1)["Relation"] = "Family"
                    
            self.families.append(newFam)             
            self.numFamilies+=1
            self.popSize += addVerts
            
    def addIngroupConnects(self):
        groupA = self.agents.vs.select(Group_eq = "A")
        groupB = self.agents.vs.select(Group_eq = "B")
        
        for i in groupA:
            numConnects = random.randint(self.igConnectLow, self.igConnectHigh)
            j = 0
        
            while j < numConnects:
                sameFamily = True
                exists = True
                while sameFamily or exists:
                    newConnect = random.randint(0, len(groupA)-1)
                    if i["Family"] == groupA[newConnect]["Family"]:
                        sameFamily = True
                    else: sameFamily = False
                    
                    if self.agents.are_connected(i.index, groupA[newConnect].index):
                        exists = True
                    else: exists = False            
                    
                self.agents.add_edge(i, groupA[newConnect])
                j += 1
                
        for i in groupB:
            numConnects = random.randint(self.igConnectLow, self.igConnectHigh)
            j = 0
        
            while j < numConnects:
                sameFamily = True
                exists = True
                while sameFamily or exists:
                    newConnect = random.randint(0, len(groupB)-1)
                    if i["Family"] == groupB[newConnect]["Family"]:
                        sameFamily = True
                    else: sameFamily = False
                    
                    if self.agents.are_connected(i.index, groupB[newConnect].index):
                        exists = True
                    else: exists = False            
                    
                self.agents.add_edge(i, groupB[newConnect])
                j += 1
                        
    def addOutgroupConnects(self):
        
        groupA = self.agents.vs.select(Group_eq = "A")
        groupB = self.agents.vs.select(Group_eq = "B")
        
        counter = 0
        
        while counter < self.xConnects:
            exists = True
            while exists:
                vertA = random.randint(0, len(groupA)-1)
                vertB = random.randint(0, len(groupB)-1)
                if self.agents.are_connected(groupA[vertA].index, groupB[vertB].index):
                    exists = True
                else: exists = False
                
            self.agents.add_edge(groupA[vertA], groupB[vertB])
            counter += 1
            
    def logStart(self):
        numSick = 0
        numImmune = 0
        for i in self.agents.vs:
            if i["Agent"].getDisease():
                numSick = numSick + 1
                i["Status"] = "S"
            else: numSick = numSick
            
            if i["Agent"].getImmunity():
                i["Status"] = "I"
                numImmune = numImmune + 1
            else: numImmune = numImmune
        
        self.initialSick = numSick
        self.initialImmune = numImmune
        
    def logEnd(self):
        numSick = 0
        numImmune = 0
        for i in self.agents.vs:
            if not(i["Agent"].getDeadValue() == True):
                if (i["Agent"].getDisease() == True):
                    numSick = numSick + 1
                
                if (i["Agent"].getImmunity() == True):
                    i["Status"] = "I"
                    numImmune = numImmune + 1
        
        self.finalSick = numSick
        self.finalImmune = numImmune
        
    def updateSickTime(self):
        for i in self.agents.vs:
            if not(i["Agent"].getDeadValue() == True):
                if (i["Agent"].getDisease() == True):
                    i["Status"] = "S"
                    i["Agent"].diseaseTime = (i["Agent"].diseaseTime + 1)
                    i["Agent"].checkDiseaseTime()
                else: i["Status"] = "H"
                    
    def updateDead(self):
        for i in self.agents.vs:
            if (i["Agent"].getValue() <= 0):
                i["Agent"].deadVal = True
                i["Agent"].value = 0
                i["Agent"].diseaseTime = None
                i["Status"] = "D"
                
    def calcNumDied(self):
        self.numDied = 0
        for i in self.agents.vs:
            if i["Agent"].getDeadValue() == True:
                self.numDied = self.numDied + 1
                
        return self.numDied

    def calcRo (self):
        numInfected = 0.0
        numTransmitted = 0.0
        Ro = None
        for i in self.agents.vs:
            if i["Agent"].getDisease() == True:
                numInfected  = numInfected + 1
                numTransmitted = numTransmitted + i["Agent"].getNumTransmitted()
                Ro = round(float(numTransmitted) / float(numInfected), 3)
        return Ro 
        
    def createInitialGraph(self):
        self.agents.vs["label"] = self.agents.vs["Group"]
        color_dict = {"H": "blue", "S": "green", "D": "red", "I": "yellow"}
        self.agents.vs["color"] = [color_dict[Status] for Status in self.agents.vs["Status"]]
        layout = self.agents.layout("kk")
        matrixPlot = igraph.plot(self.agents, layout = layout, bbox = (600, 600), margin = 20)
        self.initialGraph = matrixPlot

        

        

                