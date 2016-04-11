# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:51:46 2016

@author: Russ.Clay
"""
from Population import Population
from Interaction import Interaction
from Disease import Disease
import time
import random
import os
import csv

class Simulation:

    def __init__(self, simNum):
        self.simNum = simNum
        self.numTimePeriods = 50 # number of time periods that a simulation should run
        self.logInteractions = True # boolean indicating whether to log each interaction during the simulation (set to 'false' for large populations)
        self.popSize = 1000 #Size of the population
        self.minFam = 2 # minimum number of agents in each family
        self.maxFam = 6 # maximum number of agents in each family
        self.igConnectMin = 2 # minimum number of ingroup (non-family) connections for each agent
        self.igConnectMax = 5 # maximum number of ingroup (non-family) connections for each agent 
        self.xConnects = round(.1 * self.popSize) # set the number of outgroup connections as a proportion of the total population size
        self.meanPosVal = 1 # set the average health value change resulting from an interaction
        self.meanAvoidVal = -1 # set the average health value change resulting from avoiding an interaction
        self.immuneProb = 0 # set the probability that an agent has natural immunity from disease
        self.newDisease = Disease() # initialize a disease that can be spread in the poppulation
        self.newPop = Population(self.popSize, self.immuneProb, self.newDisease, self.xConnects, self.minFam, self.maxFam, self.igConnectMin, self.igConnectMax) # initialize a new population graph using the parameters set above
        self.intLog = [] # initialize a new interaction log as a list
        self.totalInts = 0 # initialize the total number of interactions to zero
        self.timeLog = [] # initialize a new log for summary statistics at each time period
        self.startTime = None # initialize the variable to hold the system time associated with the start of the simulation
        self.endTime = None # initialize the variable to hold the system time associated with the end of the simulation
        self.timePerInt = None # initialize the variable to hold the average time per interaction during the simulation
        self.runTime = None # initialize the variable to hold the total run time of the simultion
        self.runVals = None # initialize the variable to hold the log of parameters governing the simulation run
        
# --- Accessor Functions
    def getSimNum(self):
        return self.simNum
        
    def getNumTimePeriods(self):
        return self.numTimePeriods
        
    def getLogInteractions(self):
        return self.logInteractions
        
    def getPopSize(self):
        return self.getPopSize
        
    def getMinFam(self):
        return self.minFam
        
    def getMaxFam(self):
        return self.maxFam
        
    def getIGConnectMin(self):
        return self.igConnectMin
        
    def getIGConnectMax(self):
        return self.igConnectMax
              
    def getIntsPerTime(self):
        return self.intsPerTime
                
    def getMeanPosVal(self):
        return self.meanPosVal
        
    def getMeanAvoidVal(self):
        return self.meanAvoidVal
           
    def getImmuneProb(self):
        return self.immuneProb
        
    def getDisease(self):
        return self.newDisease
        
    def getPopulation(self):
        return self.newPop
        
    def getIntLog(self):
        return self.intLog
        
    def getTotalInts(self):
        return self.totalInts
        
    def getTimeLog(self):
        return self.timeLog
        
    def getStartTime(self):
        return self.startTime
        
    def getEndTime(self):
        return self.endTime
        
    def getTimePerInt(self):
        return self.timePerInt
        
    def getRunTime(self):
        return self.runTime
        
    def getRunVals(self):
        return self.runVals

#-------------------------        
# --- Class Functions
#-------------------------
    
    def preSimSetup(self):
        # Create initial Population
        self.newPop.setPop()
        
        # Select 1 random member of the population to be infected with disease
        randInfect = random.randint(0, len(self.newPop.agents.vs))
        self.newPop.agents.vs[randInfect]["Agent"].setDisease(self.newDisease)
        
        # Log the starting population values
        self.newPop.logStart() 
        self.newPop.createGraph(0)
        self.runVals = [(self.popSize), len(self.newPop.agents.es), self.meanPosVal, self.meanAvoidVal, 
                        self.newDisease.getSickValue(), self.newDisease.getSickTime(), 
                        self.newDisease.getTransRate(), self.immuneProb]
        
        timeLogFirstRow = ["Time", "PopSize", "NumSick", "NumImmune", "New Disease Transmissions", "Effective R0", "NumInteractions"]
        self.timeLog.append(timeLogFirstRow)
        
        if self.logInteractions == True:
            self.writeFirstIntLogRow()

        timeLogStartRow = [0, self.newPop.getSize(), self.newPop.getInitialSick(), 
                           self.newPop.getInitialImmune(), 0, 0, 0]
        self.timeLog.append(timeLogStartRow)

        self.startTime = time.time()
        self.writeInitialPop()

    def runSim(self):
        # iterate through the following steps for the defined number of time periods
        for  i in range(1, self.numTimePeriods+1):
            numInts = 0
            
            # generate a new group of random outgroup connections each time period
            self.newPop.clearOutgroupConnects()
            self.newPop.addOutgroupConnects()
            self.newPop.clearTransmissions()
            newTransStack = []  # initialize stack of potential disease transmission interactions - necessary so that agents can only spread disease a maximum of one connection away during each time period
            
            # iterate through the following steps for each connection (graph edge) in the population
            for j in self.newPop.agents.es:
#                print('Edge #' + str(j.index)) # debugging
                
                # extract agents from the connection
                vert1 = self.newPop.agents.vs[j.source]
                vert2 = self.newPop.agents.vs[j.target]
                agent1 = vert1["Agent"]
                agent2 = vert2["Agent"]
                newInt = Interaction(agent1, agent2)
                intType = j["Relation"]
                
                # check to see if either of the agents are dead
                deadCheck = newInt.deadCheck()  
                
                # execute the following if both agents are alive
                if not(deadCheck):
#                    print "Dead Check Passed"  # debugging                       
                    newInt.setStartVals() # capture the starting health values for both agents
#                    print "Interaction start values set" 
                    intPair = [vert1, vert2] # store the verticies to be passed to the gameResult() function
                    
                    newResult = self.gameResult(intPair, self.meanPosVal, self.meanAvoidVal) # determine whether the pair of agents interacted or avoided
                    
#                    print "Calculated interaction result" # debugging
                    
                    # update the health values of the agents based on the result of the interaction
                    vert1["Agent"].updateValue(newResult[1])
                    vert2["Agent"].updateValue(newResult[2])
                    
                    # if the agents interacted, determine whether disease transmission ocurred
                    if newResult[0] == "Interact":
                        newTransStack.append(vert1["Agent"].updateDisease(vert2["Agent"]))
                        newTransStack.append(vert2["Agent"].updateDisease(vert1["Agent"]))
                        numInts+=1  # increment the number of total interactions
#                        print "Interaction...checked and logged disease spread" # debugging
                    
                    newInt.setEndVals() # log the updated health values of the agents
#                    print "ending interaction values set" # debugging
                    
                    # if interaction logging is turned on, log the values captured during the interaction
                    if self.logInteractions == True:
                        interaction = [i, numInts, newInt, [vert1, vert2], newResult, intType]
                        self.intLog.append(interaction)
#                        print "appended interaction record to log" # debugging
                
            # after all interactions have ocurred for the time period, update disease spread (done separately so that disease does not spread throughout the population in a single time period)
            newTrans = self.updateDiseaseSpread(newTransStack)
#            print "determined disease spread" # debugging
            # increment the sick time for all agents who are infected with disease
            self.newPop.updateSickTime()
#            print "updated sick time"  # debug
            self.newPop.updateDead()  # iterate through the population to set the status of any agents with 0 or lower health value to 'Dead'
#            print "updated deceased population members"  # debug
            self.totalInts = self.totalInts + numInts # update the total number of interactions
#            print "updated number of interactions" # debugging
            
            # Log ending summary population statistics for the time period    
            self.newPop.logEnd()
#            print "logged ending values for time iteration"  #debugging
            R0 = self.newPop.calcRo(self.timeLog[len(self.timeLog)-1][2])
#            print "calculated R0 value" # debugging 
            self.newPop.createGraph(i)
            newLogVals = [i, self.newPop.getSize(), self.newPop.getFinalSick(), 
                          self.newPop.getFinalImmune(), newTrans, R0, numInts]
            self.timeLog.append(newLogVals)
            self.writeInteractions(i)
            print('Completed time ' + str(i)) # debugging
        
        # Update summary statistics after final time period
        newLogVals = [i, numInts, self.newPop.getFinalSick(), self.newPop.getFinalImmune(), newTrans]
        self.totalInts = self.totalInts + numInts
        self.timeLog.append(newLogVals)
        totalDied = self.newPop.calcNumDied()
        totalImmune = self.newPop.getFinalImmune()
        self.runVals.append(totalDied)
        self.runVals.append(totalImmune)
        self.endTime = time.time()
        self.runTime = round((self.endTime - self.startTime), 2)
        self.timePerInt = self.runTime / self.totalInts
        
        # Write out completed simulation statistics to the console
        print('The simulation ran in ' + str(self.runTime) + ' seconds')
        print('Total number of interactions simulated: ' + str(self.totalInts))
        print('Effective time per interaction: ' + str(self.timePerInt))
  
        # return a copy off the simulation instance to main for logging  
        return self

# -------------------
# --- Class Functions
#--------------------

    def gameResult(self, intPair, posVal, avoidVal):
        if intPair[0]["Family"] == intPair[1]["Family"]:
            newResult = self.famInteract(intPair, posVal, avoidVal)
        else:
            if intPair[0]["Group"] == intPair[1]["Group"]:
                newResult = self.ingroupInteract(intPair, posVal, avoidVal)
            else: newResult = self.outgroupInteract(intPair, posVal, avoidVal)
        
        return newResult
        
    def famInteract(self, intPair, posVal, avoidVal):
        randSeed = random.uniform(0,1)
        
        p1Interact = .95 + (intPair[0]["Agent"].getOpenness() * .05)
        p2Interact = .95 + (intPair[1]["Agent"].getOpenness() * .05)
        
        if (p1Interact < randSeed):
            newResult=self.avoidResult(avoidVal)
        else: 
            if(p2Interact < randSeed):
                newResult=self.avoidResult(avoidVal)
            else: newResult=self.interactResult(posVal)
            
        return newResult        
        
    def ingroupInteract(self, intPair, posVal, avoidVal):
        randSeed = random.uniform(0,1)
        
        p1Interact = .75 + (intPair[0]["Agent"].getOpenness() * .25)
        p2Interact = .75 + (intPair[1]["Agent"].getOpenness() * .25)
        
        if (p1Interact < randSeed):
            newResult=self.avoidResult(avoidVal)
        else: 
            if(p2Interact < randSeed):
                newResult=self.avoidResult(avoidVal)
            else: newResult=self.interactResult(posVal)
            
        return newResult 
        
        
    def outgroupInteract(self, intPair, posVal, avoidVal):
        randSeed = random.uniform(0,1)
        
        p1Interact = intPair[0]["Agent"].getOpenness() 
        p2Interact = intPair[1]["Agent"].getOpenness() 
        
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
        
    def updateDiseaseSpread(self, newTransStack):
        newTrans = 0
        
        for i in newTransStack:
            if not(i == False):
                agentID = i[0]
                disease = i[1]
                
                for j in self.newPop.agents.vs:
                    if j["Agent"].getID() == agentID:
                        j["Agent"].setDisease(disease)
                        
                newTrans+=1      
                
        return newTrans

    def writeInitialPop(self):
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')
        filename = 'initialPopulationLogData_' + str(self.simNum) + '.csv'
        with open(filename, 'wb') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                    
            firstRow = ["ID", "Family", "Group", "Openness", "Value", "SickVal", "DeadVal",
                        "Disease", "DiseaseTime", "Immunity"]
            datawriter.writerow(firstRow) 
                 
            for i in self.newPop.agents.vs:
                tempAgent = i["Agent"]
                family = i["Family"]
                group = i["Group"]
                ID = tempAgent.getID()
                opn = tempAgent.getOpenness()
                val = tempAgent.getValue()
                if tempAgent.getDisease():
                    sck = tempAgent.diseaseType.getSickValue()
                else: sck = None
                ded = tempAgent.getDeadValue()
                dis = tempAgent.getDisease()
                dtm = tempAgent.getDiseaseTime()
                imm = tempAgent.getImmunity()
                
                newRow = [ID, family, group, opn, val, sck, ded, dis, dtm, imm]
                datawriter.writerow(newRow)
                
    def writeFirstIntLogRow(self):
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')
    
        with open('interactionData.csv', 'wb') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',', lineterminator = '\n',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            firstRow = ["TimeNum", "IntNum", "Agent1", "Agent1-Openness", "Agent1-Family",
                        "Agent1-Group", "Agent1-StartVal", "Agent1-Change", "Agent1-EndVal", 
                        "Agent2", "Agent2-Openness", "Agent2-Family", "Agent2-Group", "Agent2-StartVal", 
                        "Agent2-Change", "Agent2-EndVal", "IntResult", "IntType"] 
            datawriter.writerow(firstRow)
                
    def writeInteractions(self, i):
            os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')
    
            with open('interactionData.csv', 'a') as csvfile:
                datawriter = csv.writer(csvfile, delimiter=',', lineterminator = '\n',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                
                for i in range(0, len(self.intLog)):
                    timeNum = self.intLog[i][0]
                    intNum = self.intLog[i][1]
                    interaction = self.intLog[i][2]
                    vertPair = self.intLog[i][3]
                    result = self.intLog[i][4]
                    intType = self.intLog[i][5]
                    
                    firstAgent = interaction.getAgent1()
                    secondAgent = interaction.getAgent2()
                    position1 = str(firstAgent.getID())
                    position2 = str(secondAgent.getID())
                    a1Openness = firstAgent.getOpenness()
                    a2Openness = secondAgent.getOpenness()
                    a1Family = vertPair[0]["Family"]
                    a2Family = vertPair[1]["Family"]
                    a1Group = vertPair[0]["Group"]
                    a2Group = vertPair[1]["Group"]
                    a1StartVal = interaction.getAgent1StartVal()
                    a2StartVal = interaction.getAgent2StartVal()
                    a1EndVal = interaction.getAgent1EndVal()
                    a2EndVal = interaction.getAgent2EndVal()
                    intResult = result[0]
                    agent1Change = result[1]
                    agent2Change = result[2]
                    
                    newRow = [timeNum, intNum, position1, a1Openness, a1Family, a1Group, a1StartVal,
                              agent1Change, a1EndVal, position2, a2Openness, a2Family, a2Group,
                              a2StartVal, agent2Change, a2EndVal, intResult, intType]
                    datawriter.writerow(newRow)
                    
                self.intLog = []
                

