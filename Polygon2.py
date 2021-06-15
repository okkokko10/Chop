from Vector import Vector
from Line import Line

class Polygon:
    def __init__(self,vertices):
        self.vertexList=vertices.copy()
        self.nodes=[]
        for i in range(len(vertices)):
            self.nodes.append([i,i-1,i+1,i])
    def Cutter(self,line:Line):
        
class Node:
    def __init__(self,nextNode,value):
        self.nextNode=nextNode
    
