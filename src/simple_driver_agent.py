import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

class SimpleDriverAgent():
    

    def __init__(self, actions, env, name):

        self.actions = actions
        self.env = env
        self.name = name


        with open(os.path.join(os.path.dirname(__file__), "../asl_files/agent_mult.asl")) as source:
            """Load the agent's program."""
            self.agent = self.env.build_agent(source, self.actions)
        
        self.env.run_agent(self.agent)

    
    def __repr__(self) -> str:
        return "SimpleDriverAgent" + self.name + " Actions: " + str(self.actions) + "Env: " + str(self.env)

    def __str__(self) -> str:
        return "SimpleDriverAgent: " + self.name + " Actions: " + str(self.actions) + "Env: " + str(self.env)

