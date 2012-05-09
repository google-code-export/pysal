"""
Max p regionalization

Heuristically form the maximum number (p) of regions given a set of n areas and a floor
constraint.
"""

__author__ = "Serge Rey <srey@asu.edu>, David Folch <david.folch@asu.edu>"


import pysal
from components import check_contiguity, check_contiguity_2
from pysal.common import *
from pysal.region import randomregion as RR
import multiprocessing as mp
import time

LARGE=10**6
MAX_ATTEMPTS=100

class Maxp:
    """Try to find the maximum number of regions for a set of areas such that
    each region combines continguous areas that satisfy a given threshold
    constraint.
    
    
    Parameters
    ----------
 
    w               : W
                      spatial weights object
                    
    z               : array
                      n*m array of observations on m attributes across n
                      areas. This is used to calculate intra-regional
                      homogeneity
    floor           : int
                      a minimum bound for a variable that has to be
                      obtained in each region
    floor_variable  : array
                      n*1 vector of observations on variable for the floor
    initial         : int number of initial solutions to generate

    verbose         : binary
                      if true debugging information is printed

    seeds           : list
                      ids of observations to form initial seeds. If
                      len(ids) is less than the number of observations, the
                      complementary ids are added to the end of seeds. Thus
                      the specified seeds get priority in the solution
     
    Attributes
    ----------

    area2region     : dict
                      mapping of areas to region. key is area id, value is
                      region id
    regions         : list
                      list of lists of regions (each list has the ids of areas
                      in that region)
    swap_iterations : int
                      number of swap iterations
    total_moves     : int
                      number of moves into internal regions

    Examples
    --------

    >>> import random
    >>> import numpy as np
    >>> random.seed(100)
    >>> np.random.seed(100)
    >>> w=pysal.lat2W(10,10)
    >>> z=np.random.random_sample((w.n,2))
    >>> p=np.random.random(w.n)*100
    >>> p=np.ones((w.n,1),float)
    >>> floor=3
    >>> solution=Maxp(w,z,floor,floor_variable=p,initial=100)
    >>> solution.p
    30
    >>> solution.regions[0]
    [49, 39, 29]
    >>> 

    """
    def __init__(self,w,z,floor,floor_variable,
                verbose=False,initial=100,seeds=[]):
    
        self.w=w
        self.z=z
        self.floor=floor
        self.floor_variable=floor_variable
        self.verbose=verbose
        self.seeds=seeds

        self.initial_solution()
        if not self.p:
            self.feasible = False
        else:
            self.feasible = True
            self.current_regions=copy.copy(self.regions)
            self.current_area2region=copy.copy(self.area2region)
            """
            self.initial_wss=[]
            self.attempts=0
            for i in range(initial):
                self.initial_solution()
                if self.p:
                    val=self.objective_function()
                    self.initial_wss.append(val)
                    if self.verbose:
                        print 'initial solution: ',i, val,best_val
                    if val < best_val:
                        self.current_regions=copy.copy(self.regions)
                        self.current_area2region=copy.copy(self.area2region)
                        best_val=val
                    self.attempts += 1
            self.regions=copy.copy(self.current_regions)
            self.area2region=self.current_area2region
            """
            
            curval = self.objective_function(self.regions)
            self.initial_wss=[]
            self.attempts=0
                
            time2 = time.clock()
            numOfProcess = 4
            pool = mp.Pool(processes = numOfProcess)
            id1 = self.w.id_order
            neighbor1 = dict(self.w.neighbors)
            arguments = []
            for i in range(numOfProcess):
                arguments.append([curval, initial/numOfProcess, self.z, self.floor, self.floor_variable, id1, neighbor1])
            time3 = time.clock()
            print "The preparation for parallel took %.3f seconds" % (time3 - time2)
            results = pool.map(pickBest, arguments)
            pool.terminate()
                
            winVal = 100000
            winNum = 0
            for i in range(len(results)):
                if results[i][2] < winVal:
                    winVal = results[i][2]
                    winNum = i
                
            self.regions = results[winNum][0]
            self.area2region = results[winNum][1]
            self.p = len(self.regions)
            
            time3 = time.clock()
            print "The parallel part took %.3f seconds" % (time3 - time2)
            print winVal
        
    def pickBest(self, initial):
		curval = self.objective_function(self.regions)
		self.initial_wss=[]
		self.attempts=0
		for i in range(initial):
			self.initial_solution()
			if self.p:
				val=self.objective_function()
				self.initial_wss.append(val)
				if self.verbose:
					print 'initial solution: ',i, val,curval
				if val < curval:
					self.current_regions=copy.copy(self.regions)
					self.current_area2region=copy.copy(self.area2region)
					curval=val
				self.attempts += 1
		self.regions=copy.copy(self.current_regions)
		self.area2region=self.current_area2region

    def initial_solution(self):
        self.p=0
        solving=True
        attempts=0
        while solving and attempts<=MAX_ATTEMPTS:
            regions=[]
            enclaves=[]
            if not self.seeds:
                candidates=copy.copy(self.w.id_order)
                candidates=np.random.permutation(candidates)
                candidates=candidates.tolist()
            else:
                seeds = copy.copy(self.seeds)
                nonseeds=[ i for i in self.w.id_order if i not in seeds]
                candidates=seeds
                candidates.extend(nonseeds)
            while candidates:
                seed=candidates.pop(0)
                # try to grow it till threshold constraint is satisfied
                region=[seed]
                building_region=True
                while building_region:
                    # check if floor is satisfied
                    if self.check_floor(region):
                        regions.append(region)
                        building_region=False
                    else:
                        potential=[] 
                        for area in region:
                            neighbors=self.w.neighbors[area]
                            neighbors=[neigh for neigh in neighbors if neigh in candidates]
                            neighbors=[neigh for neigh in neighbors if neigh not in region]
                            neighbors=[neigh for neigh in neighbors if neigh not in potential]
                            potential.extend(neighbors)
                        if potential:
                            # add a random neighbor
                            neigID=random.randint(0,len(potential)-1)
                            neigAdd=potential.pop(neigID)
                            region.append(neigAdd)
                            # remove it from candidates
                            candidates.remove(neigAdd)
                        else:
                            #print 'enclave'
                            #print region
                            enclaves.extend(region)
                            building_region=False
            # check to see if any regions were made before going to enclave stage
            if regions:
                feasible=True
            else:
                attempts+=1
                break
            self.enclaves=enclaves[:]
            a2r={}
            for r,region in enumerate(regions):
                for area in region:
                    a2r[area]=r
            encCount=len(enclaves)
            encAttempts=0
            while enclaves and encAttempts!=encCount:
                enclave=enclaves.pop(0)
                neighbors=self.w.neighbors[enclave]
                neighbors=[neighbor for neighbor in neighbors if neighbor not in enclaves]
                candidates=[]
                for neighbor in neighbors:
                    region=a2r[neighbor]
                    if region not in candidates:
                        candidates.append(region)
                if candidates:
                    # add enclave to random region
                    regID=random.randint(0,len(candidates)-1)
                    rid=candidates[regID]
                    regions[rid].append(enclave)
                    a2r[enclave]=rid
                    # structure to loop over enclaves until no more joining is possible
                    encCount=len(enclaves)
                    encAttempts=0
                    feasible=True
                else:
                    # put back on que, no contiguous regions yet
                    enclaves.append(enclave)
                    encAttempts+=1
                    feasible=False
            if feasible:
                solving=False
                self.regions=regions
                self.area2region=a2r
                self.p=len(regions)
            else:
                if attempts==MAX_ATTEMPTS:
                    print 'No initial solution found'
                    self.p=0
                attempts+=1

    def swap(self):
        swapping=True
        swap_iteration=0
        if self.verbose:
            print 'Initial solution, objective function: ',self.objective_function()
        total_moves=0
        self.k=len(self.regions)
        changed_regions=[1]*self.k
        nr=range(self.k)
        while swapping:
            moves_made=0
            regionIds=[r for r in nr if changed_regions[r]] 
            np.random.permutation(regionIds)
            changed_regions=[0]*self.k
            swap_iteration+=1
            for seed in regionIds:
                local_swapping=True
                local_attempts=0
                while local_swapping:
                    local_moves=0
                    # get neighbors
                    members=self.regions[seed]
                    neighbors=[]
                    for member in members:
                        candidates=self.w.neighbors[member]
                        candidates=[candidate for candidate in candidates if candidate not in members]
                        candidates=[candidate for candidate in candidates if candidate not in neighbors]
                        neighbors.extend(candidates)
                    candidates=[]
                    for neighbor in neighbors:
                        block=copy.copy(self.regions[self.area2region[neighbor]])
                        if check_contiguity(self.w,block,neighbor):
                            fv=self.check_floor_Move(block)
                            if fv:
                                candidates.append(neighbor)
                    # find the best local move 
                    if not candidates:
                        local_swapping=False
                    else:
                        nc=len(candidates)
                        moves=np.zeros([nc,1],float)
                        best=None
                        cv=0.0
                        for area in candidates:
                            current_internal=self.regions[seed]
                            current_outter=self.regions[self.area2region[area]]
                            current=self.objective_function([current_internal,current_outter])
                            new_internal=copy.copy(current_internal)
                            new_outter=copy.copy(current_outter)
                            new_internal.append(area)
                            new_outter.remove(area)
                            new=self.objective_function([new_internal,new_outter])
                            change=new-current
                            if change < cv:
                                best=area
                                cv=change
                        if best:
                            # make the move
                            area=best
                            old_region=self.area2region[area]
                            self.regions[old_region].remove(area)
                            self.area2region[area]=seed
                            self.regions[seed].append(area)
                            moves_made+=1
                            changed_regions[seed]=1
                            changed_regions[old_region]=1
                        else:
                            # no move improves the solution
                            local_swapping=False
                    local_attempts+=1
                    if self.verbose:
                        print 'swap_iteration: ',swap_iteration,'moves_made: ',moves_made
                        print 'number of regions: ',len(self.regions)
                        print 'number of changed regions: ',sum(changed_regions)
                        print 'internal region: ',seed, 'local_attempts: ',local_attempts
                        print 'objective function: ',self.objective_function()
            total_moves+=moves_made
            if moves_made==0:
                swapping=False
                self.swap_iterations=swap_iteration
                self.total_moves=total_moves
            if self.verbose:
                print 'moves_made: ',moves_made
                print 'objective function: ',self.objective_function()

    def check_floor(self,region):                
        selectionIDs = [self.w.id_order.index(i) for i in region]
        cv=sum(self.floor_variable[selectionIDs])
        if cv >= self.floor:
            return True
        else:
            return False
    
    def check_floor_Move(self,region):                
        selectionIDs = [self.w.id_order.index(i) for i in region]
        cv=sum(self.floor_variable[selectionIDs])
        if cv > self.floor:
            return True
        else:
            return False

    def objective_function(self,solution=None):
        # solution is a list of lists of region ids [[1,7,2],[0,4,3],...] such
        # that the first region has areas 1,7,2 the second region 0,4,3 and so
        # on. solution does not have to be exhaustive
        if not solution:
            solution=self.regions
        wss=0
        for region in solution:
            selectionIDs = [self.w.id_order.index(i) for i in region]
            m=self.z[selectionIDs,:]
            var=m.var(axis=0)
            wss+=sum(np.transpose(var))*len(region)
        return wss

def swap(argu):
	regionID = argu[0]					# The current region to be swapped at start
	target_regions = argu[1]			# All regions potentially to be considered
	target_area2region = argu[2]		# Mappings from area to Region
	floor_var = argu[3]
	floor = argu[4]
	id_order = argu[5]					# The ids of all areas
	neighborDict = argu[6]				# Neighborhood dictionary of all areas
	zObj = argu[7]						# Data values, one pair corresponding to each area
	swapping=True
	swap_iteration=0
	total_moves=0
	target_k=len(target_regions)		# Number of regions to be considered
	changed_regions=[1]*target_k		# Indicator of whether an region has been changed 
	nr=range(target_k)					# Index of all regions
	while swapping:
		moves_made=0
		regionIds=[r for r in nr if changed_regions[r]]		# only pay attention to areas that have been changed?
		np.random.permutation(regionIds)
		changed_regions=[0]*target_k
		swap_iteration+=1
		index = 0
		isFirst = True
		while index < len(regionIds):
		# In each iteration of the while loop, only look at the sequentially next area for swap?
			local_swapping=True
			local_attempts=0
			seed = 0
			if isFirst:
				seed = regionID
				isFirst = False
			else:
				seed = regionIds[index]
				index = index + 1
			while local_swapping:
				local_moves=0
				# get neighbors
				members=target_regions[seed]
				neighbors=[]
				for member in members:
					candidates=neighborDict[member]
					candidates=[candidate for candidate in candidates if candidate not in members]
					candidates=[candidate for candidate in candidates if candidate not in neighbors]
					neighbors.extend(candidates)
				candidates=[]
				for neighbor in neighbors:
					block=copy.copy(target_regions[target_area2region[neighbor]])
					if check_contiguity_2(neighborDict,block,neighbor):
						fv=check_floor_Move(floor_var, floor, block, id_order)
						if fv:
							candidates.append(neighbor)
				# find the best local move 
				if not candidates:
					local_swapping=False
				else:
					nc=len(candidates)
					moves=np.zeros([nc,1],float)
					best=None
					cv=0.0
					for area in candidates:
						current_internal=target_regions[seed]
						current_outter=target_regions[target_area2region[area]]
						current=objective_function(zObj, [current_internal,current_outter], id_order)
						new_internal=copy.copy(current_internal)
						new_outter=copy.copy(current_outter)
						new_internal.append(area)
						new_outter.remove(area)
						new=objective_function(zObj, [new_internal,new_outter], id_order)
						change=new-current
						if change < cv:
							best=area
							cv=change
					if best:
						# make the move
						area=best
						old_region=target_area2region[area]
						target_regions[old_region].remove(area)
						target_area2region[area]=seed
						target_regions[seed].append(area)
						moves_made+=1
						changed_regions[seed]=1
						changed_regions[old_region]=1
					else:
						# no move improves the solution
						local_swapping=False
				local_attempts+=1
		total_moves+=moves_made
		if moves_made==0:
			swapping=False
	objVal = objective_function(zObj, target_regions, id_order)
	return target_regions, target_area2region, objVal

def initial_solution(floor_variable, floor, id_order, _neighbor, preseeds = []):
	new_p=0
	solving=True
	attempts=0
	while solving and attempts<=MAX_ATTEMPTS:
		regions=[]
		enclaves=[]
		if not preseeds:
			candidates=copy.copy(id_order)
			candidates=np.random.permutation(candidates)
			candidates=candidates.tolist()
		else:
			seeds = copy.copy(preseeds)
			nonseeds=[ i for i in id_order if i not in seeds]
			candidates=seeds
			candidates.extend(nonseeds)
		while candidates:
			seed=candidates.pop(0)
			# try to grow it till threshold constraint is satisfied
			region=[seed]
			building_region=True
			while building_region:
				# check if floor is satisfied
				if check_floor(floor_variable, floor, region, id_order):
					regions.append(region)
					building_region=False
				else:
					potential=[] 
					for area in region:
						neighbors=_neighbor[area]
						neighbors=[neigh for neigh in neighbors if neigh in candidates]
						neighbors=[neigh for neigh in neighbors if neigh not in region]
						neighbors=[neigh for neigh in neighbors if neigh not in potential]
						potential.extend(neighbors)
					if potential:
						# add a random neighbor
						neigID=random.randint(0,len(potential)-1)
						neigAdd=potential.pop(neigID)
						region.append(neigAdd)
						# remove it from candidates
						candidates.remove(neigAdd)
					else:
						#print 'enclave'
						#print region
						enclaves.extend(region)
						building_region=False
		# check to see if any regions were made before going to enclave stage
		if regions:
			feasible=True
		else:
			attempts+=1
			break
		# new_enclaves=enclaves[:]
		a2r={}
		for r,region in enumerate(regions):
			for area in region:
				a2r[area]=r
		encCount=len(enclaves)
		encAttempts=0
		while enclaves and encAttempts!=encCount:
			enclave=enclaves.pop(0)
			neighbors=_neighbor[enclave]
			neighbors=[neighbor for neighbor in neighbors if neighbor not in enclaves]
			candidates=[]
			for neighbor in neighbors:
				region=a2r[neighbor]
				if region not in candidates:
					candidates.append(region)
			if candidates:
				# add enclave to random region
				regID=random.randint(0,len(candidates)-1)
				rid=candidates[regID]
				regions[rid].append(enclave)
				a2r[enclave]=rid
				# structure to loop over enclaves until no more joining is possible
				encCount=len(enclaves)
				encAttempts=0
				feasible=True
			else:
				# put back on que, no contiguous regions yet
				enclaves.append(enclave)
				encAttempts+=1
				feasible=False
		if feasible:
			solving=False
			new_regions=regions
			new_area2region=a2r
			new_p=len(regions)
		else:
			if attempts==MAX_ATTEMPTS:
				print 'No initial solution found'
				new_p=0
			attempts+=1
	return new_regions, new_area2region, new_p

def check_floor(floor_variable, floor, region, id_order):        
	selectionIDs = [id_order.index(i) for i in region]
	cv=sum(floor_variable[selectionIDs])
	if cv >= floor:
		return True
	else:
		return False

def check_floor_Move(floor_variable, floor, region, id_order):                
	selectionIDs = [id_order.index(i) for i in region]
	cv=sum(floor_variable[selectionIDs])
	if cv > floor:
		return True
	else:
		return False

def objective_function(z, solution, id_order):
	# solution is a list of lists of region ids [[1,7,2],[0,4,3],...] such
	# that the first region has areas 1,7,2 the second region 0,4,3 and so
	# on. solution does not have to be exhaustive
	wss=0
	for region in solution:
		selectionIDs = [id_order.index(i) for i in region]
		m=z[selectionIDs,:]
		var=m.var(axis=0)
		wss+=sum(np.transpose(var))*len(region)
	return wss

def pickBest(argu):
	curval = argu[0]
	initial = argu[1]
	z = argu[2]
	floor = argu[3]
	floor_var = argu[4]
	id_orders = argu[5]
	neighbor = argu[6]
	initial_wss=[]
	attempts=0
	best_p = 0
	for i in range(initial):
		tmp_regions, tmp_area2region, p = initial_solution(floor_var, floor, id_orders, neighbor)
		if p:
			val = objective_function(z, tmp_regions, id_orders)
			initial_wss.append(val)
			if val < curval:
				current_regions=copy.copy(tmp_regions)
				current_area2region=copy.copy(tmp_area2region)
				curval=val
				best_p = p
			attempts += 1
	return current_regions, current_area2region, curval, initial_wss, best_p

if __name__ == '__main__':
    
    import random
    import numpy as np
    random.seed(100)
    np.random.seed(100)
    w=pysal.lat2W(20,20)
    z=np.random.random_sample((w.n,2))
    p=np.random.random(w.n)*100
    p=np.ones((w.n,1),float)
    floor=3
    solution=Maxp(w,z,floor,floor_variable=p,initial=100)
    # time0 = time.clock()
    # solution.swap()
    # time1 = time.clock()
    # print solution.p
    # print solution.objective_function()
    # print "This swap took ", time1 - time0
    time2 = time.clock()
    numProcess = solution.p
    
    _id_order = w.id_order
    _neighborDict = dict(w.neighbors)
    
    arguments = []
    for i in range(numProcess):
        arguments.append([i, copy.copy(solution.regions), copy.copy(solution.area2region),
                            p, floor, _id_order, _neighborDict, z])
    time3 = time.clock()
    print "The preparation for parallel Swap took %.3f seconds" % (time3 - time2)
    
    time0 = time.clock()
    swapPool = mp.Pool(processes = numProcess)
    results = swapPool.map(swap, arguments)
    swapPool.close()
                
    winVal = 100000
    winNum = 0
    for i in range(len(results)):
        if results[i][2] < winVal:
            winVal = results[i][2]
            winNum = i
                
    solution.regions = results[winNum][0]
    solution.area2region = results[winNum][1]
                
    time1 = time.clock()
    print "The parallel Swap took %.3f seconds" % (time1 - time0)
    print winVal
    for i in results:
        print i[2]
