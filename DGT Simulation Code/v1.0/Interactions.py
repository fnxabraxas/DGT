# Cole Mathis 2014
# CSSS14 Drunk GT

import random
import numpy as np 
import matplotlib.pylab as plt
from time import clock
import networkx as nx
import Parameters as Par
###############################################################################################################
def alpha_update(alpha_0, Beers):
	''' Returns the new alpha value of a player given their current alpha and the beers they consume'''

	new_alpha = (1.0- alpha_0)*Par.kappa*Beers/(Par.r) +(1.0-Par.d)*alpha_0
	if new_alpha > 1.0:
		print new_alpha
		print "alpha went over 1"
	return new_alpha
# Sober pay off matrix #########################################################################
def sober_game(You_Offer,Opponent_Offers):
	'''Returns the payoff and the number of beers consumed based on each players action for a sober player '''
	# Returns a tuple: (Pay-Off, Beers)
	if(You_Offer==True):
		# print 'Player One is offering'
		# raw_input('Press Enter to continue...')
		if(Opponent_Offers==True):
			return (Par.A_s, Par.W_s)
		else:
			return (Par.B_s, Par.X_s)
	else:
		# print 'Player One isnt offering'
		# raw_input('Press Enter to continue...')
		if(Opponent_Offers==True):
			return (Par.C_s, Par.Y_s)
		else:
			return (Par.D_s, Par.Z_s)

# Drunk Pay off Matrix #########################################################################
def drunk_game(You_Offer,Opponent_Offers):
	'''Returns the payoff and the number of beers consumed based on each players action for a drunk player '''
	'''Returns a tuple: (Pay-Off, Beers) '''
	if(You_Offer==True):
		# print 'Player is offering'
		# raw_input('Press Enter to continue...')
		if(Opponent_Offers==True):
			# print 'Oppenent is offering'
			# raw_input('Press Enter to continue...')
			return (Par.A_d, Par.W_d)
		else:
			# print 'Oppenent isnt offering'
			# raw_input('Press Enter to continue...')
			return (Par.B_d, Par.X_d)
	else:
		# print 'Player isnt offering'
		# raw_input('Press Enter to continue...')
		if(Opponent_Offers==True):
			# print 'Oppenent is offering'
			# raw_input('Press Enter to continue...')
			return (Par.C_d, Par.Y_d)
		else:
			# print 'Oppenent isnt offering'
			# raw_input('Press Enter to continue...')
			return (Par.D_d, Par.Z_d)

################################################################################################
################################################################################################
def play_game(match, Drunks):
	'''Two players engaged in the game of the pub '''
	ID1 = match[0]
	ID2 = match[1]

	player1 = Drunks[ID1]
	player2 = Drunks[ID2]
	
	# Determine which action each player will use
	Player_One_Sober = True
	Player_Two_Sober = True

	Player_One_Offers = False
	Player_Two_Offers = False

	player1.cooperator = False
	player2.cooperator = False

	# Determine which game they are playing
	dice_roll = random.random()
	if dice_roll <= player1.alpha:
		Player_One_Sober = False
		# print 'Player 1 Offers'

	dice_roll = random.random()
	if dice_roll <= player2.alpha:
		Player_Two_Sober = False

	dice_roll = random.random()
	if dice_roll <= player1.strat[0]:
		Player_One_Offers = True
		player1.cooperator = True
		# print 'Player 1 Offers'

	dice_roll = random.random()
	if dice_roll <= player2.strat[0]:
		Player_Two_Offers = True
		player2.cooperator = True
	# 	print 'Player 2 Offers'

	# Play the game
	Player_One_Payoff = 0
	Player_One_Beers = 0
	Player_Two_Payoff = 0
	Player_Two_Beers = 0

	# Player One payoff/drinks
	if Player_One_Sober == True: 
		(Player_One_Payoff, Player_One_Beers) = sober_game(Player_One_Offers, Player_Two_Offers)
	else:
		(Player_One_Payoff, Player_One_Beers) = drunk_game(Player_One_Offers, Player_Two_Offers)

	# Player Two payoff/drinks
	if Player_Two_Sober == True:
		(Player_Two_Payoff, Player_Two_Beers) = sober_game(Player_Two_Offers, Player_One_Offers)
	else:
		(Player_Two_Payoff, Player_Two_Beers) = drunk_game(Player_Two_Offers, Player_One_Offers)
	#if Player_Two_Payoff < 0.0 or Player_One_Payoff < 0.0:
	#	print "Negative Payoffs"
	# Update Players
	player1.beers +=Player_One_Beers
	player2.beers += Player_Two_Beers

	player1.payoff += Player_One_Payoff
	player2.payoff += Player_Two_Payoff

	player1.Net_payoff += Player_One_Payoff
	player2.Net_payoff += Player_Two_Payoff

	# New Alphas
	Alpha_1 = alpha_update(player1.alpha, Player_One_Beers)
	player1.alpha = Alpha_1
	#print 'Alpha_1', Alpha_1

	Alpha_2 = alpha_update(player2.alpha, Player_Two_Beers)
	player2.alpha = Alpha_1
	#print 'Alpha_2', Alpha_2
###############################################################################################################
def pick_match(Bar_network, Drunks):
	from Parameters import Group_dict, p_out
	#If it's anything other than group dynamics, we are just picking an edge
	if Par.graph_type != 'Groups':
		[match] =  random.sample(Bar_network.edges(),1)

	# If it's group dynamics, we need to find a match weighted by the alpha level and in the out_group probability
	elif Par.graph_type == 'Groups':
		# We iterate until we find a match that's accepted.
		accepted = False
		while accepted == False:
			[match] =  random.sample(Bar_network.edges(),1)

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

			net_probability = p_accept*p_interact
			dice_roll = random.random()
			if dice_roll < net_probability:
				accepted = True
	return match
###############################################################################################################
def probability_interact(p_o, alpha):
	# Probability of interacting with someone given your sober probability of interacting with them, and your alpha
	p = (1.0-alpha)*p_o + (alpha/2.0)
	return p 
###############################################################################################################
def probability_accept(alpha_prompted, alpha_asking):
	# Probability of accepting an interaction with another person given you alphas
	p = 1.0 - np.abs(alpha_prompted - alpha_asking)
	return p 
###############################################################################################################
def match_players(Agents):
	'''Match up drunk assholes with other drunk jackasses '''
	matches = []
	temp_list = random.sample(Agents, Par.num_agents)

	i = 0
	while i < (Par.num_agents/2):
		matches.append( (temp_list[i], temp_list[i+1]) )
		i += 2

	return matches

##############################################################################################################
def update_strat_global(Drunks, matches):

	for Drunk in Drunks:
		Temp_Drunks = Drunks[:]
		Temp_Drunks.remove(Drunk)

		Drunk_payoff = 0.0
		for opponent in Temp_Drunks:
			(single_pay, single_beer)= payoff_matrix(Drunk.cooperator, Drunk.alpha, opponent.cooperator)
			Drunk_payoff += single_pay

		Drunk.Net_payoff = float(Drunk_payoff)/float(2*Par.num_agents)

	for match in matches:
		p_ji = (match[0].Net_payoff-match[1].Net_payoff)/(Par.r*Par.b)
		p_ij = (match[1].Net_payoff-match[0].Net_payoff)/(Par.r*Par.b)

		if p_ij < 0.0 and p_ji < 0.0:
			print "Switch probabilities incorrect."
		if p_ij > 1.0 or p_ji > 1: 
			print "Switch probabilities incorrect, >1."

		dice_roll = random.random()

		if dice_roll <= p_ij:
			match[0].strat = match[1].strat

		dice_roll = random.random()

		if dice_roll <= p_ji:
			match[1].strat = player1.strat
##############################################################################################################
def update_strat_local(player, Bar_network, Drunks):
	
	repeated_player, neighbors = zip(*nx.edges(Bar_network, player))
	probabilities = []
	
	player1 = Drunks[player]
	player1_drunk =False
	# Drunk Update vs Sober Update
	dice_roll = random.random()
	if dice_roll < player1.alpha:
		# Drunk
		player1_drunk = True
		

	payoffs = []
	for neighbor in neighbors:
		player2 = Drunks[neighbor]
		repeated_player, neighbors2 = zip(*nx.edges(Bar_network, neighbor))
		if player1_drunk == True:
			phi = (max([len(neighbors2), len(neighbors)]))*(max([Par.A_d, Par.C_d]) - min([Par.B_d, Par.D_d])) 
		else:
			phi = (max([len(neighbors2), len(neighbors)]))*(max([Par.A_s, Par.C_s]) - min([Par.B_s, Par.D_s])) 


		if player2.Net_payoff > player1.Net_payoff:
			
			p_ij = (player2.Net_payoff - player1.Net_payoff)/phi
			if p_ij < 0.0:
				print "Negative Change probabilities"
				print p_ij
				print [player2.Net_payoff, player1.Net_payoff]
		elif player2.Net_payoff <= player1.Net_payoff:
			p_ij = 0.0

		probabilities.append(p_ij)

	change_strat = False
	P_maintain = 1
	for i in range(len(probabilities)):
		P_maintain = P_maintain*(1-probabilities[i])
	dice_roll = random.random()

	if dice_roll > P_maintain:
		change_strat = True

	if change_strat == True:
		dice_roll = sum(probabilities)*random.random()
		checkpoint = 0.0
		for i in range(len(probabilities)):
			checkpoint += probabilities[i]

			if checkpoint >= dice_roll:
				new_strat_ID = neighbors[i]
				break
		Drunks[player].strat = Drunks[new_strat_ID].strat[:]
