import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

def add_procedure(actions, name, signature):
    """Add a procedure to the agent's program."""
    actions.add_procedure(name, signature)

class SimpleDriverAgent(agentspeak.runtime.Agent):
    actions = agentspeak.Actions(agentspeak.stdlib.actions)

    def __init__(self, env, name):
        super().__init__(env, name)

        self.env = env
        self.name = name

        self.env.add_agent(self)


    def run(self):
        self.env.run_agent(self)


    @add_procedure(actions, ".call_my_plan", (agentspeak.runtime.Agent, str))
    def call_my_plan(self, txt):
        """Call a plan in the agent's program."""
        print("call_my_plan was triggered")
        self.call(
            agentspeak.Trigger.addition,
            agentspeak.GoalType.achievement,
            agentspeak.Literal("my_plan", (txt.upper(), )),
            agentspeak.runtime.Intention())