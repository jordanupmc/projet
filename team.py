from Strat import *

team1=SoccerTeam("equipe1",[Player("Bravo",FonceurStrategy())])
team11=SoccerTeam("equipe11",[Player("Costa",GardienStrategy())])

team2=SoccerTeam("equipe2",[Player("t2j1",FonceurStrategy()),Player("",GardienStrategy())])
team4=SoccerTeam("equipe3",[Player("t3j1",RandomStrategy())])
