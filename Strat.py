import soccersimulator, soccersimulator.settings, cPickle

from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings,DecisionTreeClassifier

from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament,KeyboardStrategy
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
        
        if a.key[0]==2:
            a=App(miroir(state),id_team,id_player)
            return miroir_action(fonceur(a))
        return fonceur(a)
 
 
class GardienStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Gardien")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
            
        if a.key[0]==2:
            a=App(miroir(state),id_team,id_player)
        
        if a.near_ball(20) == 1 or a.is_out_goal()==0: #nearball(20)
            if a.key[0] ==2:
               return miroir_action(gardien(a))
            return gardien(a)
        
        if a.key[0] ==2:
           return miroir_action(go_vers_ball(a))+miroir_action(degager(a))
        
        return go_vers_ball(a)+degage_cote(a)

class OneOneStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "OnevOne")
        self.shoot=0

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
        q_etat(state,id_team,id_player)
        
        if a.key[0]==2:
            a=App(miroir(state),id_team,id_player)
       # return passe_j1(a)+go_vers_ball(a)
        if a.ball_vitesse == Vector2D() and a.ball_position.x==settings.GAME_WIDTH/2 and a.ball_position.y==settings.GAME_HEIGHT/2: #engagement on reduit l'acceleration du joueur 
            s=go_vers_ball(a)+degage_cote(a)
            s.acceleration.norm=settings.maxPlayerAcceleration/2.
            s.shoot.norm=1.6 
            self.shoot=0
            if a.key[0]==2: #miroir fail 
                s.acceleration.x=-s.acceleration.x
                s.shoot.x=-s.shoot.x
        
            return s
      
        if self.shoot==1: #j'ai shooter en etant gardien donc je fonce     
            if a.key[0]==2:
                return miroir_action(fonceur(a))
            return fonceur(a)

        if a.switch_to_gardien() == 0 and a.can_shoot==1: #on passe gardien  #and can_shoot==1?
            
            if a.near_ball(20) == 1 or a.is_out_goal()==0:
                g=gardien(a)
                if g.shoot.norm != 0:
                    self.shoot=1
                else:
                    self.shoot=0
                if a.key[0] == 2:
                    return miroir_action(g)
                return g
        
            if a.key[0] ==2:
                return miroir_action(go_vers_ball(a))+miroir_action(degager(a))
        
            return go_vers_ball(a)+degage_cote(a)
        else:             #FONCEUR
            if a.key[0]==2:
                return miroir_action(fonceur(a))
            return fonceur(a)
            

class DTreeStrategy(BaseStrategy):
    def __init__(self,tree,dic,gen_feat):
        BaseStrategy.__init__(self,"Tree Strategy")
        self.dic = dic
        self.tree = tree
        self.gen_feat= gen_feat
    def compute_strategy(self, state, id_team, id_player):
        
        #label = self.tree.predict(self.gen_feat(state,id_team,id_player))[0]
        features=self.gen_feat(state,id_team,id_player)
        #print features
        label=self.tree.predict(features)[0]
        if label not in self.dic:
            print("Erreur : strategie %s non trouve" %(label,))
            return SoccerAction()
        return self.dic[label].compute_strategy(state,id_team,id_player)
    
def affiche_arbre(tree):
    long = 10
    sep1="|"+"-"*(long-1)
    sepl="|"+" "*(long-1)
    sepr=" "*long
    def aux(node,sep):
        if tree.tree_.children_left[node]<0:
            ls ="(%s)" % (", ".join( "%s: %d" %(tree.classes_[i],int(x)) for i,x in enumerate(tree.tree_.value[node].flat)))
            return sep+sep1+"%s\n" % (ls,)
        return (sep+sep1+"X%d<=%0.2f\n"+"%s"+sep+sep1+"X%d>%0.2f\n"+"%s" )% \
                    (tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_left[node],sep+sepl),
                    tree.tree_.feature[node],tree.tree_.threshold[node],aux(tree.tree_.children_right[node],sep+sepr))
    return aux(0,"")

#################

def go_vers_ball(app):
    return app.vers_ball()

def degager(app):       
    hisg = Vector2D((2-app.key[0])*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
    shoot=hisg-app.ball_position
    
    s=SoccerAction(app.ball_position-app.my_position, shoot)
    s.shoot.norm=4
    
    if app.key[0]==2: #miroir fail 
        s.acceleration.x=-s.acceleration.x
        s.shoot.x=-s.shoot.x
        
    if app.can_shoot() == 0:
        return s

#return SoccerAction(Vector2D(),Vector2D(5,0)) 
    return SoccerAction(Vector2D(),Vector2D())

def conduite_ball(app):
    if app.can_shoot() == 0:
        return app.conduire_ball()
    return SoccerAction(Vector2D(),Vector2D())


def fonceur(a):
    if a.is_ball_near_goal(3.1) == 0:#3.8
        return go_vers_ball(a)+degager(a)
    return go_vers_ball(a)+conduite_ball(a)


def gardien(a):
    if a.is_out_goal() == 0:  #Si il etait dans les cages et qu'il en est sortit
        return a.go_goal()+degage_cote(a)
    if a.is_ball_in_my_camp() == 0: #balle dans ma moitie de terain
        return degage_cote(a)
    if a.is_in_goal() == 0: #initialisation 
        return a.go_goal()
    return SoccerAction()
    

def degage_cote(a):
    dep=a.ball_position-a.my_position            #--> bloquer le passage de la balle 
    dep.x=0
    
    if a.can_shoot() == 0:  # Shoot ou pas        
        if a.my_position.y >= settings.GAME_HEIGHT/2: 
            return SoccerAction(dep,Vector2D((3.14),4.5)) # angle a modifie
        else:
            return SoccerAction(dep,Vector2D(-(3.14),4.5))
    return SoccerAction(dep,Vector2D())

def passe_j1(a):
    if a.can_shoot()==1:
        return SoccerAction()
    friend=a.position_j1()
    s=SoccerAction(Vector2D(),friend-a.ball_position)
    s.shoot.norm=2.8
    
    if a.key[0]==2: #miroir fail 
        s.acceleration.x=-s.acceleration.x
        s.shoot.x=-s.shoot.x
    return s
        

###Tree#########

def gen_features(state, id_team, id_player):
    a=App(state,id_team,id_player)
    
    bpos = state.ball.position
    mpos = state.player_state(id_team,id_player).position
    myg = Vector2D((id_team-1)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
    hisg = Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
    
#distance par rapport aux bord

#distance du coequipier le plus proche

#distance de l'adversaire le plus proche
    enemy_pos=a.enemy_close_position()

#score actuel ?
#nb de joueurs ?

    return [bpos.distance(mpos),bpos.distance(myg),bpos.distance(hisg),enemy_pos.distance(bpos)]


def build_apprentissage(fn,generator):
    ex_raw = KeyboardStrategy.read(fn)
    exemples = []
    labels = []
    for x in ex_raw:
        exemples.append(generator(x[1],x[0][0],x[0][1]))
        labels.append(x[0][2])
    return exemples,labels



def apprendre_arbre(train,labels,depth=5,min_samples_leaf=2,min_samples_split=2):
    tree= DecisionTreeClassifier(max_depth=depth,min_samples_leaf=min_samples_leaf,min_samples_split=min_samples_split)
    tree.fit(train,labels)
    return tree
    
#######################Q-LEARNING##################

def position_to_grille(grille,position):
    pas_x = settings.GAME_WIDTH / grille
    pas_y = settings.GAME_HEIGHT / grille

    l = position.y / pas_y #ligne
    c = position.x / pas_x #colonne
    return c,l
    
def q_etat(state, id_team, id_player):
    a=App(state,id_team,id_player)
    grille=7
    
    x_player,y_player=position_to_grille(grille,a.my_position)
    x_ball,y_ball=position_to_grille(grille,a.ball_position)
    x_mygoal,y_mygoal =position_to_grille(grille,Vector2D((id_team-1)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))
    x_enemygoal,y_enemygoal = position_to_grille(grille,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))
    
                           #distance joueur ball           distance goal enemy,ball            distance mon goal, ball
    return [ (x_player-x_ball, y_player-y_ball) , (x_enemygoal-x_ball,y_enemygoal-y_ball), (x_mygoal-x_ball,y_mygoal-y_ball) ]

def q_action(a):
    #if a.idteam==2:
    #     return [ miroir_action(pass_j1(a)), miroir_action(conduite_ball(a)) ]
    return [ pass_j1(a), fonceur(a), gardien(a)]

def q_reward(a):
    #exemple
    #si j'ai la balle return 1
    #marque un but 100
    #perte de balle -5
    
    return

def q_value(state,action):
    
  #MIROR#########################

def miroir_point(p):
    return Vector2D(settings.GAME_WIDTH-p.x,p.y)
    
def miroir_v(v):
    return Vector2D(-v.x,v.y)

def miroir_action(action):
    action.acceleration=miroir_v(action.acceleration)
    action.shoot=miroir_v(action.shoot)
    return action

def miroir(state):
    state.ball.position=miroir_point(state.ball.position)
    state.ball.vitesse=miroir_v(state.ball.vitesse)
    for(idteam,idplayer) in state.players:
        state.player_state(idteam,idplayer).position=miroir_point(state.player_state(idteam,idplayer).position)
        state.player_state(idteam,idplayer).vitesse=miroir_v(state.player_state(idteam,idplayer).vitesse)        
    return state

    ###########################################
