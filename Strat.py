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
        return fonceur(a)
 
#TODO MIRROR 
class GardienStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Gardien")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
        if a.is_ball_near_goal(4.5) ==1:
            return gardien(a)
        return go_vers_ball(a)+degager(a)
       
#################

def go_vers_ball(app):
    return app.vers_ball()

def degager(app):
    if app.can_shoot() == 0:
        if app.key[0]==2:
            return SoccerAction(Vector2D(),Vector2D(-10,0)) 
        return SoccerAction(Vector2D(),Vector2D(10,0)) 
    return SoccerAction(Vector2D(),Vector2D())

def conduite_ball(app):
    if app.can_shoot() == 0:
        return app.conduire_ball()
    return SoccerAction(Vector2D(),Vector2D())


def fonceur(a):
    if a.is_ball_near_goal(5) == 0:
        return go_vers_ball(a)+degager(a)
    return go_vers_ball(a)+conduite_ball(a)


def gardien(a):
    if a.is_out_goal() == 0:  #Si il etait dans les cages et qu'il en est sortit
        return a.go_goal()+degage_cote(a)
    if a.is_ball_in_my_camp() == 0: #balle dans ma moitie de terain
        return degage_cote(a)
    if a.is_in_goal() == 0: #initilisation 
        return a.go_goal()

    return SoccerAction()
    

def degage_cote(a):
    dep=a.ball_position-a.my_position            #--> bloquer le passage de la balle 
    dep.x=0
    if a.can_shoot() == 0:  # Shoot ou pas
        if a.ball_position.y >= settings.GAME_HEIGHT/2: 
            return SoccerAction(dep,Vector2D(10,-1))
        else:
            return SoccerAction(dep,Vector2D(10,1)) 
    return SoccerAction(dep,Vector2D())
    
