# import agentspeak
# import agentspeak.runtime
# import agentspeak.stdlib




# @simple_driver_agent_actions.add_procedure(".call_my_plan",(agentspeak.runtime.Agent, str, str))
# def call_my_plan(agent, txt1, txt2):
#     """Call a plan in the agent's program."""
#     print("call_my_plan was triggered")
#     agent.call(
#         agentspeak.Trigger.addition,
#         agentspeak.GoalType.achievement,
#         agentspeak.Literal("my_plan", (txt1.upper(), txt2.upper())),
#         agentspeak.runtime.Intention())


# @simple_driver_agent_actions.add_function(".calc_shortest_path", (tuple, ))
# def calc_shortest_path(paths):
#     # print(paths)
#     return(min(paths, key=calc_simple_path_cost))
