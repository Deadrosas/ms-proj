from network_aware_agent.network_aware_agent import *
from reactive_driver_agent.reactive_agent import *

class Agent:
    
    def __init__(self,id,start,goal,color,type,agent_class,edges):
        self.id = id
        self.start = start
        self.goal = goal
        self.color = color
        self.type = type

        self.edges = edges
        

        match agent_class:
            case "NetworkAwareDriverAgent":
                self.agent = NetworkAwareDriverAgent(self.id,edges,self.goal)
    

            case "ReactiveDriverAgent":
                self.agent = ReactiveDriverAgent(self.id,edges,self.goal)
            case _:
                self.agent = NetworkAwareDriverAgent(self.id,edges,self.goal)

    def setPath(self,path):
        self.path = path
    def getPath(self):
        return self.path