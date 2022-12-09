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
    

def drive(self):
        """Call a plan in the agent's program."""
        self.agent.call(
            agentspeak.Trigger.addition,
            agentspeak.GoalType.achievement,
            agentspeak.Literal("drive", (self.name.upper(),)),
            agentspeak.runtime.Intention())

simple_driver_agent_env = agentspeak.runtime.Environment()


