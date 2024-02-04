import numpy as np
import Parameters
import matplotlib.pylab as plt
import matplotlib.colors as mplcolors
import matplotlib.cm as cm
import matplotlib
print Parameters.dirname
import seaborn as sns
import matplotlib.gridspec as gridspec

from Parameters import num_agents, num_experiments,num_IC,barabasi_albert_m, lattice_neighbors, regular_d, beta,T,S, T_prime, S_prime, edge_p, num_groups, p_out, RGG_r 

### Boiler Plate Plotting stuff
font = {'weight' : 'bold',
        'size'   : 16}
matplotlib.rc('font', **font)

# Here we will just look at the first two time steps because we ran many different Initial Conditions 
t1 = 0
t2 = 1

topologies = ['None', 'Random', 'Regular', 'Geometric', 'Lattice']
kappa_values = [10.0, 1.0, 0.1, 0.01]
cols = ['$\kappa = $%.2f'%kappa for kappa in kappa_values]
pad = 5 # in points

rows = len(topologies)
columns = len(kappa_values)
gs = gridspec.GridSpec(rows, columns)
axes = []

for graph_type in topologies:
    y = topologies.index(graph_type)
    for kappa in kappa_values:
        x = kappa_values.index(kappa)
        xs_arr = np.empty((num_IC, num_experiments) )
        delta_x_arr = np.empty((num_IC, num_experiments) )
        alphas_arr = np.empty((num_IC, num_experiments) )
        delta_alpha_arr = np.empty((num_IC, num_experiments) )
        magnitudes_arr = np.empty((num_IC, num_experiments) )
        colors_arr = np.empty((num_IC, num_experiments) )

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

        for exp in range(num_experiments):

            fname =dirname + '%i_average_agent_data.npy' % (exp)
            fdata = np.load(fname)

            for ic in range(num_IC):
                i = 2*ic
                j = 2*ic + 1
                xi = fdata[i,4]
                xj = fdata[j,4]
                ai = fdata[i,2]
                aj = fdata[j,2]
                dx = xj-xi
                da = aj-ai
                xs_arr[ic,exp] =xi
                alphas_arr[ic,exp] = ai
                magnitude = np.sqrt(dx**2 + da**2)
                delta_x_arr[ic,exp] = dx/magnitude
                delta_alpha_arr[ic, exp] = da/magnitude

                magnitudes_arr[ic,exp] = magnitude
                
        xs = np.mean(xs_arr, axis =1)
        delta_x = np.mean(delta_x_arr, axis= 1)
        alphas = np.mean(alphas_arr, axis = 1)
        delta_alpha = np.mean(delta_alpha_arr, axis = 1)
        magnitudes = np.mean(magnitudes_arr,axis = 1)
        colors = np.mean(colors_arr, axis =1)
        magnitudes = magnitudes/max(magnitudes)
        #print 'Max: ', max(magnitudes)
        #print "Min: ", min(magnitudes)

        seaborn_cmap = sns.cubehelix_palette(start=0.0, rot=0.0, as_cmap = True)
        jet = mplcolors.Colormap('jet', N =len(magnitudes) )
        norm = mplcolors.Normalize(vmin=min(magnitudes), vmax=max(magnitudes))
        scale_map = cm.ScalarMappable(cmap=seaborn_cmap, norm = norm)
        #print magnitudes
        colors  = scale_map.to_rgba(magnitudes)
        ax = plt.subplot(gs[y,x])
        axes.append(ax)
        ax.quiver(xs, alphas, delta_x, delta_alpha, magnitudes, cmap = cm.winter, pivot = 'mid')
        plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='on',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='on') # labels along the bottom edge are off
        # plt.title('$\kappa$ = %.3f' % kappa)
        if x == 0:
            ax.annotate(topologies[y], xy=(0, 0.5), xytext=(-ax.yaxis.labelpad - pad, 0),
                xycoords=ax.yaxis.label, textcoords='offset points',
                size='large', ha='right', va='center')
        if y == 0: 
            ax.annotate(cols[x], xy=(0.5, 1), xytext=(0, pad),
                xycoords='axes fraction', textcoords='offset points',
                size='large', ha='center', va='baseline')
        plt.xlabel('$x$')
        plt.ylabel('$a$')
        plt.ylim([0.0, 1.0])
        plt.xlim([0.0, 1.0])
    


fig = plt.gcf()
fig.set_size_inches(14.0, 10.0)


fig.tight_layout()
# tight_layout doesn't take these labels into account. We'll need 
# to make some room. These numbers are are manually tweaked. 
# You could automatically calculate them, but it's a pain.
fig.subplots_adjust(left=0.15, top=0.95)

#plt.show()


#plt.tight_layout()
fig.savefig('CompleteVectorMap.pdf', dpi=2000)
#plt.show()