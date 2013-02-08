#MaxP Regions Multi

import pysal
import copy
import random
import numpy as np
#from pysal.common import *
from pysal.region import randomregion as RR
from components import check_contiguity

#New imports
import multiprocessing as mp
from multiprocessing.sharedctypes import Array
import ctypes
from collections import deque
from random import randint, uniform
from numpy.random import RandomState

#Testing imports
import time

def _init_shared(updateflag_):
    global sharedupdate
    sharedupdate = updateflag_

def assign_enclaves(column, z, neighbordict):
    '''
    This function assigned enclaves by sequentially adding each enclave to all
     possible neighbors and accepting the soln with the lowest variance.  Sequential
     is import as we do not check for relationships between different enclave memberships, 
     just the variance of the current enclave.
    '''
    enclaves = np.where(sharedSoln[1:,column] == -1)#Returns a tuple of unassigned enclaves
    workingenclaves = np.copy(sharedSoln[1:,column])
    for enclave in enclaves[0]:#Iterate over the enclaves
        neighbors = neighbordict[enclave]
        #Iterate over the neighbors to the enclaves
        wss=float('inf')
        for neighbor in neighbors:
            #Now I need to know what groups the neighbor is in.
            group = sharedSoln[1:,column][neighbor]
            if group == -1: #Because we could assign an enclave to another enclave, fail the floor test that we do not perform again, and have a low variance...pain to debug this guy!
                break
            #Then add the enclave to that neighbor and test the variance
            workingenclaves[enclave] = group
            new_wss = objective_function_vec(column, z)
            if new_wss < wss:
                wss = new_wss
                sharedSoln[:,column][enclave] = group #If this is the current best, write it to the sharedmem space
    #Replace the p count with the wss, we can get at p whenever later with np.unique(p)
    sharedSoln[:,column][0] = wss
 
def check_soln(regions,numP,cores,w,z): #check the solution for min z
    '''This function queries the current IFS space to see if the currently computed soln is better than all other solns.
    '''
    
    def _regions_to_array(regions, newSoln):
        '''
        For large lists this function could be a great place to optimize.
        '''
        regionid = 0
        for region in regions:
            for member in region:
                newSoln[member] = regionid
            regionid += 1    
    
    sharedSoln = np.frombuffer(cSoln.get_obj())
    sharedSoln.shape = (numP,cores)
    if len(regions) >= sharedSoln[0].min(): #If any of the indices are less than p
        cSoln.get_lock()#Lock the entire shared memory array while we alter it
        column = np.argmin(sharedSoln[0]) #Get the index of the min value
        sharedSoln[0][column] = len(regions)#Write p to index 0
        newSoln = sharedSoln[1:,column] #Get a slice of the array,skipping index 0 that is the p counter
        newSoln[:] = -1 #Empty the column to be written
        _regions_to_array(regions, newSoln) #Iterate over the regions and assign their membership into the soln space               
                
def check_floor(region,floor_variable,w):
    '''
    Simple summation function that totals membership in a region and tests against
     the mandated floor value.
    '''
    if not type(region) == list: #Initialization passes a list, tabu passes an ndarray
        region.tolist()
    selectionIDs = [w.id_order.index(i) for i in region]
    cv = np.sum(floor_variable[selectionIDs])
    if cv >= floor:
        return True
    else:
        return False 

def initialize(job,z,w,neighborsdict,floor,floor_variable,numP,cores,maxattempts=100,threshold=0,suboptimal=None):
    '''
    The initialize function is simply a wrapper that pipes each core it's own 
    generator function.  That function, returns pre-enclave solutions by:
    1. Randomly select a starting polgyon.
    2. Add adjacent polygons until the floor is reached
    3. Break and return to 1.
    4. Once the only remaining polygons are enclaves test the current p value
        against all solutions in the shared memory solution space.
        
        If this solution is better, write it.  If not, break and return to 1 with
         an empty solution.
    
    The second time this function is called, the threshold passed is the maximum 
     value found in the the first mxattempts.  We then iterate again, attempting
     to find c solutions, one for each core, with the same p value.  This can occur
     up to 10**6 times before we break.  This limits total iterations, but only
     the most complex problems should ever get near c*(10**6) iterations.
    '''
    
    def iterate_to_p(job,z,w,neighborsdict,floor,floor_variable,numP,cores, maxattempts, threshold,suboptimal):
        solving = True 
        attempts = 0
        while solving and attempts <= maxattempts:
            regions = []
            enclaves = []
            seeds = [] #What are seeds doing?
            if not seeds:
                #If seeds is empty we need to generate a random weights list
                candidates = copy.copy(w.id_order)
                candidates = np.random.permutation(candidates)
                candidates = candidates.tolist()  
            else:
                seeds = copy.copy(seeds)
                nonseeds = [i for i in w.id_order if i not in seeds]
                candidates = seeds
                candidates.extend(nonseeds)
            while candidates:#Here we pick a random starting seed from all available candidates (not already in a region)
                seed = candidates.pop(0)
                region = [seed]
                building_region = True
                while building_region:
                    #check if floor is satisfied
                    if check_floor(region,floor_variable,w): #If this returns true, the region satisifies the floor constraint is 'completed'.  
                        regions.append(region)
                        building_region = False 
                    else: #Else - we are under the floor and must add the 'best' region.
                        potential = []
                        for area in region: #what are the neighbors of the current region
                            neighbors = neighborsdict[area]
                            neighbors = [neigh for neigh in neighbors if neigh in candidates]
                            neighbors = [neigh for neigh in neighbors if neigh not in region]
                            neighbors = [neigh for neigh in neighbors if neigh not in potential]
                            potential.extend(neighbors)
                        if potential:
                            # add a random neighbor
                            neigID = random.randint(0, len(potential) - 1)
                            neigAdd = potential.pop(neigID)
                            region.append(neigAdd)
                            # remove it from candidates
                            candidates.remove(neigAdd)
                        else:
                            #print 'enclave'
                            enclaves.extend(region)
                            building_region = False
                            #check to see if any regions were made before going to enclave stage
            if threshold == 0:
                if len(regions) >= threshold:
                    attempts += 1
                    yield regions
                else:
                    attempts += 1
            else:#Here we standardize the answers without limit to number of iterations.  Will that work?
                attempts += 1
                if len(suboptimal) == 0:
                    break
                if len(regions) == threshold:
                    suboptimal.pop()
                    yield regions              

    for regions in iterate_to_p(job,z,w,neighborsdict,floor,floor_variable,numP,cores, maxattempts, threshold,suboptimal): 
        check_soln(regions, numP,cores,w,z)
        
def objective_function_vec(column,attribute_vector):
    '''
    This is an objection function checker designed to access the 
    shared memory space.  It is suggested that this is faster than vectorization
    because we do not have to initialize additional in memory temp arrays.
    
    Parameters
    ----------
    z        :ndarray
              An array of attributes for each polygon
              
    Returns
    -------
    None     :-
              This writes the objective function to the 0 index of the sharedmem
              space, and overwrites sum(p) from the initialization phase.
    '''
    try:
        groups = sharedSoln[1:,column]
    except:
        groups = column
    wss = 0
    for group in np.unique(groups):
        #print group, attribute[groups==group]
        wss+= np.sum(np.var(attribute_vector[groups == group]))
    return wss
    #sharedSoln[0:,column][0] = wss

def set_half_to_best(cores):
    '''
    This function sets 1/2 of all solutions to the current best solution to 
     foster intensification. (James et al. 2009)
    '''
    current_best = np.argmin(sharedSoln[0])
    current_best_value = np.min(sharedSoln[0])
    num_top_half = (cores // 2)
    num_top_half -= len(np.where(sharedSoln[0] == current_best_value)[0])
    for soln in range(num_top_half):
        replace = np.argmax(sharedSoln[0])
        sharedSoln[:,replace] = sharedSoln[:,current_best]

def tabulength(numP):
    '''Talliard(1990)'''
    smin = (numP-1) * 0.9
    smax = (numP-1) * 1.1
    tabu_length = 6 + (randint(0,int(smax - smin)))
    return int(tabu_length)        

'''Test Data Generation a la PySAL tests.'''                                      
#Setup the test data:
w = pysal.lat2W(10, 10)
random_init = RandomState(123456789)
z = random_init.random_sample((w.n, 2))
#print z.max(), z.min(), z.std() #Comment out to verify that the 'random' seed is identical over tests
p = np.ones((w.n, 1), float) 
floor_variable = p
floor = 3

#Multiprocessing setup
cores = mp.cpu_count()
cores = cores * 2
numP = len(p)+1
#Shared memory solution space
lockSoln = mp.Lock()
cSoln = Array(ctypes.c_double, numP*cores, lock=lockSoln)
numSoln = np.frombuffer(cSoln.get_obj())
numSoln.shape = (numP,cores)
numSoln[:] = -1
#Shared memory update flag space
lockflag = mp.Lock()
c_updateflag = Array(ctypes.c_int, 3*(cores*2), lock=lockflag) #Do I need different locks? #Why double cores again?
updateflag = np.frombuffer(c_updateflag.get_obj())
updateflag.shape=(3,cores)
updateflag[0] = 1 #True for first iteration. - whether the answer was updated
updateflag[1] = 0 #Iteration counter per core.
for index in range(len(updateflag[2])): #Define the tabu list length for each chord.
    updateflag[2][index] = tabulength(numP)
_init_shared(updateflag)

neighbordict = dict(w.neighbors)#Class instances are not pickable.

#Phase Ia - Initialize a nubmer of IFS equal to the number of cores
jobs = []
for core in range(0,cores):
    proc = mp.Process(target=initialize, args=(core,z,w,neighbordict,floor,floor_variable,numP, cores))
    jobs.append(proc)
for job in jobs:
    job.start()
for job in jobs:
    job.join()
del jobs[:], proc, job

sharedSoln = np.frombuffer(cSoln.get_obj())
sharedSoln.shape = (numP, cores)
if sharedSoln.all() == -1: 
    #print "No initial feasible solutions found. Perhaps increase the number of iterations?"
    sys.exit(0)
#print sharedSoln

#Phase Ib - Standardize the values.
current_max_p = sharedSoln[0].max()
suboptimal = np.where(sharedSoln[0] < current_max_p)[0]
if suboptimal.size == 0:
    print "Solutions standardized, assigning enclaves"
else:
    manager = mp.Manager() #Create a manager to manage the coutdown
    suboptimal_countdown = manager.list(suboptimal)
    print "IFS with vaired p generated.  Standardizing to p=%i." %current_max_p
    jobs = []
    for core in range(0,cores):
        proc = mp.Process(target=initialize, args=(core,z,w,neighbordict,floor,floor_variable,numP,cores, 100, current_max_p,suboptimal_countdown))
        
        jobs.append(proc)
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()
    del jobs[:], proc, job        
#print sharedSoln

##This simply checks that we are not violating the floor.
#for column in range(4):
    #groups =  np.unique(sharedSoln[:,column])
    #for group in groups:
        #print group, np.where(sharedSoln[:,column]==group)[0]
    
 
#Phase Ic - Assign enclaves
jobs = []
for column_num in range(sharedSoln.shape[1]):
    proc = mp.Process(target=assign_enclaves, args=(column_num, z[:,0], neighbordict))
    jobs.append(proc)
for job in jobs:
    job.start()
for job in jobs:
    job.join()
del jobs[:], proc, job

#Phase Id - Set 50% soln to best current soln
set_half_to_best(cores)

#print sharedSoln[0]

def tabu_search(core, z, neighbordict,numP,w,floor_variable,lockSoln, lockflag, maxfailures=15,maxiterations=10):
    ##Pseudo constants
    pid = mp.current_process()._identity[0]
    tabu_list = deque(maxlen=sharedupdate[2][core])#What is this core's tabu list length? 
    maxiterations *= cores #Test synchronize cores to exit at the same time.
        
    maxfailures += int(maxfailures*uniform(-1.1, 1.2))#James et. al 2007
    
    def _tabu_check(tabu_list, neighbor, region, old_membership):
        if tabu_list:#If we have a deque with contents
            for tabu_region in(tabu_list):
                if neighbor == tabu_region[0]:
                    #print neighbor, tabu_region[0]
                    if region == tabu_region[1] and old_membership == tabu_region[2]:
                        return False    
    

    def _diversify_soln(core_soln_column, neighbordict,z, floor_variable,lockSoln):
        '''
        The goal of this function is to diversify a soln that is not improving.
        What about the possability of diversifying a good answer away from 'the soln?'
        I do no think that that should be an issue - we make a randomized greedy swap.  Is one enough?
        
        Rationale: This is a randomized Greedy swap (GRASP), where we store the best n permutations and then randomly select the one we will use.  Originally in Li et. al (in press).  We need to test different values of n to see what the impact is.
        '''
        #print "Diversifying: ", sharedSoln[0]

        #Initialize a local swap space to store n best diversified soln - these do not need to be better 
        div_soln_space = np.ndarray(sharedSoln.shape)
        div_soln_space[:] = float("inf")
        workingcopy = np.copy(sharedSoln[0:,core_soln_column])            

        #Iterate through the regions and check all moves, store the 4 best.
        for region in np.unique(workingcopy[1:]):
            members = np.where(workingcopy == region)[0]
            neighbors = []
            for member in members:
                candidates = neighbordict[member-1]#neighbordict is 0 based, member is 1 based
                candidates = [candidate for candidate in candidates if candidate not in members]
                candidates = [candidate for candidate in candidates if candidate not in neighbors]
                neighbors.extend(candidates)
            candidates = []
            
            #Iterate through the neighbors
            for neighbor in neighbors:
                neighborcopy = np.copy(workingcopy[:]) #Pull a copy of the local working version
                old_membership = neighborcopy[neighbor]#Track where we started to check_floor
                
                neighborcopy[neighbor] = region #Move the neighbor into the new region in the copy
                
                #Here we start to check the swap and see if it is better
                swap_var = objective_function_vec(neighborcopy[1:],z)#Variance of the new swap
                if not swap_var < div_soln_space[0].any():
                    block = np.where(workingcopy[1:] == neighbor)[0]#A list of the members in a region.
                    block=block.tolist() #For current contiguity check
                    if check_contiguity(neighbordict, block, neighbor):#Check contiguity
                        if check_floor(np.where(neighborcopy[1:,]==region)[0], floor_variable, w) and check_floor(np.where(neighborcopy[1:,]==old_membership)[0],floor_variable,w):
                            
                            neighborcopy[0] = swap_var
                            if not np.isinf(div_soln_space[0].any()):
                                div_soln_space[:,np.argmax(div_soln_space[0])] = neighborcopy[:]
                            else:
                                div_soln_space[:,np.argmin(div_soln_space[0])] = neighborcopy[:]
                        else:
                            del neighborcopy
                            #print "Swap failed due to floor_check."
                    else:
                        del neighborcopy
                        #print "Swap failed due to contiguity."
        #It is possible that the perturbation will not generate enough soln to fill the space, 
        # so we need to ignore those columns with variance = infinity.
        
        #Write one of the neighbor perturbations to the shared memory space to work on.
        valid = np.where(div_soln_space[0] != np.inf)[0]
        try:
            selection = randint(0,len(valid)-1)
            with lockSoln:
                sharedSoln[:,core_soln_column] = div_soln_space[:,selection]
                #print "Diversified to:", sharedSoln[0]
        except:
            pass
            #print div_soln_space[0]
            #print "Attempt to diversify failed."
            

        
    ##This shows that we are operating asynchronously.   
    #if core ==2:
        #time.sleep(5)
    
    while sum(sharedupdate[1]) < maxiterations:
        core_soln_column = (core + sharedupdate[1][core])%len(sharedupdate[1]) #This iterates the cores around the search space.
        
        #Check for diversification here and diversify if necessary...
        if sharedupdate[0][core_soln_column] == False:
            _diversify_soln(core_soln_column, neighbordict,z, floor_variable,lockSoln) #Li, et. al (in press - P-Compact_Regions)

        #print "ProcessID %i is processing soln column %i in iteration %i."%(pid, core_soln_column,sharedupdate[1][core]) #Uncomment to see that cores move around the search space    
        failures = 0 #The total iteration counter
        #What are the current best solutions local to this core?
        local_best_variance = sharedSoln[:,core_soln_column][0]
        workingSoln = np.copy(sharedSoln[:,core_soln_column])    
        
        while failures <= maxfailures:#How many total iterations can the core make
      
            #Select a random starting point in the search space.
            nr = np.unique(workingSoln[1:]) #This is 0 based, ie. region 0 - region 31
            regionIDs = nr
            changed_regions = np.ones(len(nr))
            randstate = RandomState(pid) #To 'unsync' the cores we need to instantiate a random class with a unique seed.
            randstate.shuffle(regionIDs) #shuffle the regions so we start with a random region
            changed_regions[:] = 0
            swap_flag = False #Flag to stop looping prior to max iterations if we are not improving.
            
            #Iterate through the regions, checking potential swaps
            for region in regionIDs:
                members = np.where(workingSoln == region)[0] #get the members of the region
                #print region, members
                #Get the neighbors to the members.  Grab only those that could change.
                neighbors = []
                for member in members:
                    candidates = neighbordict[member-1]#neighbordict is 0 based, member is 1 based
                    candidates = [candidate for candidate in candidates if candidate not in members]
                    candidates = [candidate for candidate in candidates if candidate not in neighbors]
                    neighbors.extend(candidates)
                candidates = []
                
                #Iterate through the neighbors
                for neighbor in neighbors:
                    neighborSoln = np.copy(workingSoln[:]) #Pull a copy of the local working version
                    old_membership = neighborSoln[neighbor]#Track where we started to check_floor
                    
                    tabu_move_check =_tabu_check(tabu_list, neighbor, region, old_membership)
                    if tabu_move_check is not None:
                        break
                    
                    neighborSoln[neighbor] = region #Move the neighbor into the new region in the copy
                    
                    #Here we start to check the swap and see if it is better
                    swap_var = objective_function_vec(neighborSoln[1:],z)#Variance of the new swap
                    if swap_var <= local_best_variance:
                        block = np.where(workingSoln[1:] == neighbor)[0]#A list of the members in a region.
                        block=block.tolist() #For current contiguity check
                        if check_contiguity(neighbordict, block, neighbor):#Check contiguity
                            if check_floor(np.where(neighborSoln[1:,]==region)[0], floor_variable, w) and check_floor(np.where(neighborSoln[1:,]==old_membership)[0],floor_variable,w):#What about the floor of the region loosing the member in the original code?
                                #print "Swap made on core %i.  Objective function improved from %f to %f." %(pid, swap_var, local_best_variance)
                                local_best_variance = swap_var#Set the new local best to the swap. We have made a swap that betters the objective function.
                                neighborSoln[0] = swap_var
                                workingSoln[:] = neighborSoln[:]
                                swap_flag = True #We made a swap
                                tabu_list.appendleft((neighbor,old_membership,region))#tuple(polygon_id, oldgroup,newgroup)
                            else:
                                del neighborSoln
                                #print "Swap failed due to floor_check."
                        else:
                            del neighborSoln
                            #print "Swap failed due to contiguity."
                    
            if swap_flag == False:
                #print "Failed to make any swap, incrementing the fail counter."
                failures += 1
            
        #print workingSoln, len(np.unique(workingSoln[1:]))    
        
        with lockflag:
            sharedupdate[0][core_soln_column] = 0 #Set the update flag to false
            #print "Locking update flag to set to false"
        
        with lockSoln:#The lock is released at the end of the with statement
            sharedSoln[:,core_soln_column]#Lock the column of the shared soln we are using.
            if workingSoln[0] < sharedSoln[:,core_soln_column][0]:
                sharedSoln[:,core_soln_column]
                sharedSoln[:,core_soln_column] = workingSoln
                #print "Better soln loaded into sharedSoln: %f." %(workingSoln[0])
                sharedupdate[0][core_soln_column] = 1 #Set the update flag to true
                if not workingSoln[0] < sharedSoln[0].any():
                    set_half_to_best(len(sharedSoln[0]))
                    #print "Setting half the soln to new global best. ", sharedSoln[0]
        #Increment the core iteration counter    
        sharedupdate[1][core] += 1
    
        #print "Process %i completed iteration %i/%i." %(pid, sharedupdate[1][core], maxiterations)
        #print sharedupdate[0]
        
#Phase II - Swapping
print "Initiating Phase II: Tabu Search"

#We  need an iterator here to count max iterations or total time to work or something.  We track failures internal to each process.
for core in range(cores):
    proc = mp.Process(target=tabu_search, args=(core, z[:,0], neighbordict, numP,w,floor_variable, lockSoln, lockflag))
    jobs.append(proc)
for job in jobs:
    job.start()
for job in jobs:
    job.join()
del jobs[:], proc, job

print "Regions: ", len(np.unique(sharedSoln[1:,0]))
print "New Solutions: ", sharedSoln[0]
print "Update Flags: ", sharedupdate[0]
print "Iteration Counter: ",sharedupdate[1]
print "Tabu length: ",sharedupdate[2]