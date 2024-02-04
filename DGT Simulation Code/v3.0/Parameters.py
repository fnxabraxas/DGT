import itertools
import os
import math
''' Simulation Parameters '''
num_experiments =10 # The number of times the experiment should be run, for calculating ensemble averages
num_agents = 1024 # The number of players involved

# Sober Game
T = 1.5  # 0=< T = <2
S = -0.5  # -1 =< S =< 0

# Drunk Game
T_prime = 0.5  # 0=< T' = <2
S_prime = 0.5  # -1 =< S' =< 0

### Rate Constants ###
kappa = 1.00 # Strength of beer
beta = 1.0

'''Pay off Matrices '''
### Pay off ### 
# Beer effects alpha level, pay off does not. 
#############################
# 			|
# 	A		|   B
#___________|____________
# 			|
# 	C		|	D
# 			|
#############################
### Sober Game ###
A_s = 1.0
B_s = S
C_s = T
D_s = 0.0

### Drunk Game ###
A_d = 1.0
B_d = S_prime
C_d = T_prime
D_d = 0.0


### Topology ###
'''The structure of the population '''
graph_type = 'None' #'None' #'Regular' #'Random' #'Lattice', 'Geometric' 'Edge_list'
mean_degree  = 8.0
f_name = 'hidden-layer-RGG.txt'
edge_p = mean_degree*(1.0/num_agents)#- 0.0005  # Probability of connection in a random graph, only useful if graph_type = 'Random'
barabasi_albert_m = 2 # Controls topology if graph_type = 'BA'
RGG_r = math.sqrt(mean_degree/(math.pi*num_agents)) #0.051725 # Radius for Random Geometric Graph
regular_d = int(mean_degree) # Number of edges in regular random graph
lattice_neighbors = mean_degree
p_out = 0.1 # Initial probability of interacting outside your group, only useful if graph_type = 'Groups'
num_groups = 2 # Number of groups in population, only useful if graph_type = 'Groups'

### Initialization ##
pregame = False  # If True, the initial alpha level of players is picked randomly, if False, alpha = 0 for all players initially


''' Output Specifications '''
output_agents = True # If True, all the data for each agent will be output every (infreq_data) iterations
output_network = False # If True, the network data will be output every (infreq_data) iterations
draw_networks = False # If True, the network will be draw using networkx and saved as a png every (infreq_data) iterations
update_freq = 10		 # The number of iterations between individual strategy update events, only one player updates strategy ever update_freq time
infreq_data = 200 # The number of iterations between large data dumps
output_time_series = False # If true, Time series data on bulk variables will be printed (average alpha, average strategy, average beers etc)

'''These controls are still buggy. '''
specify_drunk_hubs = False 
specify_cooperative_hubs = False
# These are intial alphas
ic_list1 = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
initial_conditions = []

### Generate all possible initial conditions ###
for i in range(len(ic_list1)):
    for j in range(len(ic_list1)):
        initial_conditions.append( ( ic_list1[i], ic_list1[j]) )
num_IC = len(initial_conditions)       
######################################################################################################################
# Global Variables that program will modify ##########################################################################
######################################################################################################################
Drunks = [] 
Groups = []
Group_dict = {}
pos = None

#r = max(W_s,X_s,Y_s, Z_s, W_d, X_d, Y_d, Z_d, 1.0)

if graph_type == 'BA':
	dirname = 'data/%iPlayers_%.2fkappa_%.4fbeta_BA_%im_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents, kappa,beta,  barabasi_albert_m , T, S, T_prime, S_prime)

elif graph_type == 'Random':
	dirname = 'data/%iPlayers_%.2fkappa_%.4fbeta_Random_%.4fp_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents, kappa,beta, edge_p,  T, S, T_prime, S_prime)

elif graph_type == 'Geometric':
	dirname = 'data/%iPlayers_%.2fkappa_%.4fbeta_Geometric_%.4fr_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents, kappa, beta, RGG_r,  T, S, T_prime, S_prime)

elif graph_type == 'Regular':
	dirname = 'data/%iPlayers_%.2fkappa_%.4fbeta_Regular_%id_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents, kappa, beta, regular_d,  T, S, T_prime, S_prime)

elif graph_type == 'Lattice':
	dirname = 'data/%iPlayers_%.2fkappa_%.4fbeta_Lattice_%id_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents, kappa, beta, lattice_neighbors,  T, S, T_prime, S_prime)

elif graph_type == 'None':
	dirname = 'data/%iPlayers_%.2fkappa_%.4fbeta_Well_mixed_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents,  kappa, beta,  T, S, T_prime, S_prime)
	
elif graph_type == 'Groups':
	dirname = 'data/%iPlayers_%.2fkappa_Groups_%igroups_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents, kappa,  num_groups, p_out,  T, S, T_prime, S_prime)

elif graph_type == 'Edge_list':
	dirname = 'data/%iPlayers_%.2fkappa_input_%.2fT_%.2fS_%.2fTp_%.2fSp/' %( num_agents,  kappa,   T, S, T_prime, S_prime)
	
if not os.path.exists(dirname):
            os.makedirs(dirname)
