from Strat import *
from team import team1, team2,team22, team4, team11

try:
    f=open('dico.pkl','r')
    qlearn=cPickle.load(f)
    f.close()
    break
except IOError:
    qlearn=None

#LOOP    changer strat a chaque tour de boucle
"""
ON UTILISE PLUTOT UNE COLLECTION DE MATCH
--> scenario est donc une liste de scenario
match=SoccerMatch(team2,team22)
match.play()
"""
states=match.states
#actions=match.action

scenario=(states, actions) 

if team2==match.team1:
    x=0 # pas sur team1==0
else:
    x=1

qlearn=learn_q(x,0, qlearn, scenario,0.1,0.9)
#END LOOP


cPickle.dump(qlearn,file('dico.pkl','w'))
