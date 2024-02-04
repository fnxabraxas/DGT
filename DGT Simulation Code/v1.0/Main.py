# Cole Mathis 2014
# CSSS14 Drunk GT

import random
import numpy as np 
import matplotlib.pylab as plt
from time import clock
from Agents import *
from Initialize import *
from Interactions import *
from Output import *

import Parameters as Par 

##################################################################################################
def main():
    
    
    reload(Parameters)
    for exp in range(Par.num_experiments):

        start_time = clock()
        Bar_network, Par.Drunks = Initialize_alcoholics()
        game = 0
        freq_counter = 0
        infreq_counter = 0
        
        output_agent_data(exp, Par.Drunks, t = game)
        output_network(Bar_network, Par.Drunks, exp, t = game, draw = Par.draw_networks)
        
        print "Initialized..."
    	while game < Par.total_games:
            # Pick random edge to play on
            match = pick_match(Bar_network, Par.Drunks) 

    		# The game
            play_game(match, Par.Drunks)

            # Update player strategies and (maybe) output some data
            if freq_counter <= game:
                if Par.output_time_series == True: 
                    output_time_data(exp, game, Par.Drunks)
                freq_counter += Par.update_freq
                [player] = random.sample(Bar_network.nodes(),1)
                update_strat_local(player, Bar_network, Par.Drunks)

                #Bar_network = update_network(Bar_network, Drunks)

            if infreq_counter <= game:
                if Par.output_agents == True: 
                    output_agent_data(exp, Par.Drunks, t = game)
                if Par.output_network == True:
                    output_network(Bar_network, Par.Drunks, exp, t= game, draw = Par.draw_networks)
                infreq_counter += Par.infreq_data
                print game

            game +=1
            if game == int(Par.total_games/2.0):
                print "Half way there..."
            #print game
        
        output_agent_data(exp, Par.Drunks, t = game)
    run_time = clock() - start_time
    print 'Final data saved, run time: ',run_time

# End of Main function ###########################################################################



if __name__=="__main__":
    main()