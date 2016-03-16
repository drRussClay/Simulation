# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 14:49:30 2016

@author: Russ.Clay
"""
"Class for Exporting Files"
" intLog = [i, newInt, newRule, newResult]"

import os
import csv
import igraph

class Export:
    def __init__(self, simulation):
        self.population = simulation.getPopulation()
        self.interactions = simulation.getIntLog()
        self.timeLog = simulation.getTimeLog()
        self.runVals = simulation.getRunVals()
        
    def writeInteractions(self):
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')

        with open('interactionData.csv', 'wb') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
            firstRow = ["TimeNum", "IntNum", "FirstAgent", "FirstAgentAvers", "FirstAgentStartVal",
                        "FirstAgentChange", "FirstAgentEndVal", "SecondAgent", "SecondAgentAvers", 
                        "SecondAgentStartVal", "SecondAgentChange", "SecondAgentEndVal", "IntResult"]  
            datawriter.writerow(firstRow)
            
            for i in range(0, len(self.interactions)):
                timeNum = self.interactions[i][0]
                intNum = self.interactions[i][1]
                firstAgent = self.interactions[i][2].getAgent1()
                secondAgent = self.interactions[i][2].getAgent2()
                position1 = str(firstAgent.getID())
                position2 = str(secondAgent.getID())
                a1StartVal = self.interactions[i][2].getAgent1StartVal()
                a2StartVal = self.interactions[i][2].getAgent2StartVal()
                a1EndVal = self.interactions[i][2].getAgent1EndVal()
                a2EndVal = self.interactions[i][2].getAgent2EndVal()
                result = self.interactions[i][4][0]
                agent1Change = self.interactions[i][4][1]
                agent2Change = self.interactions[i][4][2]
                
                newRow = [timeNum, intNum, position1, firstAgent.getOpenness(), a1StartVal,
                          agent1Change, a1EndVal, position2, secondAgent.getOpenness(),
                          a2StartVal, agent2Change, a2EndVal, result]
                datawriter.writerow(newRow)

    def writeTimeLog(self, simNum):
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')
        filename = 'timeLogData_' + str(simNum) + '.csv'
        with open(filename, 'wb') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                    
            for i in range(0, len(self.timeLog)-1):
                newRow = self.timeLog[i]
                datawriter.writerow(newRow)
                                
    def writeFinalPopulation(self, simNum):
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')
        filename = 'finalPopulationLogData_' + str(simNum) + '.csv'
        with open(filename, 'wb') as csvfile:
            datawriter = csv.writer(csvfile, delimiter=',',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                                    
            firstRow = ["ID", "Openness", "Value", "SickVal", "DeadVal",
                        "Disease", "DiseaseTime", "Immunity"]
            datawriter.writerow(firstRow) 
            
            for i in self.population.getVS():
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
                
    def writeMatrix(self, simNum):
        
        os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Images')
        self.population.initialGraph.save('StartingNetworkPlot.png')
        self.population.agents.vs["label"] = self.population.agents.vs["Group"]
        color_dict = {"H": "blue", "S": "green", "D": "red", "I": "yellow"}
        self.population.agents.vs["color"] = [color_dict[Status] for Status in self.population.agents.vs["Status"]]
        layout = self.population.agents.layout("fr")
        matrixPlot = igraph.plot(self.population.agents, layout = layout, bbox = (600, 600), margin = 20)
        matrixPlot.save('EndingNetworkPlot.png')
                
                