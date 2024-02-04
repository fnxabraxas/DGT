# Cole Mathis 2014
# CSSS14 Drunk GT

import random
import numpy as np 
import math
import networkx as nx

import Parameters as Par
from Agents import Drinker
#from Interactions import payoff_matrix
###############################################################################################################
def Initialize_alcoholics():

	### Initialize Network 
	if Par.graph_type == 'Random': # Random Graph
		Bar_network = nx.gnp_random_graph(Par.num_agents, Par.edge_p)
		# For details see: https://networkx.github.io/documentation/latest/reference/generated/networkx.generators.random_graphs.gnp_random_graph.html#networkx.generators.random_graphs.gnp_random_graph

	elif Par.graph_type == 'BA': # Heterogenous Network
		
		Bar_network = nx.barabasi_albert_graph(Par.num_agents, Par.barabasi_albert_m)
		# For details see: https://networkx.github.io/documentation/latest/reference/generated/networkx.generators.random_graphs.barabasi_albert_graph.html#networkx.generators.random_graphs.barabasi_albert_graph
	
	elif Par.graph_type == 'None': # Well mixed population
		Bar_network = nx.complete_graph(Par.num_agents)
		# For details see: https://networkx.github.io/documentation/latest/reference/generated/networkx.generators.classic.complete_graph.html#networkx.generators.classic.complete_graph
	elif Par.graph_type == 'Groups':
		Bar_network = nx.complete_graph(Par.num_agents)
		Par.Groups, Par.Group_dict = Initialize_Groups(Par.num_agents, Par.num_groups)
	Drunks = []
	
	if Par.specify_initial_conditions == True:
		mean_x = Par.IC_x # Initial degree of cooperation
		mean_alpha = Par.IC_alpha # Initial alpha level
		for ID in range(Par.num_agents):
			A_prob = np.random.normal(mean_x, Par.sigma_x)
			while  A_prob < 0.0 or A_prob > 1.0:
				A_prob = np.random.normal(mean_x, Par.sigma_x)
			B_prob = 1 - A_prob

			strat = [A_prob, B_prob]
			Drunks.append(Drinker(ID, strat))

			Drunks[ID].alpha = np.random.normal(mean_alpha, Par.sigma_alpha)
			while Drunk[ID].alpha < 0.0 or Drunk.alpha > 1.0:
				Drunk[ID].alpha = np.random.normal(mean_alpha, Par.sigma_alpha)

	else: # Randomize agents
		for ID in range(Par.num_agents):
			A_prob = random.random()
			B_prob = 1 - A_prob
			strat = [A_prob, B_prob]

			Drunks.append(Drinker(ID, strat))
			if Par.pregame == False:
				Drunks[ID].alpha = 0.0 #random.random()
			else:
				Drunks[ID].alpha = random.random()
			
	return Bar_network, Drunks
########################################################################################################################
def update_network(current_net, Drunks):
	# pick an edge
	[players] = random.sample(current_net.edges(),1)


	return new_net


########################################################################################################################		
def Initialize_Groups(num_agents, num_groups):
	group_size = int(float(num_agents)/float(num_groups))
	agent_list = range(0, num_agents)
	groups = [agent_list[i:i+group_size] for i in xrange(0, len(agent_list), group_size)]

	group_dict = {}
	for i in range(len(groups)):
		for agent in groups[i]:
			group_dict[agent] = i
	return groups, group_dict
	