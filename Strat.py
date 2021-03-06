import soccersimulator, soccersimulator.settings, cPickle

from soccersimulator import BaseStrategy, Vector2D, SoccerAction, settings,DecisionTreeClassifier

from soccersimulator import SoccerTeam, SoccerMatch
from soccersimulator import Player, SoccerTournament,KeyboardStrategy
from tools import *
#from Qlearn import qlearn


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
            res=gardien(a)           
            res.acceleration.norm=settings.maxPlayerAcceleration/2.2

            res.name="gardien"
            if a.key[0] ==2:
               return miroir_action(res)
            return res

        res=go_vers_ball(a)+degage_cote(a)   
        res.acceleration.norm=settings.maxPlayerAcceleration/2.2

        res.name="go_vers_ball+degage_cote"
        if a.key[0] ==2:
           return miroir_action(res)
        
        return res

class OneOneStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "OnevOne")
        self.shoot=0

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
        
        if a.key[0]==2:
            a=App(miroir(state),id_team,id_player)
            
        #return miroir_action(passe_j1(a)+go_vers_ball(a))
       
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
            self.shoot=0
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
          

class CampeurStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "Campeur")

    def compute_strategy(self, state,id_team, id_player):
        a=App(state,id_team,id_player)
        return campeur(a)   
   
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
    res= app.vers_ball()
    #res.name="go_vers_ball"
    return res

def degager(app):       
    hisg = Vector2D((2-app.key[0])*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)
    shoot=hisg-app.ball_position
    
    s=SoccerAction(app.ball_position-app.my_position, shoot)
    s.shoot.norm=4
    
    if app.key[0]==2: #miroir fail 
        s.acceleration.x=-s.acceleration.x
        s.shoot.x=-s.shoot.x
        
    if app.can_shoot() == 0:
        s.name="degager"
        return s

    return SoccerAction(Vector2D(),Vector2D())

def conduite_ball(app):
    if app.can_shoot() == 0:
        res=app.conduire_ball()
        res.name="conduite_ball"
        return res
    return SoccerAction(Vector2D(),Vector2D())


def fonceur(a):
    if a.is_ball_near_goal(3.1) == 0:#3.8
        res= go_vers_ball(a)+degager(a)
        res.name="fonceur_shoot"
        return res
    res= go_vers_ball(a)+conduite_ball(a)
    res.name="fonceur_conduite"
    return res

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
            res= SoccerAction(dep,Vector2D((3.14),4.5)) # angle a modifie
            res.name="degage_cote_haut"
            return res
        else:
            res=SoccerAction(dep,Vector2D(-(3.14),4.5))
            res.name="degage_cote_bas"
            return res
    return SoccerAction(dep,Vector2D())
     
def campeur(a):
    rayon=22
    if a.key[0]==2 and a.my_position.x >= settings.GAME_WIDTH/2.5:
        return SoccerAction(Vector2D(settings.GAME_WIDTH/2.5,settings.GAME_HEIGHT/3)-a.my_position,Vector2D())
    else:
        if a.key[0]==2:    
            a=App(miroir(a.state),a.key[0],a.key[1])
            if a.my_position.distance(a.ball_position) <= (settings.BALL_RADIUS+settings.PLAYER_RADIUS)*rayon:
                return miroir_action(fonceur(a))
            else: 
                return SoccerAction(Vector2D.create_random(-1,1),Vector2D())

        else:
            if a.my_position.x <= settings.GAME_WIDTH-settings.GAME_WIDTH/2.5:
                return SoccerAction(Vector2D(settings.GAME_WIDTH-settings.GAME_WIDTH/2.5,settings.GAME_HEIGHT/3)-a.my_position,Vector2D())
            else:
                 if a.my_position.distance(a.ball_position) <= (settings.BALL_RADIUS+settings.PLAYER_RADIUS)*rayon:
                     return fonceur(a)
                 else: 
                     return SoccerAction(Vector2D.create_random(-1,1),Vector2D())


def passe_j1(a):
    if a.can_shoot()==1:
        return SoccerAction()
    friend=a.position_j1()
    s=SoccerAction(Vector2D(),friend-a.ball_position)

    s.shoot.norm=2.5
    """
    if a.key[0]==2: #miroir fail 
        s.acceleration.x=-s.acceleration.x
        s.shoot.x=-s.shoot.x
    """
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

    l = int(position.y / pas_y) #ligne
    c = int(position.x / pas_x) #colonne
    
    return c,l
    
def q_etat(state, id_team, id_player): #discretisation
    a=App(state,id_team,id_player)
    grille=7
    
    x_player,y_player=position_to_grille(grille,a.my_position)
    x_ball,y_ball=position_to_grille(grille,a.ball_position)
    x_mygoal,y_mygoal =position_to_grille(grille,Vector2D((id_team-1)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))
    x_enemygoal,y_enemygoal = position_to_grille(grille,Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))
             
    return ( (x_player-x_ball, y_player-y_ball) , (x_enemygoal-x_ball,y_enemygoal-y_ball), (x_mygoal-x_ball,y_mygoal-y_ball) )


##########ID DES CASES DU TABLEAU Q_ETAT#########
D_J_B=0   #distance joueur ball 
D_Genemy_B=1   #distance goal enemy,ball 
D_MyG_B=2 #distance mon goal, ball



def q_reward(s,a=None):
    r=0
    if s[D_J_B]== (0,0): #and a!= None and a.name=="conduite_ball": #distance joueur ball
        r+=5
    else:
        r+=-1

    if s[D_MyG_B][0] == (0): #l'adversaire a mis un but
        r+= -100

    if s[D_Genemy_B][0] == (0): #je viens de marquer
        r+=100


    return r
# q(s,a) : dict : s -> (dict : a -> reel)
#q[s][a]+
    #scenario : [(etat,action),(etat,None)]

    #alpha critere de convergence
    
def learn_q(id_team=1, id_player=0,q=None,scenario=None,alpha=0.1,gamma = 0.9):
    if q is None:
        q = dict()
    R = q_reward(q_etat(scenario[-1][0],id_team,id_player)) #On commence avec le dernier etat
    for (etat,action) in  scenario[-2::-1]:
        state = q_etat(etat,id_team, id_player)
        if state is not q:
            q[state] = dict()
        if action is not q[state]:
            q[state][action] = 0. # ou  random
        q[state][action] = q[state][action]+alpha*(R-q[state][action])
        R = gamma*R+q_reward(state,action)
        
    return q

def ia_q(q,s):
    actions = q[s]
    return sorted(actions.items(),key = lambda x:x[1],reverse = True)[0] #sort l'action avec la plus grande recompense

class QStrategy(BaseStrategy):
    def __init__(self):
        BaseStrategy.__init__(self, "QStrategy")
        try:
            f=open('dico.pkl','rb')
            self.qlearn=cPickle.load(f)
            f.close()
        except IOError:
            self.qlearn=None

    def compute_strategy(self, state,id_team, id_player):
        print ia_q(self.qlearn,q_etat(state,id_team,id_player))[0][0]
        return SoccerAction()
        
  #MIROR#########################

def miroir_point(p):
    return Vector2D(settings.GAME_WIDTH-p.x,p.y)
    
def miroir_v(v):
    return Vector2D(-v.x,v.y)

def miroir_action(action):
    #action.name=action.name
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
