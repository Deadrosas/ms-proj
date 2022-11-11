import agentspeak
import agentspeak.runtime
import agentspeak.stdlib

import os

actions = agentspeak.Actions(agentspeak.stdlib.actions)

@actions.add_procedure(".call_my_plan",(agentspeak.runtime.Agent, str))
def call_my_plan(agent, txt):
    """Call a plan in the agent's program."""
    agent.call(
        agentspeak.Trigger.addition,
        agentspeak.GoalType.achievement,
        agentspeak.Literal("my_plan", (txt.upper(), )),
        agentspeak.runtime.Intention())
    

env = agentspeak.runtime.Environment()

with open(os.path.join(os.path.dirname(__file__), "agent.asl")) as source:
    """Load the agent's program."""
    agent = env.build_agent(source, actions)


if __name__ == "__main__":
    """Run the agent."""
    env.run_agent(agent)