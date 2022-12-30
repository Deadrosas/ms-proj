import os
import sys
import optparse
import xml.etree.ElementTree as ET

import time

from simple_driver_agent.simple_driver_agent import *

from simple_driver_agent.simple_driver_agent_components import *

from edge import *

vehicles = {}

vehicle_times = {}

vehicle_edge = {}

edges = {}

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

    # print(connection_list)
    # print(edge_list)
    
    #print (edges)
    # print(edges)
    # print(connections)




"""Deal with AgentSpeak code here"""

# actions = agentspeak.Actions(agentspeak.stdlib.actions)

env = agentspeak.runtime.Environment()

current_vehicles = {}

#TODO: Get paths from routes.xml
paths = ((("E1", 3), ("E2", 40), ("E3", 5))
        ,(("E14", 3), ("E13", 4), ("E12", 5), ("E11", 2), ("E10", 2), ("E9", 1), ("E8", 2), ("E7", 5), ("E6", 2), ("E5", 1), ("E4", 1)))

def run():
    """execute the TraCI control loop"""
    step = 0
    

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        

        

        # vehicles = traci.edge.getLastStepVehicleIDs("E0")

        vehicles = traci.vehicle.getIDList()
        

        delta_t = traci.simulation.getDeltaT()
        updateVehicles(vehicles)
        for vehicle in vehicles:
            
            current_edge = traci.vehicle.getRoadID(vehicle)
        
            #check if vehicle edge changed
            if vehicle_edge[vehicle] != current_edge: 
                ##Check if it's an edge
                if current_edge[0] == 'E':
                    vehicle_edge[vehicle] = current_edge #update current edge
                    vehicle_times[vehicle][current_edge] = 0 #elapsed time for new edge

            else:
                vehicle_times[vehicle][current_edge] += delta_t #update time in current edge

            # vehicles[vehicle] = sda.SimpleDriverAgent(env, vehicle, actions)
            # traci.vehicle.getLastActionTime(vehicle)
            if vehicle not in current_vehicles:
                current_vehicles[vehicle] = SimpleDriverAgent(vehicle, paths)
                print("Vehicle {} is on the edge {}".format(vehicle, traci.vehicle.getRoadID(vehicle)))

            current_vehicles[vehicle].calc_path(paths)

            

            connected_edges = traci.edge.getIDList()

           # print(connected_edges)

            

        # traci.vehicle.getLastActionTime()

        # if step % 100 == 0:
        #     print(step)

        if step % 100 == 0 and step != 0:
            print(current_vehicles)
        #     for vehicle in current_vehicles:
        #         print(current_vehicles[vehicle])
        #         current_vehicles[vehicle].calc_path(paths)
            
        # #     traci.vehicle.changeTarget("carflow.0", "E4")
        # #     traci.vehicle.changeTarget("carflow.2", "E4")


        step += 1



    traci.close()

    print(vehicle_times)

    sys.stdout.flush()


def updateVehicles(vehicles):

    for vehicle in vehicles:
        
        if vehicle not in vehicle_edge:

            print(traci.vehicle.getRoadID(vehicle))
            vehicle_times[vehicle] = {}
            vehicle_edge[vehicle] = traci.vehicle.getRoadID(vehicle)
            vehicle_times[vehicle][traci.vehicle.getRoadID(vehicle)] = 0


    
       
        


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

    traci.start([sumoBinary, "-c", "../SUMO_Simulations/Basic/basic.sumocfg", "--tripinfo-output", "tripinfo.xml"])

    run()