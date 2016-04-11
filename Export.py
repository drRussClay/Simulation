# -*- coding: utf-8 -*-
"""
Created on Sat Jan 16 14:49:30 2016

@author: Russ.Clay
"""
"Class for Exporting Files"
" intLog = [i, newInt, newRule, newResult]"

import os
import csv

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
            firstRow = ["TimeNum", "IntNum", "Agent1", "Agent1-Openness", "Agent1-Family",
                        "Agent1-Group", "Agent1-StartVal", "Agent1-Change", "Agent1-EndVal", 
                        "Agent2", "Agent2-Openness", "Agent2-Family", "Agent2-Group", "Agent2-StartVal", 
                        "Agent2-Change", "Agent2-EndVal", "IntResult", "IntType"]  
            datawriter.writerow(firstRow)
            
            for i in range(0, len(self.interactions)):
                timeNum = self.interactions[i][0]
                intNum = self.interactions[i][1]
                interaction = self.interactions[i][2]
                vertPair = self.interactions[i][3]
                result = self.interactions[i][4]
                intType = self.interactions[i][5]
                
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
                                    
            firstRow = ["ID", "Family", "Group", "Openness", "Value", "SickVal", "DeadVal",
                        "Disease", "DiseaseTime", "Immunity"]
            datawriter.writerow(firstRow) 
                 
            for i in self.population.agents.vs:
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

                

                
                