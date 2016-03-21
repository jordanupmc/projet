from Strat import *
from team import team1, team2,team22, team4, team11


match=SoccerMatch(team2,team22)
match.play()

states=match.states

"""
actions=list()
for i in range(len(states)-1):
    actions.append(states[i].player_action(2,1))
""" 
scenario=(states, actions)
qlearn=learn_q(0,0, None, scenario,0.1,0.9)
