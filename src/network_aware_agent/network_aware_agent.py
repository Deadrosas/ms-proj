import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os


def find_paths(edges, start, end, path=[]):
    # Add the start node to the path
    path = path + [(start, edges[start].get_cost())]

    # If the start node is the end node, return the path
    if start == end:
        return [path]

    # If the start node is not in the edge list, return an empty list
    if start not in edges:
        return []
    # Initialize an empty list to store the paths
    paths = []

    # Get the next nodes from the start node
    next_nodes = edges[start].get_next()

    # Recursively search for paths from the next nodes
    for node in next_nodes:
        new_paths = find_paths(edges, node, end, path)
        # Add the new paths to the list of paths
        for p in new_paths:
            paths.append(tuple(p))
    return paths
    


class NetworkAwareDriverAgent():
    

    def __init__(self, name, edges, destination, start = "E0"):

        self.name = name

        self.destination = destination

        self.known_paths = []
        
        self.start = start

        self.edges_dictionary = edges



    def calc_path(self):
        
        self.path = []

       

        paths = find_paths(self.edges_dictionary, self.start, self.destination)

        

        
        
        # ----------------------------- AGENTSPEAK -----------------------------
        calc_path_action = agentspeak.Actions(agentspeak.stdlib.actions) 


        def calc_simple_path_cost(path):
            return(sum(map(lambda x: x[1], path)))

        """
        The python function calc_shortest_path is called when the agent intention '.calc_shortest_path' is called.
        It then does what the agent needs it to do. In this case it does everything ( calculates the shortest path )."""
        @calc_path_action.add_function(".calc_shortest_path", (tuple, ))
        def calc_shortest_path(paths):
            path = min(paths, key=calc_simple_path_cost)
            self.path = path
            return path

        # -----------------------------------------------------------------------


        # ----------------------------- CREATE ENVIRONMENT -----------------------------
        env = agentspeak.runtime.Environment()

        with open(os.path.join(os.path.dirname(__file__), "calc_path.asl")) as source:
            agent = env.build_agent(source, calc_path_action)

        # ------------------------------------------------------------------------------

        # ----------------------------- ADD BELIEFS -------------------------------------
        
        """Add a belief to the agent. The tuple paths is added as 'paths' to the agent."""
        agent.add_belief(agentspeak.Literal("paths", (tuple(paths),)), agentspeak.runtime.Intention())
        
        # -----------------------------------------------------------------------------

        # ----------------------------- RUN AGENT -----------------------------
        env.run_agent(agent)
        return list(map(lambda x: x[0], self.path))


    def __repr__(self) -> str:
        return "SimpleDriverAgent" + self.name

    def __str__(self) -> str:
        return "SimpleDriverAgent: " + self.name

