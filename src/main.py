import os
import sys
import optparse

from simple_driver_agent import *

from simple_driver_agent_components import *

vehicles = {}

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




"""Deal with AgentSpeak code here"""

# actions = agentspeak.Actions(agentspeak.stdlib.actions)

env = agentspeak.runtime.Environment()

current_vehicles = {}

def run():
    """execute the TraCI control loop"""
    step = 0


    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        vehicles = traci.edge.getLastStepVehicleIDs("E0")

        for vehicle in vehicles:
            # vehicles[vehicle] = sda.SimpleDriverAgent(env, vehicle, actions)
            
            if vehicle not in current_vehicles:
                current_vehicles[vehicle] = SimpleDriverAgent(vehicle)
                print("Vehicle {} is on the edge {}".format(vehicle, "E0"))



        # if step % 100 == 0:
        #     print(step)

        if step % 100 == 0 and step != 0:
            # print(current_vehicles)
            for vehicle in current_vehicles:
                print(current_vehicles[vehicle])
                current_vehicles[vehicle].calc_path("E4")
            
        #     traci.vehicle.changeTarget("carflow.0", "E4")
        #     traci.vehicle.changeTarget("carflow.2", "E4")


        step += 1



    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    """main entry point"""
    options = get_options()


    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    
    traci.start([sumoBinary, "-c", "../SUMO_Simulations/Basic/basic.sumocfg", "--tripinfo-output", "tripinfo.xml"])

    run()