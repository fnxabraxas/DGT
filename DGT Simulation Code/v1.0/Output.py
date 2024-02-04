# Cole Mathis 2014
# CSSS14 Drunk GT
import random
import numpy as np 
import csv
import Parameters as Par 
import pandas as pd
########################################################################################################
def output_time_data(exp, t, Drunks):

	mean_alpha(exp, t, Drunks)
	alpha_cooperators(exp,t, Drunks)
	mean_beers(exp, t, Drunks)
	total_beers(exp, t, Drunks)
	instant_cooperation(exp, t, Drunks)
	mean_payoff(exp, t, Drunks)
	total_payoff(exp,t, Drunks)
	mean_cooperation(exp, t, Drunks)
	#record_interactions(exp, t, matches)
########################################################################################################
def output_agent_data(exp, Drunks, t = 0):
	alphas = []
	cooperators = []
	strategies = []
	payoffs = []
	beers =[]
	cooperator_alphas = []
	for Drunk in Drunks:
		alphas.append(Drunk.alpha)
		beers.append(Drunk.beers)
		payoffs.append(Drunk.Net_payoff)
		strategies.append(Drunk.strat[0])
		if Drunk.cooperator == True:
			cooperator_alphas.append(Drunk.alpha)
		else:
			cooperator_alphas.append('NA')

	filename = Par.dirname + "%i_agent_data_%i.csv" % (exp, t)
	columns = ['alphas', 'strategies', 'payoffs', 'beers', 'cooperator_alphas' ]
	df = pd.DataFrame([alphas, strategies, payoffs, beers, cooperator_alphas], index = columns)

	df = df.T
	df.to_csv(filename)
########################################################################################################
def output_initial_data(exp, Drunks):
	alphas = []
	cooperators = []
	strategies = []
	payoffs = []
	beers =[]
	cooperator_alphas = []
	for Drunk in Drunks:
		alphas.append(Drunk.alpha)
		beers.append(Drunk.beers)
		payoffs.append(Drunk.Net_payoff)
		strategies.append(Drunk.strat[0])
		if Drunk.cooperator == True:
			cooperator_alphas.append(Drunk.alpha)
		else:
			cooperator_alphas.append('NA')

	filename = Par.dirname + "%i_initial_data.csv" %exp
	columns = ['alphas', 'strategies', 'payoffs', 'beers', 'cooperator_alphas' ]
	df = pd.DataFrame([alphas, strategies, payoffs, beers, cooperator_alphas], index = columns)

	df = df.T
	df.to_csv(filename)
#########################################################################################################
def mean_alpha(exp,t, Drunks):
	alphas = []
	for Drunk in Drunks:
		alphas.append(Drunk.alpha)
	mean_alpha = np.mean(alphas)
	std_dev_alpha = np.std(alphas)

	filename=Par.dirname+('%i_mean_alpha.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(mean_alpha)+ '	'+str(std_dev_alpha)
	file.write(s)
	file.write('\n')
	file.close()
#########################################################################################################
def alpha_cooperators(exp,t, Drunks):
	alphas = []
	for Drunk in Drunks:
		if Drunk.cooperator == True:
			alphas.append(Drunk.alpha)

	mean_alpha = np.mean(alphas)
	std_dev_alpha = np.std(alphas)

	filename=Par.dirname+('%i_alpha_c.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(mean_alpha)+ '	'+str(std_dev_alpha)
	file.write(s)
	file.write('\n')
	file.close()
#########################################################################################################
def mean_beers(exp, t, Drunks):
	beers = []
	for Drunk in Drunks:
		beers.append(Drunk.beers)
	mean_beers = np.mean(beers)
	std_dev_beers = np.std(beers)

	filename=Par.dirname+('%i_mean_beers.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(mean_beers)+ '	'+str(std_dev_beers)
	file.write(s)
	file.write('\n')
	file.close()
#########################################################################################################
def total_beers(exp, t, Drunks):
	beers = []
	for Drunk in Drunks:
		beers.append(Drunk.beers)
	all_beers = np.sum(beers)

	filename=Par.dirname+('%itotal_beers.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(all_beers)
	file.write(s)
	file.write('\n')
	file.close()
#########################################################################################################
def mean_payoff(exp, t, Drunks):
	payoffs = []
	for Drunk in Drunks:
		payoffs.append(Drunk.Net_payoff)
	mean_payoffs = np.mean(payoffs)
	std_dev_payoffs = np.std(payoffs)

	filename=Par.dirname+('%imean_payoffs.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(mean_payoffs)+ '	'+str(std_dev_payoffs)
	file.write(s)
	file.write('\n')
	file.close()
#########################################################################################################
def total_payoff(exp, t, Drunks):
	payoffs = []
	for Drunk in Drunks:
		payoffs.append(Drunk.Net_payoff)
	all_payoffs = np.sum(payoffs)

	filename=Par.dirname+('%i_total_payoffs.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(all_payoffs)
	file.write(s)
	file.write('\n')
	file.close()


#########################################################################################################
def mean_cooperation(exp, t, Drunks):
	cooperators = []
	for Drunk in Drunks:
		cooperators.append(Drunk.strat[0])
	mean_cooperators = np.mean(cooperators)
	std_dev_cooperators = np.std(cooperators)

	filename=Par.dirname+('%i_mean_cooperators.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(mean_cooperators)+ '	'+str(std_dev_cooperators)
	file.write(s)
	file.write('\n')
	file.close()
#########################################################################################################
def instant_cooperation(exp, t, Drunks):
	cooperators = []
	for Drunk in Drunks:
		if Drunk.cooperator == True:
			cooperators.append(1.0)
		else:
			cooperators.append(0.0)

	mean_cooperators = np.mean(cooperators)
	std_dev_cooperators = np.std(cooperators)

	filename=Par.dirname+('%i_instant_cooperators.dat' % exp)
	if t==0:
		file = open(filename, 'w')
	else:
		file = open(filename, 'a')

	s = str(t) + '	'+str(mean_cooperators)
	file.write(s)
	file.write('\n')
	file.close()

#########################################################################################################
def plot_data(exp):
	import matplotlib.pylab as plt
	# This will make a .png with 4 plots, the monomer-space landscape, Monomers vs T, Average Length vs time and Diversity vs Time
	fig= plt.figure()

	t,mean_alpha = np.loadtxt((Par.dirname+'%imean_alpha.dat' % (exp)),usecols= (0,1),  unpack = True)
	t,mean_cooperators = np.loadtxt((Par.dirname+'%imean_cooperators.dat' % (exp)), usecols= (0,1), unpack = True)
	ax1= fig.add_subplot(221)
	ax1.scatter(mean_cooperators, mean_alpha)
	x0,x1 = ax1.get_xlim()
	y0,y1 = ax1.get_ylim()
	plt.ylabel('mean alpha')
	plt.xlabel('mean cooperation')
	plt.axis([0,x1, 0,y1])

	t,alpha_c = np.loadtxt((Par.dirname+'%ialpha_c.dat' % (exp)),usecols= (0,1),  unpack = True)
	t,instant_cooperation = np.loadtxt((Par.dirname+'%iinstant_cooperators.dat' % (exp)), usecols= (0,1), unpack = True)
	ax2= fig.add_subplot(222)
	ax2.scatter(instant_cooperation, alpha_c)
	x0,x1 = ax2.get_xlim()
	y0,y1 = ax2.get_ylim()
	plt.ylabel('alpha_c')
	plt.xlabel('instant cooperation')
	plt.axis([0,x1, 0,y1])

	ax3= fig.add_subplot(223)
	ax3.scatter(t, alpha_c)
	x0,x1 = ax3.get_xlim()
	y0,y1 = ax3.get_ylim()
	plt.ylabel('alpha_c')
	plt.xlabel('time')
	plt.axis([0,x1, 0,y1])

	ax4= fig.add_subplot(224)
	ax4.scatter(t, mean_cooperators)
	x0,x1 = ax4.get_xlim()
	y0,y1 = ax4.get_ylim()
	plt.ylabel('mean cooperators')
	plt.xlabel('time')
	plt.axis([0,x1, 0,y1])



	plt.savefig(('%ik%.4f_r%.4f_d%.4f_Players%i.png' % (exp, Par.kappa, Par.r, Par.d, Par.num_agents)))

#########################################################################################################
def output_network(Bar_network, Drunks, exp, t = 0, draw = False):
	import networkx as nx 
	

	if Par.graph_type != 'Groups':
		fname = Par.dirname +'%i_bar_network_%i.xml' % (exp, t)
		nx.write_graphml(Bar_network, fname)

	elif Par.graph_type == 'Groups':
		from Parameters import Groups, Group_dict, p_out
		from Interactions import probability_interact, probability_accept
		weighted_net = nx.Graph()
		values= []

		edges = nx.edges(Bar_network)
		for match in edges:
			if not weighted_net.has_edge(match[0], match[1]):

				player1 = Drunks[match[0]]
				player2 = Drunks[match[1]]
				player1_group = Group_dict[match[0]]
				player2_group = Group_dict[match[1]]

				if player1_group == player2_group:
					p_in = 1 - p_out
					p_interact = probability_interact(p_in, player1.alpha )
					p_accept = probability_accept(player2.alpha, player1.alpha)
				else:
					p_interact = probability_interact(p_out, player1.alpha )
					p_accept = probability_accept(player2.alpha, player1.alpha)

				p_net = p_interact*p_accept

				weighted_net.add_edge(match[0], match[1], weight = p_net)

				values.append(p_net)
		

		#fname = Par.dirname +'%i_bar_network_%i.xml' % (exp, t)
		#nx.write_gexf(weighted_net, fname)
		fname = Par.dirname +'%i_bar_network_%i.csv' % (exp, t)
		nx.write_weighted_edgelist(weighted_net, fname, delimiter = ',')
		if draw == True:
			import matplotlib.pylab as plt
			import matplotlib.colors as colors
			import matplotlib.cm as cmx

			max_value = max(values)
			jet = cm = plt.get_cmap('Blues') 
			cNorm  = colors.Normalize(vmin=0, vmax=max_value)
			scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
			colorList = []
			
			for i in range(len(values)):
				colorVal = scalarMap.to_rgba(float(values[i])/float(max_value))
				colorList.append(colorVal)
			if t == 0:
				pos = nx.spring_layout(weighted_net)
				Par.pos = pos
			nx.draw(weighted_net, pos= Par.pos, edge_color=colorList)
			fname = Par.dirname +'%i_bar_network_%i.png' % (exp, t)
			plt.savefig(fname) # save as png
			plt.close()
#########################################################################################################
def show_networks(t_start, t_stop, freq, exp = 0):
	import networkx as nx 
	import matplotlib.pylab as plt
	import matplotlib.colors as colors
	import matplotlib.cm as cmx

	t = t_start
	while t < t_stop:

		fname = Par.dirname +'%i_bar_network_%i.csv' % (exp, t)
		nodes1, nodes2, weights  = np.loadtxt(fname, unpack = True, delimiter = ',')
		weighted_net = nx.Graph()

		for i in range(len(nodes1)):
			weighted_net.add_edge(nodes1[i], nodes2[i], weight = weights[i])

		max_value = max(weights)
		jet = cm = plt.get_cmap('Blues') 
		cNorm  = colors.Normalize(vmin=0, vmax=max_value)
		scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
		colorList = []
		
		for i in range(len(weights)):
			colorVal = scalarMap.to_rgba(float(weights[i])/float(max_value))
			colorList.append(colorVal)
		if t == t_start:
			pos = nx.spring_layout(weighted_net)
			Par.pos = pos
		nx.draw(weighted_net, pos= Par.pos, edge_color=colorList)
		plt.show()
		plt.close()
		t +=freq