import soccersimulator, soccersimulator.settings

from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings

from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament

class App(object):
    def __init__(self,state,idteam,idplayer):
        self.state=state
        self.key=(idteam,idplayer)

    def my_position(self):
        return self.state.player_state(self.key[0],self.key[1]).position
    
    def ball_position(self):
        return self.state.ball.position
        
    def shoot(self,force):
        return SoccerAction(Vector2D(),force-self.state.my_position())

    def ball_vitesse(self):
        return self.state.ball.vitesse
    
    def go_goal(self):
        if self.key[0] == 1:
            return SoccerAction(Vector2D(settings.GAME_GOAL_HEIGHT/1.5,settings.GAME_HEIGHT/2)-self.my_position(),Vector2D(0,0))
        if self.key[0] ==2:
            return SoccerAction(Vector2D(settings.GAME_WIDTH-(settings.GAME_GOAL_HEIGHT/1.5),settings.GAME_HEIGHT/2)-self.my_position(),Vector2D(0,0))
        

#func
#ball dans quel moitie de terrain
#
class RandomStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Random")

    def compute_strategy(self, state,id_team, id_player):
        return SoccerAction(Vector2D.create_random(-1,1),Vector2D.create_random(-1,1))

 
class FonceurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Fonceur")

    def compute_strategy(self, state,id_team, id_player):
        p=state.player_state(id_team,id_player)
        if p.position.distance(state.ball.position) < (settings.BALL_RADIUS+settings.PLAYER_RADIUS):
            if id_team == 1:
                return SoccerAction(state.ball.position-p.position,Vector2D(10,0))
            if id_team == 2:
                return SoccerAction(state.ball.position-p.position,Vector2D(-10,0)) 
        return SoccerAction(state.ball.position-p.position,Vector2D())   



class GardienStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Gardien")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)

        
        if a.ball_position().x<(settings.GAME_WIDTH/2) or a.ball_position().x>(settings.GAME_WIDTH/2):  #la balle a traverse la moitie de terrain
            dep=a.ball_position()-a.my_position()            #--> bloquer le passage de la balle 
            dep.x=0
            if a.my_position().distance(a.ball_position()) < (settings.BALL_RADIUS+settings.PLAYER_RADIUS):  # Degagement ou pas
                return SoccerAction(dep,Vector2D(10,0))   
            return SoccerAction(dep,Vector2D())

        if a.my_position().distance(Vector2D(settings.GAME_GOAL_HEIGHT/1.5,settings.GAME_HEIGHT/2)) > settings.PLAYER_RADIUS: #Si le Gardien n'est pas dans ces cages
            return a.go_goal()             # --> Aller dans les cages
        #On est dans les cages
       
        return SoccerAction()
    -->
