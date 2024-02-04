
import os

# Simulation Parameters
num_experiments =1 # The number of times the experiment should be run, for calculating ensemble averages
num_agents = 200 # The number of players involved
total_games = 10000 # The number of iterations

# Output Specifications
output_agents = True # If True, all the data for each agent will be output every (infreq_data) iterations
output_network = False # If True, the network data will be output every (infreq_data) iterations
draw_networks = False # If True, the network will be draw using networkx and saved as a png every (infreq_data) iterations
update_freq = 5		 # The number of iterations between individual strategy update events, only one player updates strategy ever update_freq time
infreq_data = 100 # The number of iterations between large data dumps
output_time_series = False # If true, Time series data on bulk variables will be printed (average alpha, average strategy, average beers etc)


'''Pay off Matrices '''
### (Pay off, Beer) ### 
# Beer effects alpha level, pay off does not. 
#############################
# 			|
# 	(A,W)	|   (B,X)
#___________|____________
# 			|
# 	(C,Y)	|	(D,Z)
# 			|
#############################
### Sober Game ###
(A_s, W_s) = (0.0,2.0)
(B_s, X_s) = (-1.0,1.0)
(C_s, Y_s) = (1.0,1.0)
(D_s, Z_s) = (0.0,0.0)

### Drunk Game ###
(A_d, W_d) = (2.0,2.0)
(B_d, X_d) = (1.0,1.0)
(C_d, Y_d) = (1.0,1.0)
(D_d, Z_d) = (0.0,0.0)


### Rate Constants ###
kappa = 1.00 # Strength of beer
d = 0.0500   # Metabolic rate of players
beta = 0.1

### Topology ###
'''The structure of the population '''
graph_type = 'None' #'Random' #, 'BA'
edge_p = 0.1 # Probability of connection in a random graph, only useful if graph_type = 'Random'
barabasi_albert_m = 1 # Controls topology if graph_type = 'BA'
p_out = 0.1 # Initial probability of interacting outside your group, only useful if graph_type = 'Groups'
num_groups = 2 # Number of groups in population, only useful if graph_type = 'Groups'

### Initialization ##
pregame = False  # If True, the initial alpha level of players is picked randomly, if False, alpha = 0 for all players initially

'''These controls are still buggy. '''
specify_initial_conditions = False #If True, the user can specify initial condtions, if not, then IC are random
IC_x = 0.5
IC_alpha = 0.5

sigma_alpha = 0.1
sigma_x  = 0.1

######################################################################################################################
# Global Variables that program will modify ##########################################################################
######################################################################################################################
Drunks = [] 
Groups = []
Group_dict = {}
pos = None

r = max(W_s,X_s,Y_s, Z_s, W_d, X_d, Y_d, Z_d, 1.0)

if graph_type == 'BA':
	dirname = 'data/%iPlayers_%iGames_%.2fkappa_%.2fd_BA_%im_%.1fAs_%.1fBs_%.1fCs_%.1fDs_%.1fAd_%.1fBd_%.1fCd_%.1fDd/' %( num_agents, total_games, kappa, d, barabasi_albert_m , A_s, B_s, C_s, D_s, A_d, B_d, C_d, D_d)

elif graph_type == 'Random':
	dirname = 'data/%iPlayers_%iGames_%.2fkappa_%.2fd_Random_%.3fp_%.1fAs_%.1fBs_%.1fCs_%.1fDs_%.1fAd_%.1fBd_%.1fCd_%.1fDd/' %( num_agents, total_games, kappa, d, edge_p,  A_s, B_s, C_s, D_s, A_d, B_d, C_d, D_d)

elif graph_type == 'None':
	dirname = 'data/%iPlayers_%iGames_%.2fkappa_%.2fd_Well_mixed_%.1fAs_%.1fBs_%.1fCs_%.1fDs_%.1fAd_%.1fBd_%.1fCd_%.1fDd/' %( num_agents, total_games, kappa, d,  A_s, B_s, C_s, D_s, A_d, B_d, C_d, D_d)
	
elif graph_type == 'Groups':
	dirname = 'data/%iPlayers_%iGames_%.2fkappa_%.2fd_Groups_%igroups_%.3fpout_%.1fAs_%.1fBs_%.1fCs_%.1fDs_%.1fAd_%.1fBd_%.1fCd_%.1fDd/' %( num_agents, total_games, kappa, d, num_groups, p_out,  A_s, B_s, C_s, D_s, A_d, B_d, C_d, D_d)
	
if not os.path.exists(dirname):
            os.makedirs(dirname)