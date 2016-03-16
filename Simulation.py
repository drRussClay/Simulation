# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 10:51:46 2016

@author: Russ.Clay
"""
from Population import Population
from Interaction import Interaction
from Disease import Disease
from Rules import Rules
import time
import random
import os
import csv

class Simulation:

    def __init__(self, simNum):
        self.simNum = simNum
        self.numTimePeriods = 100
        self.logInteractions = True
        self.popSize = 100 #Size of the population
        self.minFam = 2
        self.maxFam = 6
        self.igConnectLow = 2
        self.igConnectHigh = 5
        self.xConnects = round(.2 * self.popSize)
        self.intsPerTime = .2 # interactions as a proportion of the population per time period
        self.meanPosVal = 5 #Mean value of an interaction
        self.meanAvoidVal = 0 #Mean value of avoiding an interaction
        self.disRisk = .05 #Probability of being a disease carrier at the start of the simulation)
        self.immuneProb = .05 #Probability of being immune to disease at the start of the simulation
        self.newDisease = Disease()
        self.newPop = Population(self.popSize, self.disRisk, self.immuneProb, self.newDisease, self.xConnects, self.minFam, self.maxFam, self.igConnectLow, self.igConnectHigh)
        self.intLog = []
        self.totalInts = 0
        self.timeLog = []
        self.startTime = None
        self.endTime = None
        self.timePerInt = None
        self.runTime = None
        self.runVals = None
        
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
        
    def getIGConnectLow(self):
        return self.igConnectLow
        
    def getIGConnectHigh(self):
        return self.igConnectHigh
              
    def getIntsPerTime(self):
        return self.intsPerTime
                
    def getMeanPosVal(self):
        return self.meanPosVal
        
    def getMeanAvoidVal(self):
        return self.meanAvoidVal
        
    def getDisRisk(self):
        return self.disRisk
        
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
        
# --- Additional Functions
    
    def preSimSetup(self):
        self.newPop.setPop()
        self.newPop.logStart() 
        self.newPop.createInitialGraph()
        self.runVals = [(self.popSize), (self.intsPerTime * self.popSize), self.meanPosVal, self.meanAvoidVal, 
                        self.newDisease.getSickValue(), self.newDisease.getSickTime(), self.disRisk, 
                        self.newDisease.getTransRate(), self.immuneProb]
        
        timeLogFirstRow = ["Time", "PopSize", "NumSick", "NumImmune", "New Disease Transmissions", "Effective R0", "NumInteractions"]
        self.timeLog.append(timeLogFirstRow)

        timeLogStartRow = [0, self.newPop.getSize(), self.newPop.getInitialSick(), 
                           self.newPop.getInitialImmune(), 0, 0, 0]
        self.timeLog.append(timeLogStartRow)

        self.startTime = time.time()
        self.writeInitialPop()

    def runSim(self):
        lowPopFlag = False
        for  i in range(1, self.numTimePeriods+1):
            if lowPopFlag: break
            newTrans = 0
            numInts = int(round(self.intsPerTime * self.newPop.getSize()))
            for j in range(1,numInts+1):
                deadCheck = True
                while deadCheck:
                    edgeNum = random.randint(0, len(self.newPop.agents.es)-1)
                    randEdge = self.newPop.agents.es[edgeNum]
                    vert1 = self.newPop.agents.vs[randEdge.source]
                    vert2 = self.newPop.agents.vs[randEdge.target]
                    agent1 = vert1["Agent"]
                    agent2 = vert2["Agent"]
                    newInt = Interaction(agent1, agent2)
                    deadCheck = newInt.deadCheck()                           
                newInt.setStartVals()
                newRule = Rules([agent1, agent2])
                
                newResult = newRule.gameResult(self.meanPosVal, self.meanAvoidVal)
                if newResult[0] == "Avoid":
                    vert1["Agent"].updateValue(newResult[1])
                    vert2["Agent"].updateValue(newResult[2])
                else: 
                    newTrans = newTrans + vert1["Agent"].updateDisease(vert2["Agent"], newResult[1])
                    newTrans = newTrans + vert2["Agent"].updateDisease(vert1["Agent"], newResult[2])
            
                newInt.setEndVals()
                
                if self.logInteractions == True:
                    interaction = [i, j, newInt, newRule, newResult]
                    self.intLog.append(interaction)
                
            
            self.newPop.updateSickTime()
            self.newPop.updateDead()
            self.totalInts = self.totalInts + numInts
                
            self.newPop.logEnd()
            R0 = self.newPop.calcRo()
            
            newLogVals = [i, self.newPop.getSize(), self.newPop.getFinalSick(), 
                          self.newPop.getFinalImmune(), newTrans, R0, numInts]
            self.timeLog.append(newLogVals)
            print('Completed time ' + str(i))
            if lowPopFlag: break
    
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
    
        print('The simulation ran in ' + str(self.runTime) + ' seconds')
        print('Total number of interactions simulated: ' + str(self.totalInts))
        print('Effective time per interaction: ' + str(self.timePerInt))
    
        return self
        
    def writeInitialPop(self):
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')
        filename = 'initialPopulationLogData_' + str(self.simNum) + '.csv'
        with open(filename, 'wb') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                    
            firstRow = ["ID", "Openness", "Value", "SickVal", "DeadVal",
                        "Disease", "DiseaseTime", "Immunity"]
            datawriter.writerow(firstRow) 
                 
            for i in self.newPop.agents.vs:
                tempAgent = i["Agent"]
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
                
                newRow = [ID, opn, val, sck, ded, dis, dtm, imm]
                datawriter.writerow(newRow)

