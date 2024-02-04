# Cole Mathis 2014
# CSSS14 Drunk GT

import random
import numpy as np 
#import matplotlib.pylab as plt
from time import clock
from Agents import *
from Initialize import *
from Interactions import *
from Output import *

import Parameters as Par 

##################################################################################################
def main():
    reload(Parameters)
    start_time = clock()
    for exp in range(Par.num_experiments):
        reload(Parameters)
        for ic in range(Par.num_IC):
            
            if ic == 0:
                Bar_network, Par.Drunks = Initialize_alcoholics(exp, ic)
            else:
                Par.Drunks = Initialize_alcoholics(exp,ic, Bar_network = Bar_network)
            game = 0
            freq_counter = 0
            infreq_counter = 0
            
            output_agent_data_averages(exp,ic, Par.Drunks, t =0)
            #output_network(Bar_network, Par.Drunks, exp,ic, t = game, draw = Par.draw_networks)
            
            #print exp, ic
            matches = Bar_network.edges()

            for match in matches:
                # Play on all edges
            	# The game
                play_game(match, Par.Drunks)

                
                
            fermi_rule_update_synchronous(Bar_network, Par.Drunks)
            output_agent_data_averages(exp, ic, Par.Drunks, t = 1)
        run_time = clock() - start_time
    print 'Final data saved, run time: ',run_time

# End of Main function ###########################################################################



if __name__=="__main__":
    main()