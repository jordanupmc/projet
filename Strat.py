import soccersimulator, soccersimulator.settings

from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings

from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament
from tools import *

class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")

    def compute_strategy(self, state,id_team, id_player):
        return SoccerAction(Vector2D.create_random(-1,1),Vector2D.create_random(-1,1))

 
class FonceurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Fonceur")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
        p=state.player_state(id_team,id_player)
        if p.position.distance(state.ball.position) < (settings.BALL_RADIUS+settings.PLAYER_RADIUS): #Possibilite de tir
            if id_team == 1:
                if a.ball_position().x > (settings.GAME_WIDTH)-settings.GAME_WIDTH/4 and a.ball_position().y < (settings.GAME_WIDTH)-settings.GAME_WIDTH/4 and a.ball_position().y > settings.GAME_WIDTH/4: #Tirer fort si dans 1/4 du terrain
                    return SoccerAction(state.ball.position-p.position,Vector2D(10,0))
                return SoccerAction(state.ball.position-p.position,Vector2D(1.2,0))  #Conduite de balle sinon
            if id_team == 2:
                if a.ball_position().x < settings.GAME_WIDTH/4 and a.ball_position().y < (settings.GAME_WIDTH)-settings.GAME_WIDTH/4 and a.ball_position().y > settings.GAME_WIDTH/4:
                    return SoccerAction(state.ball.position-p.position,Vector2D(-10,0)) 
                return SoccerAction(state.ball.position-p.position,Vector2D(-1.2,0)) 
        return SoccerAction(state.ball.position-p.position,Vector2D())   



class GardienStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Gardien")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)

        #Limite des cages
        if a.my_position().y >= (settings.GAME_HEIGHT/2)+settings.GAME_GOAL_HEIGHT/2 and not a.my_position().distance(a.ball_position()) < (settings.BALL_RADIUS+settings.PLAYER_RADIUS):
            return a.go_goal()
        if a.my_position().y <= (settings.GAME_HEIGHT/2)-settings.GAME_GOAL_HEIGHT/2 and not  a.my_position().distance(a.ball_position()) < (settings.BALL_RADIUS+settings.PLAYER_RADIUS):
            return a.go_goal()

        if a.ball_position().x<(settings.GAME_WIDTH/2) or a.ball_position().x>(settings.GAME_WIDTH/2):  #la balle a traverse la moitie de terrain
            dep=a.ball_position()-a.my_position()            #--> bloquer le passage de la balle 
            dep.x=0
            if a.my_position().distance(a.ball_position()) < (settings.BALL_RADIUS+settings.PLAYER_RADIUS):  # Shoot ou pas
                if a.ball_position().y >= settings.GAME_HEIGHT/2: 
                    return SoccerAction(dep,Vector2D(10,-1))
                else:
                    return SoccerAction(dep,Vector2D(10,1)) 
            return SoccerAction(dep,Vector2D())

        if a.my_position().distance(Vector2D(settings.GAME_GOAL_HEIGHT/1.5,settings.GAME_HEIGHT/2)) > settings.PLAYER_RADIUS: #Si le Gardien n'est pas dans ces cages
            return a.go_goal()             # --> Aller dans les cages
        #On est dans les cages
       
        return SoccerAction()
