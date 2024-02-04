#!/usr/bin/python

import os
import shutil
import multiprocessing
import time
Runs=[[2.0, 1.0, 20, 10],[2.0, 1.0, 200, 10], [2.0, 1.0, 2000, 10],
[2.0, 0.01, 20, 10],[2.0, 0.01, 200, 10], [2.0, 0.01, 2000, 10],
[2.0, 0.1, 20, 10],[2.0, 0.1, 200, 10], [2.0, 0.1, 2000, 10],
[2.0, 1.0, 20, 100],[2.0, 1.0, 200, 100], [2.0, 1.0, 2000, 100],
[2.0, 0.01, 20, 100],[2.0, 0.01, 200, 100], [2.0, 0.01, 2000, 100],
[2.0, 0.1, 20, 100],[2.0, 0.1, 200, 100], [2.0, 0.1, 2000, 100],
[2.0, 1.0, 20, 1000],[2.0, 1.0, 200, 1000], [2.0, 1.0, 2000, 1000],
[2.0, 0.01, 20, 1000],[2.0, 0.01, 200, 1000], [2.0, 0.01, 2000, 1000],
[2.0, 0.1, 20, 1000],[2.0, 0.1, 200, 1000], [2.0, 0.1, 2000, 1000]]
# [2.0, 0.15, 200],[2.0, 0.15, 2000], [2.0, 0.15, 20]
# [0.5, 0.075, 200],[0.5, 0.075, 2000], [0.5, 0.075, 20],
# [0.5, 0.025, 200],[0.5, 0.025, 2000], [0.5, 0.025, 20],
# [0.5, 0.15, 200],[0.5, 0.15, 2000], [0.5, 0.15, 20],
# [0.2, 0.075, 200],[0.2, 0.075, 2000], [0.2, 0.075, 20],
# [0.2, 0.025, 200],[0.2, 0.025, 2000], [0.2, 0.025, 20],
# [0.2, 0.15, 200],[0.2, 0.15, 2000], [0.2, 0.15, 20],
# [0.8, 0.075, 200],[0.8, 0.075, 2000], [0.8, 0.075, 20],
# [0.8, 0.025, 200],[0.8, 0.025, 2000], [0.8, 0.025, 20],
# [0.8, 0.15, 200],[0.8, 0.15, 2000], [0.8, 0.15, 20]]


jobs = []
job = 0
originalDirectory = os.getcwd()
pool = multiprocessing.Pool()
for i in range(len(Runs)):
    os.chdir(originalDirectory)
    import Parameters as Par
    
    Par.r =Runs[i][0]
    Par.kappa =Runs[i][1]
    Par.num_agents =Runs[i][2]
    Par.total_games= Runs[i][3]
    
    

    dirname = '/%iPlayers_%.2fkappa_%.2fd_%iGames/' %( Par.num_agents, Par.kappa, Par.d, Par.total_games)
    if not os.path.exists(originalDirectory+ dirname):
        os.makedirs(originalDirectory+ dirname)
    newdir = originalDirectory +dirname
    shutil.copy(originalDirectory+'/Main.py', newdir)
    shutil.copy(originalDirectory+'/Interactions.py', newdir+'/Interactions.py')
    shutil.copy(originalDirectory+'/Initialize.py', newdir+'/Initialize.py')
    shutil.copy(originalDirectory+'/Parameters.py', newdir+'/Parameters.py')
    shutil.copy(originalDirectory+'/Output.py', newdir+'/Output.py')
    shutil.copy(originalDirectory+'/Agents.py', newdir+'/Agents.py')
    
    os.chdir(newdir)
    Par.dirname = newdir
    for exp in range(1):
            
            import Parameters as Par
            Par.r =Runs[i][0]
            Par.kappa =Runs[i][1]
            Par.num_agents =Runs[i][2]
    
            from Main import main

            p = multiprocessing.Process(target=main)
            #print 'Job '+ str(exp) +' started.'
            jobs.append(p)
            p.start()
for job in jobs:
    p.join()

