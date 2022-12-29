import agentspeak
import agentspeak.runtime
import agentspeak.stdlib
import random
from collections.abc import Iterable

import os

def calc_simple_path_cost(path):

    return(sum(map(lambda x: x[1], path)))

def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x

def build_paths(edge, destination_edge, edges, path = []):

    print("EDGE:---------------")
    print(edge)
    path = path + [edge.get_name()]

    print("PATH:---------------")
    print(path)

    if edge.get_name() == destination_edge.get_name():
        print("RETURN PATH")
        return path
    


    paths = []
    for next_edge in edge.get_next():

        # print(next_edge)
        new_path = build_paths(edges[next_edge], destination_edge, edges, path)
        
        print("NEW PATH:---------------")
        print(new_path)

        paths.append(new_path)
    
    return paths

    


class SimpleDriverAgent():
    

    def __init__(self, name, destination, start = "E0"):

        self.name = name

        self.destination = destination

        self.known_paths = []
        
        self.start = start



    def calc_path(self, edges_dictionary):
        
    

        starting_edge = edges_dictionary[self.start]

        destination_edge = edges_dictionary[self.destination]

        paths = build_paths(starting_edge, destination_edge, edges_dictionary)

        print("PATHS:----------------")
        print(paths)
        
        # ----------------------------- AGENTSPEAK -----------------------------
        calc_path_action = agentspeak.Actions(agentspeak.stdlib.actions) 


        """
        The python function calc_shortest_path is called when the agent intention '.calc_shortest_path' is called.
        It then does what the agent needs it to do. In this case it does everything ( calculates the shortest path )."""
        @calc_path_action.add_function(".calc_shortest_path", (tuple, ))
        def calc_shortest_path(paths):

            path = min(paths, key=calc_simple_path_cost)

            path_temp = random.choice(path)
            return path_temp

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
        return


    def __repr__(self) -> str:
        return "SimpleDriverAgent" + self.name

    def __str__(self) -> str:
        return "SimpleDriverAgent: " + self.name

