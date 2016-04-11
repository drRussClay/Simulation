# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 09:18:22 2016

@author: Russ.Clay
"""
from Simulation import Simulation
from Export import Export
import os
import csv

# declare the number of simulations to run and the number to assign to the first
# simulation log file (files will increment sequentially from the first number)
numSims = 1
startNumber = 0
simLog = []

# define the format of the output file for summary information from each simulation run
def writeSimLog(simLog, startNumber):
    popStatVals = ["SimNumber", "StartPopSize", "InitialConnections", "PosVal", "AvoidVal", "SickVal", "SickTime", 
                  "DisTransRate", "ImmuneProb", "NumDied", "NumImmune"]
     
    os.chdir('C:/Users/russ.clay/Desktop/Simulations/Agent/Exports')
    with open('simulationLogData.csv', 'wb') as csvfile:
        datawriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)                      

        datawriter.writerow(popStatVals)
        for i in simLog:
            runVals = i.getRunVals()
            newRow=[]
            newRow.append(startNumber)
            for j in runVals:
                newRow.append(j)
            datawriter.writerow(newRow)
            startNumber += 1

# --------------------------------------------------------
# main code body
# create a new simulation, run it, and create all necessary output files for each simulation run

for i in range(startNumber, numSims+startNumber):
    newSim = Simulation(i)
    newSim.preSimSetup()
    simLog.append(newSim.runSim())
    
    newExport = Export(newSim)
    newExport.writeTimeLog(i)
    newExport.writeFinalPopulation(i)
    print('Finished Simulation ' + str(i))

#write the summary file for all simulation runs 
writeSimLog(simLog, startNumber)




