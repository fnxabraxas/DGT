# Cole Mathis 2014
# CSSS14 Drunk GT

from numpy import*
import Parameters
###################################################################################################
class Drinker(object):
    """A Drinking agent"""
    
    def __init__(self, ID, strat):
        #print("A new agent has been born!")
        self.ID = ID

       	self.alpha = 0.0
       	self.beers = 0
       	self.payoff = 0 # Most recent pay off

        
       	self.cooperator = False # Most recent play
       	self.Net_payoff = 0.0
        self.strat = strat # probability of Offering a round (cooperation), probability of staying silent (defection)
        

