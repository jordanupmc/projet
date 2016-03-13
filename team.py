from Strat import *

team11=SoccerTeam("equipeBravo",[Player("Bravo",OneOneStrategy())])
team1=SoccerTeam("Diego Costa",[Player("D.Costa",OneOneStrategy())])
#team11=SoccerTeam("equipe11",[Player("Costa",KeyboardStrategy())])


'''
import os
fn=os.path.join(os.path.dirname(os.path.realpath(__file__)),"tree.pkl")
tree = cPickle.load(file(fn))
dic = {"Random":RandomStrategy(),"Fonceur":FonceurStrategy(),"Gardien":GardienStrategy()}

print affiche_arbre(tree)
treeStrat = DTreeStrategy(tree,dic,gen_features)


strat_key = KeyboardStrategy(fn="test.tree")
strat_key.add("a",RandomStrategy())
strat_key.add("z",FonceurStrategy())
strat_key.add("e",GardienStrategy())
'''

#team1=SoccerTeam("equipe1",[Player("Bravo", FonceurStrategy())])
#team1=SoccerTeam("equipe1",[Player("Bravo", treeStrat)])
#team11=SoccerTeam("equipe11",[Player("Costa",strat_key)])

team2=SoccerTeam("equipe2",[Player("Zizou",FonceurStrategy()),Player("Bravo",GardienStrategy())])
team4=SoccerTeam("equipe4",[Player("t3j1",OneOneStrategy()),[Player("Zizou",FonceurStrategy()),Player("Bravo",GardienStrategy())],Player("Muller",GardienStrategy())])
