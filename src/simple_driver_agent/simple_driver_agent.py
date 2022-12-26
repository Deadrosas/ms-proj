import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

class SimpleDriverAgent():
    

    def __init__(self, name, paths):

        self.name = name
        self.paths = paths

        
        # self.calc_path_agent_source = source


    def calc_path(self, paths):
        
        # ----------------------------- AGENTSPEAK -----------------------------
        calc_path_action = agentspeak.Actions(agentspeak.stdlib.actions)


        def calc_simple_path_cost(path):

            return(sum(map(lambda x: x[1], path)))

        @calc_path_action.add_function(".calc_shortest_path", (tuple, ))
        def calc_shortest_path(paths):

            path = min(paths, key=calc_simple_path_cost)
            return path

        # ----------------------------- AGENTSPEAK -----------------------------


        # ----------------------------- CREATE ENVIRONMENT -----------------------------
        env = agentspeak.runtime.Environment()

        with open(os.path.join(os.path.dirname(__file__), "simple_driver_agent.asl")) as source:
            agent = env.build_agent(source, calc_path_action)

        # ----------------------------- CREATE ENVIRONMENT -----------------------------

        # ----------------------------- ADD BELIEFS -----------------------------
        
        agent.add_belief(agentspeak.Literal("paths", (tuple(paths),)), agentspeak.runtime.Intention())
        
        # ----------------------------- ADD BELIEFS -----------------------------

        # ----------------------------- RUN AGENT -----------------------------
        env.run_agent(agent)
        return


    def __repr__(self) -> str:
        return "SimpleDriverAgent" + self.name

    def __str__(self) -> str:
        return "SimpleDriverAgent: " + self.name

