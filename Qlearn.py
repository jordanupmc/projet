from Strat import *

try:
    f=open('dico.pkl','rb')
    qlearn=cPickle.load(f)
    f.close()
except IOError:
    print 'DICO VIDE'
    qlearn=None

try:
    f2=open('./genmatchs.pkl','rb')
    scenario=cPickle.load(f2)
    f2.close()
except IOError:
    scenario=None


'''
print '-------\n'
print(scenario[0][0])#scenario match 0 etat 0/2000
print '-------\n'
print(scenario[0][0][0].ball.position)
print '-------\n'
print(scenario[0][0][1]) #strat du match 0 etat 0/2000 
'''
i=0


for i in range(len(scenario)):
    qlearn=learn_q(1,0, qlearn, scenario[i],0.1,0.9)
'''
 
if team2==match.team1 or team1==match.team1 or team4==match.team1:
    x=0 # pas sur team1==0
else:
    x=1
'''
#qlearn=learn_q(0,0, qlearn, scenario[i],0.1,0.9)
print "DUMP dico.pkl"
cPickle.dump(qlearn,file('dico.pkl','wb'))
