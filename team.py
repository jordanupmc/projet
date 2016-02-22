from Strat import *

#team1=SoccerTeam("equipe1",[Player("Bravo",GardienStrategy())])
#team11=SoccerTeam("equipe11",[Player("Costa",FonceurStrategy())])

strat_key = KeyboardStrategy(fn="test.tree")
strat_key.add("a",RandomStrategy())
strat_key.add("z",FonceurStrategy())
strat_key.add("e",GardienStrategy())
tree=cPickle.load("tree.pkl")

team1=SoccerTeam("equipe1",[Player("Bravo",DTreeStrategy(tree...))])
team11=SoccerTeam("equipe11",[Player("Costa",FonceurStrategy())])

team2=SoccerTeam("equipe2",[Player("Zizou",FonceurStrategy()),Player("Bravo",GardienStrategy())])
team4=SoccerTeam("equipe4",[Player("t3j1",FonceurStrategy())],[Player("Zizou",FonceurStrategy()),Player("Bravo",GardienStrategy())],Player("Muller",GardienStrategy())])
