import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

from simple_driver_agent_components import *


class SimpleDriverAgent():
    

    def __init__(self, name):

        self.actions = simple_driver_agent_actions
        self.name = name

        
        # self.calc_path_agent_source = source

    def calc_path(self, path):
        
        env = agentspeak.runtime.Environment()

        with open(os.path.join(os.path.dirname(__file__), "../asl_files/agent_mult.asl")) as source:
            agent = env.build_agent(source, self.actions)
        
        env.run_agent(agent)
        print(self.actions)
        return


    def __repr__(self) -> str:
        return "SimpleDriverAgent" + self.name + " Actions: " + str(self.actions)

    def __str__(self) -> str:
        return "SimpleDriverAgent: " + self.name + " Actions: " + str(self.actions)

