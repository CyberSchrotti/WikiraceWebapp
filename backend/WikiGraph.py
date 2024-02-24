import time
import networkit as nk
import numpy as np
from pathlib import PurePath

class WikiGraph:

    def __init__(self, workingdir="", allTitlesPath="", adjacentListPath="", graphPath=""):
        
        self.workingdir = workingdir        
        self.allTitlesPath = str(PurePath(workingdir).joinpath(allTitlesPath))
        self.adjacentListPath = str(PurePath(workingdir).joinpath(adjacentListPath))
        self.graphPath = str(PurePath(workingdir).joinpath(graphPath))
        self.G = None
        self.pName2Index = dict()
        self.index2Pname = list()

    def loadGraphNK(self, graphPath=""):
        if len(graphPath) < 1 and len(self.graphPath) < 1:
            print("No graph path set")
            return
        if len(graphPath) > 0:
            print("load graph ", graphPath)
            self.G = nk.graphio.NetworkitBinaryReader().read(graphPath)
        else:
            print("load graph ", self.graphPath)
            self.G = nk.graphio.NetworkitBinaryReader().read(self.graphPath)

    def findPathNum(self, source, target):
        
        start_time = time.time()
        bfs = nk.distance.BFS(self.G, source, target=target)
        bfs.run()
        path = bfs.getPath(target)
        end_time = time.time()
        duration = end_time - start_time
        print("search took:", duration, "sec")
        return path        

    def findPathName(self, sourceName, targetName):

        if not sourceName in self.pName2Index:
            print(sourceName, "not found")
            return []
        if not targetName in self.pName2Index:
            print(targetName, "not found")
            return []
        
        sourceIndex = self.pName2Index[sourceName]
        targetIndex = self.pName2Index[targetName]

        indexPath = self.findPathNum(sourceIndex, targetIndex)
        namePath = [self.index2Pname[i] for i in indexPath]

        return namePath
    
    def pNameIsValid(self, name):
        return name in self.pName2Index

    def loadAllHeadingNS0Pretty(self, allTitlesPath=""):
        if len(allTitlesPath) < 1 and len(self.allTitlesPath) < 1:
            print("No all titles path set")
            return
        localpath = self.allTitlesPath
        if len(allTitlesPath) > 0:
            localpath = self.allTitlesPath

        self.pName2Index = dict()
        self.index2Pname = list()

        with open(localpath, "r", encoding="utf-8") as f:         

            for index, line in enumerate(f):
                cleanedLine = line.strip().replace("_", " ")    
                self.pName2Index[cleanedLine] = index
                self.index2Pname.append(cleanedLine)
                
