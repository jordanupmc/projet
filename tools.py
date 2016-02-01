import soccersimulator, soccersimulator.settings
from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings

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
    
    def go_goal(self): #sans ballon
        if self.key[0] == 1:
            return SoccerAction(Vector2D(settings.GAME_GOAL_HEIGHT/1.5,settings.GAME_HEIGHT/2)-self.my_position(),Vector2D(0,0))
        if self.key[0] ==2:
            return SoccerAction(Vector2D(settings.GAME_WIDTH-(settings.GAME_GOAL_HEIGHT/1.5),settings.GAME_HEIGHT/2)-self.my_position(),Vector2D(0,0))
        

#func
#ball dans quel moitie de terrain
#
