import os
import sys
import optparse
import xml.etree.ElementTree as ET

import time

from simple_driver_agent.simple_driver_agent import *

from simple_driver_agent.simple_driver_agent_components import *

from edge import *
from agent import *

vehicles = {}

vehicle_times = {}

vehicle_edge = {}

edges = {}

agents = {}

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("SUMO_HOME is not set!!!")




from sumolib import checkBinary

import traci


def get_options():
    """get the command line options"""
    opt_parser = optparse.OptionParser()
    opt_parser.add_option('--nogui', action="store_true",
                                    default= False, help= "run the commandline version of SUMO")
    options, args = opt_parser.parse_args()
    return options

def get_average_cost(lanes):
    """Get the average cost of the lanes"""
    cost = 0
    for lane in lanes:
        cost += float(lane.attrib["length"])/ float(lane.attrib["speed"])
    return cost/len(lanes)

def parse_network(path = "../SUMO_Simulations/Basic/basic.net.xml"):
    tree = ET.parse(path)

    root = tree.getroot()

    edges_xml = root.findall("edge")

    connections = root.findall("connection")
    edge_cost = []
    connection_list = []
    # Get Edges only and exclude junctions and internal edges
    for edge in edges_xml:
        lanes = edge.findall("lane")
        edge_cost = get_average_cost(lanes)
        edge_id = edge.attrib["id"] if edge.attrib["id"].startswith("E") else None
        if edge_id != None:
            edges[edge_id] = Edge(edge_id, edge_cost)
    
    for connection in connections:
        connect = (connection.attrib["from"], connection.attrib["to"]) if connection.attrib["from"].startswith("E") and connection.attrib["to"].startswith("E") else None
        connection_list.append(connect) if connect != None and connect not in connection_list else None

    for edge in edges:
        
        edges[edge].add_previous(list(map(lambda x: x[0], filter(lambda x: x[1] == edge, connection_list))))
        edges[edge].add_next(list(map(lambda x: x[1], filter(lambda x: x[0] == edge, connection_list))))

    #print(connection_list)
    #print(edge_list)
    
    #print (edges)
   # print(edges)
   # print(connections)

def parse_agents(path):
    tree = ET.parse(path)
    root = tree.getroot()

    agents_xml = root.findall("agent")

    for agent in agents_xml:
        agents[agent.attrib["id"]] = Agent(agent.attrib["id"],agent.attrib["start"],agent.attrib["goal"],agent.attrib["color"],agent.attrib["type"])
        



"""Deal with AgentSpeak code here"""

# actions = agentspeak.Actions(agentspeak.stdlib.actions)

env = agentspeak.runtime.Environment()

current_agents = {}

#TODO: Get paths from routes.xml
paths = ((("E1", 3), ("E2", 40), ("E3", 5))
        ,(("E14", 3), ("E13", 4), ("E12", 5), ("E11", 2), ("E10", 2), ("E9", 1), ("E8", 2), ("E7", 5), ("E6", 2), ("E5", 1), ("E4", 1)))

def run():
    """execute the TraCI control loop"""
    step = 0
    
    startAgents()

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
    

        vehicles = traci.vehicle.getIDList()

        print(vehicles)
        
        
        updateVehicles(vehicles)
        updateTimes(vehicles)


        step += 1



    traci.close()

   
    print(vehicle_edge)
    print(vehicle_times)

    sys.stdout.flush()


def startAgents():
    for agent in agents:
        current_agents[agent.id] = SimpleDriverAgent(agent.id, paths)
        current_vehicles[vehicle].calc_path(paths)
        
       


def updateVehicles(vehicles):

    for vehicle in vehicles:

        if vehicle.startswith("agent") and vehicle.split(".")[0] not in vehicle_edge:
            
            print("New Agent {} is on the edge {}".format(vehicle, traci.vehicle.getRoadID(vehicle)))

            vehicle_id = vehicle.split(".")[0]
            
            vehicle_times[vehicle_id] = {}
            vehicle_edge[vehicle_id] = traci.vehicle.getRoadID(vehicle)
            vehicle_times[vehicle_id][traci.vehicle.getRoadID(vehicle)] = 0


def updateTimes(vehicles):

    delta_t = traci.simulation.getDeltaT()
    for vehicle in (vehicle for vehicle in vehicles if vehicle.startswith("agent")):
            
            vehicle_id = vehicle.split(".")[0]
            
            current_edge = traci.vehicle.getRoadID(vehicle)

            #check if vehicle edge changed
            if vehicle_edge[vehicle_id] != current_edge: 
                ##Check if it's an edge
                if current_edge[0] == 'E':
                    vehicle_edge[vehicle_id] = current_edge #update current edge
                    vehicle_times[vehicle_id][current_edge] = 0 #elapsed time for new edge
                    print("Agent " + vehicle_id + "on a new edge " + current_edge)

            else:
                vehicle_times[vehicle_id][current_edge] += delta_t #update time in current edge
                print("Updating time for vehicle " + vehicle_id + "on edge " + current_edge + " with time " + str(vehicle_times[vehicle_id][current_edge]) )
 
            # vehicles[vehicle] = sda.SimpleDriverAgent(env, vehicle, actions)
            # traci.vehicle.getLastActionTime(vehicle)
           # if vehicle_id not in current_agents:
               # current_agents[vehicle_id] = SimpleDriverAgent(vehicle, paths)
                
               # print("Initialized Agent {} is on the edge {}".format(vehicle, traci.vehicle.getRoadID(vehicle)))

           # current_vehicles[vehicle].calc_path(paths)

        


if __name__ == "__main__":
    """main entry point"""
    
    if len(sys.argv) == 1:
        print("Format: main.py [simul_path]")
        print("simul_path is the path relative to the /SUMO_SIMULATIONS/ directory")
        exit(1)
    
    options = get_options()


    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    

    simul = sys.argv[1]

    pathSimul = "../SUMO_Simulations/" + simul + ".sumocfg"

    parse_network("../SUMO_Simulations/" + simul + ".net.xml")

    parse_agents("../SUMO_Simulations/" + simul+ ".agents.xml")

    traci.start([sumoBinary, "-c", pathSimul, "--tripinfo-output", "tripinfo.xml"])

    run()