import agentspeak
import agentspeak.runtime
import agentspeak.stdlib


def calc_simple_path_cost(path):
    """Calculate the cost of a path.
    Each path is a list of edges. With it's associated weight.
    So a Path weight is the sum of all edges weights multiplied by their distance.

    """

    return(len(path))

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


@simple_driver_agent_actions.add_function(".calc_shortest_path", (list, ))
def calc_shortest_path(paths):
    return(min(paths, key=calc_simple_path_cost))