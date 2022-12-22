"""Example of calling a plan in an agent's program."""

import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

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

with open(os.path.join(os.path.dirname(__file__), "../asl_files/agent.asl")) as source:
    """Load the agent's program."""
    env.build_agents(source, 3, actions)

if __name__ == "__main__":
    """Run the agent."""
    env.run()