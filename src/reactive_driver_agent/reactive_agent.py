import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os


'''The Agent looks 1 edge ahead and chooses the edge with the least cost. No matter the cost of the edges after that one.'''
class ReactiveDriverAgent():
    

    def __init__(self, name, destination, start = "E0"):

        self.name = name

        self.destination = destination

        self.known_paths = []
        
        self.start = start



    def calc_path(self, edges_dictionary):


        # print("PATHS:----------------")
        # print(paths)
        
        # ----------------------------- AGENTSPEAK -----------------------------
        calc_path_action = agentspeak.Actions(agentspeak.stdlib.actions) 

        
        @calc_path_action.add_function(".get_next_edges", (tuple, ))
        def get_next_edges(edge):
            
            return edges_dictionary[edge].get_next()

        # -----------------------------------------------------------------------


        # ----------------------------- CREATE ENVIRONMENT -----------------------------
        env = agentspeak.runtime.Environment()

        with open(os.path.join(os.path.dirname(__file__), "calc_path_complex.asl")) as source:
            agent = env.build_agent(source, calc_path_action)

        # ------------------------------------------------------------------------------
        
        # ----------------------------- ADD BELIEFS -------------------------------------
        
        """Add a belief to the agent. The tuple paths is added as 'paths' to the agent."""
        agent.add_belief(agentspeak.Literal("start", (self.start,)), agentspeak.runtime.Intention())
        agent.add_belief(agentspeak.Literal("destination", (self.destination,)), agentspeak.runtime.Intention())
        
        # -----------------------------------------------------------------------------

        # ----------------------------- RUN AGENT -----------------------------
        env.run_agent(agent)
        return


    def __repr__(self) -> str:
        return "SimpleDriverAgent" + self.name

    def __str__(self) -> str:
        return "SimpleDriverAgent: " + self.name

