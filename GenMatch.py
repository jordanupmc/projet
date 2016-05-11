import random 
from Strat import *
#Genere des matchs

strats=[OneOneStrategy(),GardienStrategy(), RandomStrategy(), FonceurStrategy(), CampeurStrategy()]
NB_MATCH=12

i=0
match=list()

while i<NB_MATCH:
    qt1=SoccerTeam("MonteCarlo1",[Player("Bravo",strats[random.randint(0,len(strats)-1)])])
    qt11=SoccerTeam("Coach1v1",[Player("D.Costa",strats[random.randint(0,len(strats)-1)])])
    sm=SoccerMatch(qt1,qt11)
    sm.play()
    match.append(zip(sm.states,sm.strats))
    
    i+=1

i=0
while i<NB_MATCH:
    qt2=SoccerTeam("MonteCarlo2",[Player("Zizou",strats[random.randint(0,len(strats)-1)]),Player("Bravo",strats[random.randint(0,len(strats)-1)])])
    qt22=SoccerTeam("Coach2v2",[Player("Zizou",strats[random.randint(0,len(strats)-1)]),Player("Bravo",strats[random.randint(0,len(strats)-1)])])
    
    sm=SoccerMatch(qt2,qt22)
    sm.play()
    match.append(zip(sm.states,sm.strats))
    
    i+=1
"""
i=0
while i<NB_MATCH:

    qt4=SoccerTeam("MonteCarlo4",[Player("t3j1",strats[random.randint(0,len(strats)-1)]),Player("Zizou",strats[random.randint(0,len(strats)-1)]),Player("Bravo",strats[random.randint(0,len(strats)-1)]),Player("Muller",strats[random.randint(0,len(strats)-1)])])

    qt44=SoccerTeam("Coach4v4",[Player("t3j1",strats[random.randint(0,len(strats)-1)]),Player("Zizou",strats[random.randint(0,len(strats)-1)]),Player("Bravo",strats[random.randint(0,len(strats)-1)]),Player("Muller",strats[random.randint(0,len(strats)-1)])])
    
    sm=SoccerMatch(qt4,qt44)
    sm.play()
    match.append(zip(sm.states,sm.strats))

    i+=1
"""

cPickle.dump(match,file('./genmatchs.pkl','wb'))
