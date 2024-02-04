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
def Initialize_alcoholics(exp, ic, Bar_network = None):
	from Parameters import initial_conditions
	if ic == 0:
		print "New Network Made"
		### Initialize Network 
		if Par.graph_type == 'Random': # Random Graph
			Bar_network = nx.gnp_random_graph(Par.num_agents, Par.edge_p)
			if not nx.is_connected(Bar_network):
				print "Graph not completely connected"
			# For details see: https://networkx.github.io/documentation/latest/reference/generated/networkx.generators.random_graphs.gnp_random_graph.html#networkx.generators.random_graphs.gnp_random_graph
		elif Par.graph_type == 'BA': # Heterogenous Network
			Bar_network = nx.barabasi_albert_graph(Par.num_agents, Par.barabasi_albert_m)
			# For details see: https://networkx.github.io/documentation/latest/reference/generated/networkx.generators.random_graphs.barabasi_albert_graph.html#networkx.generators.random_graphs.barabasi_albert_graph
		elif Par.graph_type == 'Geometric':
			Bar_network = nx.random_geometric_graph(Par.num_agents, Par.RGG_r)
		elif Par.graph_type == 'Regular':
			Bar_network =nx.random_regular_graph(int(Par.regular_d), Par.num_agents)
		elif Par.graph_type == 'Lattice':
			Bar_network = initialize_lattice(Par.num_agents)
		elif Par.graph_type == 'None': # Well mixed population
			Bar_network = nx.complete_graph(Par.num_agents)
			# For details see: https://networkx.github.io/documentation/latest/reference/generated/networkx.generators.classic.complete_graph.html#networkx.generators.classic.complete_graph
		elif Par.graph_type == 'Groups':
			Bar_network = nx.complete_graph(Par.num_agents)
			Par.Groups, Par.Group_dict = Initialize_Groups(Par.num_agents, Par.num_groups)
		elif Par.graph_type == 'Edge_list':
			Bar_network= nx.read_edgelist(Par.f_name, nodetype = int)
			Par.num_agents = len(Bar_network.nodes())
	Drunks = []
	
	if Par.specify_drunk_hubs == True or Par.specify_cooperative_hubs == True:
		#degree_sequence=sorted([(n,d) for n,d in Bar_network.degree()], reverse=True) # degree sequence
		degree_seq = []		
		for n in Bar_network.nodes():
			d  = Bar_network.degree(n)
			degree_seq.append( (n,d) )

		degree_sequence = sorted(degree_seq,key=lambda tup: tup[1], reverse = True)
		player_IDs, degrees = zip(*degree_sequence)

		Drunks = [None,]*len(player_IDs)
		mean_x = initial_conditions[ic][0]
		mean_alpha = initial_conditions[ic][1]

		if Par.specify_drunk_hubs == True:
			total_Drunk = mean_alpha*len(player_IDs)
			num_Drunk = 0
			for ID in player_IDs:
				dice_roll = random.random()
				if dice_roll < mean_x:
					A_prob = 0.95
				else:
					A_prob = 0.05
				B_prob = 1 - A_prob
				strat = [A_prob, B_prob]
				
				Drunks[ID] = Drinker(ID, strat)
				if num_Drunk < total_Drunk:
					Drunks[ID].alpha = 1.0
					num_Drunk +=1 #random.random()
				else:
					Drunks[ID].alpha = 0.0

		if Par.specify_cooperative_hubs == True:
			total_cooperative = mean_x*len(player_IDs)
			num_cooperate = 0
			for ID in player_IDs:
				if num_cooperate < total_cooperative:
					A_prob = 0.95
					num_cooperate += 1
				else:
					A_prob = 0.05
				B_prob = 1 - A_prob
				strat = [A_prob, B_prob]
				
				Drunks[ID] = Drinker(ID, strat)
				Drunks[ID].alpha = mean_alpha

	else: # Randomize agents
		mean_x = initial_conditions[ic][0]
		mean_alpha = initial_conditions[ic][1]

		for ID in range(Par.num_agents):
			dice_roll = random.random()
			if dice_roll < mean_x:
				A_prob = 0.95
			else:
				A_prob = 0.05
			B_prob = 1 - A_prob
			strat = [A_prob, B_prob]
			
			Drunks.append(Drinker(ID, strat))
			Drunks[ID].alpha = mean_alpha #random.random()
			
	if ic == 0:
		return Bar_network, Drunks
	else:
		return Drunks
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

def initialize_lattice(num_agents):
	#import matplotlib.pylab as plt
	length = int(np.sqrt(num_agents))

	G=nx.grid_2d_graph(length,length, periodic =True)
	# print G.nodes()
	# raw_input("Enter")
	for node in G.nodes():
		(i,j) = node
		if i == 0:
			
			if j == 0:
				G.add_edge( (i,j), (i + 1, j+1) )
				G.add_edge( (i,j), (i + 1, (length-1) ))
				G.add_edge( (i,j), ((length-1), j+1) )
				G.add_edge( (i,j), ((length-1), (length-1)) )


			elif j == (length-1):
				G.add_edge( (i,j), (i + 1, 0) )
				G.add_edge( (i,j), (i + 1, j-1 ))
				G.add_edge( (i,j), (i +(length-1), 0) )
				G.add_edge( (i,j), (i +(length-1), j-1) )

			else:
				G.add_edge( (i,j), (i + 1, j+1) )
				G.add_edge( (i,j), (i + 1, j-1) )
				G.add_edge( (i,j), ((length-1), j+1) )
				G.add_edge( (i,j), ((length-1), j-1) )

		elif i == (length-1):

			if j == 0:
				G.add_edge( (i,j), (0, j+1) )
				G.add_edge( (i,j), (0, (length -1) ) )
				G.add_edge( (i,j), (i-1, j+1) )
				G.add_edge( (i,j), (i-1, (length-1) ) )


			elif j == (length-1):
				G.add_edge( (i,j), (0, 0 ) )
				G.add_edge( (i,j), (0, j-1 ) )
				G.add_edge( (i,j), (i-1, 0) )
				G.add_edge( (i,j), (i-1, j-1) )

			else:
				G.add_edge( (i,j), (0, j+1 ) )
				G.add_edge( (i,j), (0, j-1 ) )
				G.add_edge( (i,j), (i-1, j+1) )
				G.add_edge( (i,j), (i-1, j-1) )

		else:

			if j == 0:
				G.add_edge( (i,j), (i+1, j+1 ) )
				G.add_edge( (i,j), (i+1, (length-1) ) )
				G.add_edge( (i,j), (i-1, j+1) )
				G.add_edge( (i,j), (i-1, (length-1)) )

			elif j == (length-1):
				G.add_edge( (i,j), (i+1, 0 ) )
				G.add_edge( (i,j), (i+1, j-1 ) )
				G.add_edge( (i,j), (i-1, 0 ) )
				G.add_edge( (i,j), (i-1, j-1) )

			else:
				G.add_edge( (i,j), (i+1, j+1 ) )
				G.add_edge( (i,j), (i+1, j-1 ) )
				G.add_edge( (i,j), (i-1, j+1) )
				G.add_edge( (i,j), (i-1, j-1) )
	G = nx.convert_node_labels_to_integers(G)
	return G



	# degrees = nx.degree(G).values()
	# print np.mean(degrees)
	# # for node in G.nodes():
	# # 	print node, len(G.edges(node))
	# # 	raw_input('Enter')
	# pos = dict( (n, n) for n in G.nodes() )
	# labels = dict( ((i, j), i * 10 + j) for i, j in G.nodes() )
	# nx.draw_networkx(G, pos=pos, labels=labels)

	# plt.axis('off')
	# plt.show()

	