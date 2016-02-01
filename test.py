from Strat import *
            
team1=SoccerTeam("equipe1",[Player("Bravo",GardienStrategy())])
team2=SoccerTeam("equipe2",[Player("t2j1",FonceurStrategy())])
team3=SoccerTeam("equipe3",[Player("t3j1",RandomStrategy())])
match=SoccerMatch(team1,team2)
#match.play()
soccersimulator.show(match)
tournoi=SoccerTournament(1)
tournoi.add_team(team1)
tournoi.add_team(team2)
tournoi.add_team(team3)
#tournoi.play()
soccersimulator.show(tournoi)
                            
