# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 11:15:33 2016

@author: Russ.Clay
"""
from Agent import Agent
import igraph
import random
import os


class Population:
    "The Population class defines and updates a population of agents"
    
    def __init__(self, popLimit, iProb, disease, xConnects, minFam, maxFam, igConnectLow, igConnectHigh):
        self.agents = igraph.Graph(directed = False) # initialize a graph that will hold the population of agents
        self.minFam = minFam # sets the minimum number of agents in a family (recieved from Class:Simulation)
        self.maxFam = maxFam # sets the maximum number of agents in a family (recieved from Class:Simulation)
        self.igConnectLow = igConnectLow # sets the minimum number of ingroup connections (recieved from Class:Simulation)
        self.igConnectHigh = igConnectHigh # sets the maximum number of ingroup connections (recieved from Class:Simulation)
        self.iProb = iProb # sets the probability that any agent is naturally immune to disease
        self.disease = disease # holds an instance of Class:Disease that can infect agents in the population
        self.popLimit = popLimit # sets the maximum size of the population
        self.popSize = 0 # holds the current size of the population
        self.numInfected = None # holds the current number of infected individuals
        self.numFamilies = 0 # holds the current number of families in the population
        self.initialSick = None # captures the number of agents with disease in the population at time 0
        self.initialImmune = None # captures the number of agents immune to disease at time 0
        self.finalSick = None # captures the number of agents with disease at the end of the simulation
        self.finalImmune = None # captures the number of agents with immunity at the end of the simulation
        self.numDied = None # holds the number of agents that died during the simulation
        self.xConnects = xConnects # holds the number of cross-group connections that will be generated each time period
        self.families = [] # holds a list of the families in the simulation (families are lists of agents)
        
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
           
    def get_iProb(self):
        return self.iProb
        
    def getDisease(self):
        return self.disease
                      
    def getSize(self):
        return self.popSize
        
    def getNumInfected(self):
        return self.numInfected
        
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

#--------------------                        
# --- Class Functions
#--------------------

    def setPop(self):
        self.addFamilies()
        self.addIngroupConnects()
        self.addOutgroupConnects()
    
    def addFamilies(self):    
        while self.popSize < self.popLimit: # create new agents in bundles of families while the population is less than the maximum size
            startVert = len(self.agents.vs)            
            popLeft = self.popLimit - self.popSize
            newVerts = random.randint(self.minFam, self.maxFam)
            
            # ensure that the final family group added does not exceed the maximum population size
            if newVerts < popLeft:
                addVerts = newVerts
            else: addVerts = popLeft
            
            #create new set of verticies that will represent a family in the pouplation
            self.agents.add_vertices(addVerts)
            endVert = len(self.agents.vs)
            newFam = []
            groupNum = random.randint(1,2)
            
            # initialize instances of Class:Agent to be stored at each vertex, and assign necessary properties to each agent / vertex
            for i in range(startVert, endVert):
                newAgent = Agent()
                newAgent.setID(i) # unique ID for each agent
                self.agents.vs(i)["Agent"] = newAgent # store the agent at the vertex
                self.agents.vs(i)["Index"] = str(i) # create a string representation of the unique ID for logging and reporting
                self.agents.vs(i)["Status"] = "H" # set the current disease status of the agent to 'H' (Healthy)
                self.agents.vs(i)["Family"] = str(self.numFamilies) # set an identifier of the family that the agent belongs to (family number increments with each new group created)
                # designate the agent as a member of 'Group A' or 'Group B' based on the randomly generated number above                
                if groupNum == 1:
                    self.agents.vs(i)["Group"] = "A"
                else: self.agents.vs(i)["Group"] = "B"
                newFam.append(i)
#                print "Added agent " + str(i) #debugging                
            
            # Create connections between all members of the family and designate those as family connections
            for i in range(startVert, endVert-1):
                for j in range(i+1, endVert):
                    self.agents.add_edge(i, j)
                    self.agents.es(len(self.agents.es)-1)["Relation"] = "Family"
                    
            self.families.append(newFam) # store the family in the family list            
            self.numFamilies+=1 # update the total number of families in the population
            self.popSize += addVerts # update the total number of agents in the population
            
    def addIngroupConnects(self): # create connections between ingroup members
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
                self.agents.es(len(self.agents.es)-1)["Relation"] = "Ingroup"
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
                self.agents.es(len(self.agents.es)-1)["Relation"] = "Ingroup"
                j += 1
                        
    def addOutgroupConnects(self): # add random connections between members of different groups     
        groupA = self.agents.vs.select(Group_eq = "A")
        groupB = self.agents.vs.select(Group_eq = "B")
        counter = 0
        
        # add connections until the number of desired connections is reached
        while counter < self.xConnects:
            exists = True
            while exists:
                vertA = random.randint(0, len(groupA)-1)
                vertB = random.randint(0, len(groupB)-1)
                if self.agents.are_connected(groupA[vertA].index, groupB[vertB].index):
                    exists = True
                else: exists = False
                
            self.agents.add_edge(groupA[vertA], groupB[vertB])
            self.agents.es(len(self.agents.es)-1)["Relation"] = "Outgroup"
            counter += 1
            
    def clearOutgroupConnects(self):  # clear outgroup connections (used at the beginning of each time period so that different, randomly generated outcroup connections occur throughout the simulation)      
        outgroup = self.agents.es.select(Relation_eq = "Outgroup")
        if len(outgroup) > 0:
            outgroup.delete() 
            
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
                self.popSize -= 1
                
    def calcNumDied(self):
        self.numDied = 0
        for i in self.agents.vs:
            if i["Agent"].getDeadValue() == True:
                self.numDied = self.numDied + 1
                
        return self.numDied

    def calcRo (self, priorInfected):
        if priorInfected == 0:
            return 0
        else:
            numInfected = 0.0
            Ro = None
            for i in self.agents.vs:
                if i["Agent"].getDisease() == True:
                    numInfected += 1
            newCases = numInfected - priorInfected
                            
            Ro = round(float(newCases) / float(priorInfected), 3)
            return Ro 
        
    def clearTransmissions(self):
        for i in self.agents.vs:
            i["Agent"].numTransmitted = 0
        
    def createGraph(self, timePeriod):
        self.agents.vs["label"] = self.agents.vs["Group"]
        color_dict = {"H": "blue", "S": "green", "D": "red", "I": "yellow"}
        self.agents.vs["color"] = [color_dict[Status] for Status in self.agents.vs["Status"]]
        layout = self.agents.layout("kk")
        matrixPlot = igraph.plot(self.agents, layout = layout, bbox = (600, 600), margin = 20)
        
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Images')
        filename = 'NetworkPlot_' + str(timePeriod) + '.png'
        matrixPlot.save(filename)

        

        

                