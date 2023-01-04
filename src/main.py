import os
import sys
import optparse
import xml.etree.ElementTree as ET

import time

from network_aware_agent.network_aware_agent import *
from reactive_driver_agent.reactive_agent import *

from agent import *
from edge import *

vehicles = {}

vehicle_times = {}

vehicle_edge = {}

edges = {}

agents = {}

route_id = 0


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
        
        edges[edge].set_previous(list(map(lambda x: x[0], filter(lambda x: x[1] == edge, connection_list))))
        edges[edge].set_next(list(map(lambda x: x[1], filter(lambda x: x[0] == edge, connection_list))))


def parse_agents(path):
    tree = ET.parse(path)
    root = tree.getroot()

    agents_xml = root.findall("agent")

    for agent in agents_xml:
        agents[agent.attrib["id"]] = Agent(agent.attrib["id"],agent.attrib["start"],agent.attrib["finish"],agent.attrib["color"],agent.attrib["type"],agent.attrib["class"],edges)


"""Deal with AgentSpeak code here"""

# actions = agentspeak.Actions(agentspeak.stdlib.actions)

env = agentspeak.runtime.Environment()

current_vehicles = {}

def startAgents():
    
    global route_id

    for agent in agents:
        
        currentAgent = agents[agent]
        
        #current_agents[agent.id] = agent.agent    

        currentAgent.setPath(currentAgent.agent.calc_path())
        
    
        traci.route.add(str(route_id),currentAgent.getPath())
        traci.vehicle.add(agent,str(route_id),currentAgent.type,"now")
        route_id = route_id+1

        vehicle_times[agent] = {}
        vehicle_edge[agent] = traci.vehicle.getRoadID(agent)
        vehicle_times[agent][traci.vehicle.getRoadID(agent)] = 0
        


def run():
    """execute the TraCI control loop"""
    step = 0
    
    startAgents()

    print("Agents Started")

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        

        vehicles = traci.vehicle.getIDList()        

        
        updateAgents(vehicles)
        updateTimes()
       

        step += 1



    traci.close()

    #print(vehicle_times)

    sys.stdout.flush()


def updateEdges(agent):

    for edge in vehicle_times[agent.id]:
        
        if edge == '':
            continue

        if vehicle_times[agent.id][edge] > 0:
            
            agent.edges[edge].set_cost(vehicle_times[agent.id][edge])

def updateAgents(vehicles):

    global route_id

    for agent in agents:

        if agent not in vehicles:

            updateEdges(agents[agent])

            #agent ended, start again
            currentAgent = agents[agent]
            
            print(currentAgent.agent.calc_path())

            currentAgent.setPath(currentAgent.agent.calc_path())
            
            traci.route.add(str(route_id),currentAgent.getPath())
            traci.vehicle.add(agent,str(route_id),currentAgent.type,"now")
            route_id = route_id + 1

            vehicle_times[agent] = {}
            vehicle_edge[agent] = traci.vehicle.getRoadID(agent)
            vehicle_times[agent][traci.vehicle.getRoadID(agent)] = 0
            
            print(vehicle_times)
        
           
           

def updateTimes():

    delta_t = traci.simulation.getDeltaT()
    for agent in agents:
            
        
        current_edge = traci.vehicle.getRoadID(agent)

            #check if vehicle edge changed
        if vehicle_edge[agent] != current_edge: 
             ##Check if it's an edge
            if current_edge[0] == 'E':
                vehicle_edge[agent] = current_edge #update current edge
                vehicle_times[agent][current_edge] = 0 #elapsed time for new edge
                #print("Agent " + agent + "on a new edge " + current_edge)

        else:
            vehicle_times[agent][current_edge] += delta_t #update time in current edge
            #print("Updating time for vehicle " + agent + "on edge " + current_edge + " with time " + str(vehicle_times[agent][current_edge]) )
 

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

    print("../SUMO_Simulations/" + simul+ ".agents.xml")

    parse_network("../SUMO_Simulations/" + simul + ".net.xml")
    parse_agents("../SUMO_Simulations/" + simul+ ".agents.xml")

    traci.start([sumoBinary, "-c", pathSimul, "--tripinfo-output", "tripinfo.xml"])

    run()