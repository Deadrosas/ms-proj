import os
import sys
import optparse

if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("SUMO_HOME is not set!!!")



from sumolib import checkBinary
import traci


def get_options():
    opt_parser = optparse.OptionParser()
    opt_parser.add_option('--nogui', action="store_true",
                                    default= False, help= "run the commandline version of SUMO")
    options, args = opt_parser.parse_args()
    return options



def run():
    step = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()

        if step % 100 == 0:
            print(step)

        if step == 100:
            print(traci.vehicle.getIDList())
            
            traci.vehicle.changeTarget("carflow.0", "E4")
            traci.vehicle.changeTarget("carflow.2", "E4")


        step += 1



    traci.close()
    sys.stdout.flush()


if __name__ == "__main__":
    options = get_options()


    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        sumoBinary = checkBinary('sumo-gui')

    
    traci.start([sumoBinary, "-c", "SUMO_Simulations\\Basic\\basic.sumocfg", "--tripinfo-output", "tripinfo.xml"])

    run()