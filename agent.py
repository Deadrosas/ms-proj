import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

actions = agentspeak.Actions(agentspeak.stdlib.actions)





class Agent:
    def __init__(self, id, routes,route, agent_file):
        self.id = id
        self.routeTimes = routes
        self.agent_file = agent_file
        self.route = route

        @actions.add_procedure(".call_my_plan",(agentspeak.runtime.Agent, str))
        def call_my_plan(agent, txt):
            """Call a plan in the agent's program."""
            
            agent.call(
                agentspeak.Trigger.addition,
                agentspeak.GoalType.achievement,
                agentspeak.Literal("my_plan", (txt.upper(), )),
                agentspeak.runtime.Intention())

        self.env = agentspeak.runtime.Environment()

        with open(os.path.join(os.path.dirname(__file__), self.agent_file)) as source:
            """Load the agent's program."""
            self.agent = self.env.build_agent(source, actions)

    

    def update_routeTimes(new_routes):
        self.routeTimes = new_routes
    
    def getRoute():
        return self.route



    async def run():
        self.env.run_agent(self.agent)

