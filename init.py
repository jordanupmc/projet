import soccersimulator, soccersimulator.settings

from soccersimulator import AbstractStrategy, Vector2D, SoccerAction, settings

from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament


class RandomStrategy(AbstractStrategy):
    def __init__(self):
        AbstractStrategy.__init__(self, "Random")

    def compute_strategy(self, state,id_team, id_player):
        return SoccerAction(Vector2D.create_random(-1,1),Vector2D.create_random(-1,1))

 
class FonceurStrategy(AbstractStrategy):
    def __init__(self):
        AbstractStrategy.__init__(self, "Fonceur")

    def compute_strategy(self, state,id_team, id_player):
        p=state.player_state(id_team,id_player)
        if p.position.distance(state.ball.position) < (settings.BALL_RADIUS+settings.PLAYER_RADIUS):
            if id_team == 1:
                return SoccerAction(state.ball.position-p.position,Vector2D(10,0))
            if id_team == 2:
                return SoccerAction(state.ball.position-p.position,Vector2D(-10,0)) 
        return SoccerAction(state.ball.position-p.position,Vector2D())   



class GardienStrategy(AbstractStrategy):
    def __init__(self):
        AbstractStrategy.__init__(self, "Gardien")

    def compute_strategy(self, state,id_team, id_player):
        if state.player_state.position.distance(Vector2D(settings.GAME_WIDTH,settings.GAME_HEIGHTS/2)) > 0:
            return  SoccerAction(Vector2D(-7,0),Vector2D(0,0))
        return SoccerAction()
    
        
team1=SoccerTeam("equipe1",[Player("t1j1",GardienStrategy())])
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
                            
