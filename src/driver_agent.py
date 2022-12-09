import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

simple_driver_agent_actions = agentspeak.Actions(agentspeak.stdlib.actions)

@simple_driver_agent_actions.add_procedure(".call_my_plan",(agentspeak.runtime.Agent, str, str))
def call_my_plan(agent, txt1, txt2):
    """Call a plan in the agent's program."""
    print("call_my_plan was triggered")
    agent.call(
        agentspeak.Trigger.addition,
        agentspeak.GoalType.achievement,
        agentspeak.Literal("my_plan", (txt1.upper(), txt2.upper())),
        agentspeak.runtime.Intention())



class DriverAgent():
    
    def __init__(self, name):

        self.name = name


        
        with open(os.path.join(os.path.dirname(__file__), "../asl_files/agent_mult.asl")) as source:
            """Load the agent's program."""
            self.calc_path_agent_source = source

    def calc_path(self, path):
        
        agent = self.env.build_agent(self.calc_path_agent_source, self.actions)

        actions = agentspeak.Actions(agentspeak.stdlib.actions)

        @actions.add_procedure(".call_my_plan",(agentspeak.runtime.Agent, str))
        def call_my_plan(agent, txt):
             """Call a plan in the agent's program."""
            print("call_my_plan was triggered")
            agent.call(
            agentspeak.Trigger.addition,
            agentspeak.GoalType.achievement,
            agentspeak.Literal("my_plan", (txt.upper(), )),
            agentspeak.runtime.Intention())
    

            env = agentspeak.runtime.Environment()
        
        self.env.run_agent(agent)
        return


    def __repr__(self) -> str:
        return "SimpleDriverAgent" + self.name + " Actions: " + str(self.actions) + "Env: " + str(self.env)

    def __str__(self) -> str:
        return "SimpleDriverAgent: " + self.name + " Actions: " + str(self.actions) + "Env: " + str(self.env)

