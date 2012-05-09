'''
Created on Oct 13, 2010

@author: Xing Kang

Global Max p regionalization

Heuristically form the maximum number (p) of regions given a set of n areas and a floor
constraint. Use Global search approach.
'''

import pysal
from components import check_contiguity
from pysal.common import *
from pysal.region import randomregion as RR
import multiprocessing as mp
import pyopencl as cl

LARGE=10**6
MAX_ATTEMPTS=100

class GlobalMaxp:
    
	def __init__(self,w,z,floor,floor_variable,
				verbose=False,initial=100,seeds=[]):

		self.w=w
		self.z=z
		self.floor=floor
		self.floor_variable=floor_variable
		self.verbose=verbose
		self.seeds=seeds
		# gc.enable()
		# possible improvement of Maxp on a global perspective
		# should be organized as a function?
		
		# this block is to generate very first solution,
		# and get first mapping of area 2 region.
		# based on this we can possibly make some improvements.

		self.initial_solution()
		if not self.p:
			self.feasible = False
		else:
			self.feasible = True
			self.current_regions = copy.copy(self.regions)
			self.current_area2region = copy.copy(self.area2region)
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
			
			time3 = time.clock()
			print "The parallel part took %.3f seconds" % (time3 - time2)
			print winVal
			# print len(results)
			# print results
			"""
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
			"""

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

	def globalSwap(self):
		# this block is to generate the matrix,
		# indicating possible move on every area and the changes in obj func
		# before and after the move
			
		# first we need to initialize the matrix
		curval = self.objective_function()
		w = self.w
		possiblemoveMatrix = [0]*w.n
		for i in range(w.n):
			possiblemoveMatrix[i] = [0]*4
			
		# then generate this matrix at very beginning
		for i in range(len(self.regions)):
			for j in self.regions[i]:
				for count, k in enumerate(w.neighbors[j]):
					# if center area differs in region with its current neighbor
					if(self.area2region[k] != self.area2region[j]):
					#   self.current_regions = copy.deepcopy(self.regions)
					#   self.current_regions[i].remove(j)
					#   self.current_regions[self.area2region[k]].append(j)
						# save the previous region that area j(center area) is in
						preReg = self.area2region[j]
						aftReg = self.area2region[k]
						current_internal=self.regions[self.area2region[j]]
						current_outter=self.regions[self.area2region[k]]
						current=self.objective_function([current_internal,current_outter])
						new_internal=copy.copy(current_internal)
						new_outter=copy.copy(current_outter)
						new_internal.remove(j)
						new_outter.append(j)
						new=self.objective_function([new_internal,new_outter])
						# calculate the obj func value after the possible move
						# afterval = self.objective_function(self.current_regions)
						afterval = curval + new - current
						# add the structure containing current possible move
						possiblemoveMatrix[j][count] = [j, k, preReg, aftReg, curval, afterval]
			
			
		# mainloop to check if there is a global best move that could
		# improve the obj func, until no improved move could be found
			
		isGlobalMoveExist = True
			
		# record location and value of possible best move
		currentArea = -1
		currentItemIdx = -1
		currentObjVal = curval
			
		while isGlobalMoveExist:
			isGlobalMoveExist = False
			moveCandidates = []
				
			for i in range(len(possiblemoveMatrix)):
				for j in range(len(possiblemoveMatrix[i])):
					if not possiblemoveMatrix[i][j] == 0:
						objValAfter = possiblemoveMatrix[i][j][5]
						if objValAfter < currentObjVal:
							preRegionIdx = possiblemoveMatrix[i][j][2]
							leaver = possiblemoveMatrix[i][j][0]
							if self.check_floor_Move(self.regions[preRegionIdx]):
								currentObjVal = objValAfter
								currentArea = i
								currentItemIdx = j
								isGlobalMoveExist = True
								moveCandidates.append([preRegionIdx, leaver])
			
			# make the move after finding a global best move
			while len(moveCandidates) > 0:
				if isGlobalMoveExist:
					curMoveCandidate = moveCandidates.pop()
					block = copy.copy(self.regions[curMoveCandidate[0]])
					if check_contiguity(self.w, block, curMoveCandidate[1]):  
						pre_Region = possiblemoveMatrix[currentArea][currentItemIdx][2]
						aft_Region = possiblemoveMatrix[currentArea][currentItemIdx][3]
						self.regions[pre_Region].remove(currentArea)
						self.regions[aft_Region].append(currentArea)
						self.area2region[currentArea] = aft_Region
						# delete the item in possible move matrix
						possiblemoveMatrix[currentArea][currentItemIdx] = 0
								
						# important!!! First major bug occurs here
						# after deleting best move, have to make adjustment to every possible move in it
						# change the third element from pre_Region to aft_Region
						for i in possiblemoveMatrix[currentArea]:
							if not i == 0:
								i[2] = aft_Region
						# change all the previous obj func value to currentObjVal,
						# in possiblemoveMatrix
						for i in possiblemoveMatrix:
							for j in i:
								if not j == 0:
									j[4] = currentObjVal
						
						# make adjustments to neighbors of currentArea
						# restrictions seem not enough here
						for i in w.neighbors[currentArea]:
							possiblemoves = possiblemoveMatrix[i]
							neighborRegion = self.area2region[i]
						
						# construct a new item in possiblemoveMatrix,
						# when neighbor is within same region of pre_region.
						# the obj func value is set 0 at first and will be
						# calculated in later process
						if neighborRegion == pre_Region:
							for j in possiblemoves:
								if j == 0:
									j = [i, currentArea, pre_Region, aft_Region, currentObjVal, 0]
									break;
											
						# when neighbor is not in pre_region, two circumstances:
						# 1. neighbor is in aft_region, no reason to move to current area
						#   probably need to remove this move item
						# 2. neighbor is in third-party region, just need to change the
						#   corresponding aft_region element in the item
						#   say,  possiblemoveMatrix[neighbor][item][2] = aft_region
						else:
							for j in range(len(possiblemoves)):
								# what happens if current neighbor has multiple
								# possible moves to aft_region?
								tmpMove = possiblemoves[j]
								if not tmpMove == 0:
									if tmpMove[1] == currentArea:
										if tmpMove[2] != aft_Region:
											tmpMove[3] = aft_Region
										else:
											# is it really reasonable to remove this possible move
											possiblemoves[j] = 0
						
						# recalculate all the obj Func value after possible move,
						# based on region distribution that have changed
						for i in possiblemoveMatrix:
							for j in i:
								if not j == 0:
									preReg = j[2]
									aftReg = j[3]
									current_internal=self.regions[preReg]
									current_outter=self.regions[aftReg]
									current=self.objective_function([current_internal,current_outter])
									new_internal=copy.copy(current_internal)
									new_outter=copy.copy(current_outter)
									new_internal.remove(j[0])
									new_outter.append(j[0])
									new=self.objective_function([new_internal,new_outter])
									j[5] = j[4] + new - current
						break;

	def globalSwap_BFS(self):
		# this block is to generate the matrix,
		# indicating possible move on every area and the changes in obj func
		# before and after the move
			
		# first we need to initialize the matrix
		curval = self.objective_function()
		w = self.w
		possiblemoveMatrix = [0]*w.n
		for i in range(w.n):
			possiblemoveMatrix[i] = [0]*4
			
		# then generate this matrix at very beginning
		for i in range(len(self.regions)):
			for j in self.regions[i]:
				for count, k in enumerate(w.neighbors[j]):
					# if center area differs in region with its current neighbor
					if(self.area2region[k] != self.area2region[j]):
					#   self.current_regions = copy.deepcopy(self.regions)
					#   self.current_regions[i].remove(j)
					#   self.current_regions[self.area2region[k]].append(j)
						# save the previous region that area j(center area) is in
						preReg = self.area2region[j]
						aftReg = self.area2region[k]
						current_internal=self.regions[self.area2region[j]]
						current_outter=self.regions[self.area2region[k]]
						current=self.objective_function([current_internal,current_outter])
						new_internal=copy.copy(current_internal)
						new_outter=copy.copy(current_outter)
						new_internal.remove(j)
						new_outter.append(j)
						new=self.objective_function([new_internal,new_outter])
						# calculate the obj func value after the possible move
						# afterval = self.objective_function(self.current_regions)
						afterval = curval + new - current
						# add the structure containing current possible move
						possiblemoveMatrix[j][count] = [j, k, preReg, aftReg, curval, afterval]
			
			
		# mainloop to check if there is a global best move that could
		# improve the obj func, until no improved move could be found
			
		isGlobalMoveExist = True
			
		# record location and value of possible best move
		currentArea = -1
		currentItemIdx = -1
		currentObjVal = curval
			
		while isGlobalMoveExist:
			isGlobalMoveExist = False
			moveCandidates = []
				
			for i in range(len(possiblemoveMatrix)):
				for j in range(len(possiblemoveMatrix[i])):
					if not possiblemoveMatrix[i][j] == 0:
						objValAfter = possiblemoveMatrix[i][j][5]
						if objValAfter < currentObjVal:
							preRegionIdx = possiblemoveMatrix[i][j][2]
							leaver = possiblemoveMatrix[i][j][0]
							if self.check_floor_Move(self.regions[preRegionIdx]):
								currentObjVal = objValAfter
								currentArea = i
								currentItemIdx = j
								isGlobalMoveExist = True
								moveCandidates.append([preRegionIdx, leaver])
			
			# make the move after finding a global best move
			while len(moveCandidates) > 0:
				if isGlobalMoveExist:
					curMoveCandidate = moveCandidates.pop()
					block = copy.copy(self.regions[curMoveCandidate[0]])
					if check_contiguity_breadth(self.w, block, curMoveCandidate[1]):  
						pre_Region = possiblemoveMatrix[currentArea][currentItemIdx][2]
						aft_Region = possiblemoveMatrix[currentArea][currentItemIdx][3]
						self.regions[pre_Region].remove(currentArea)
						self.regions[aft_Region].append(currentArea)
						self.area2region[currentArea] = aft_Region
						# delete the item in possible move matrix
						possiblemoveMatrix[currentArea][currentItemIdx] = 0
								
						# important!!! First major bug occurs here
						# after deleting best move, have to make adjustment to every possible move in it
						# change the third element from pre_Region to aft_Region
						for i in possiblemoveMatrix[currentArea]:
							if not i == 0:
								i[2] = aft_Region
						# change all the previous obj func value to currentObjVal,
						# in possiblemoveMatrix
						for i in possiblemoveMatrix:
							for j in i:
								if not j == 0:
									j[4] = currentObjVal
						
						# make adjustments to neighbors of currentArea
						# restrictions seem not enough here
						for i in w.neighbors[currentArea]:
							possiblemoves = possiblemoveMatrix[i]
							neighborRegion = self.area2region[i]
						
						# construct a new item in possiblemoveMatrix,
						# when neighbor is within same region of pre_region.
						# the obj func value is set 0 at first and will be
						# calculated in later process
						if neighborRegion == pre_Region:
							for j in possiblemoves:
								if j == 0:
									j = [i, currentArea, pre_Region, aft_Region, currentObjVal, 0]
									break;
											
						# when neighbor is not in pre_region, two circumstances:
						# 1. neighbor is in aft_region, no reason to move to current area
						#   probably need to remove this move item
						# 2. neighbor is in third-party region, just need to change the
						#   corresponding aft_region element in the item
						#   say,  possiblemoveMatrix[neighbor][item][2] = aft_region
						else:
							for j in range(len(possiblemoves)):
								# what happens if current neighbor has multiple
								# possible moves to aft_region?
								tmpMove = possiblemoves[j]
								if not tmpMove == 0:
									if tmpMove[1] == currentArea:
										if tmpMove[2] != aft_Region:
											tmpMove[3] = aft_Region
										else:
											# is it really reasonable to remove this possible move
											possiblemoves[j] = 0
						
						# recalculate all the obj Func value after possible move,
						# based on region distribution that have changed
						for i in possiblemoveMatrix:
							for j in i:
								if not j == 0:
									preReg = j[2]
									aftReg = j[3]
									current_internal=self.regions[preReg]
									current_outter=self.regions[aftReg]
									current=self.objective_function([current_internal,current_outter])
									new_internal=copy.copy(current_internal)
									new_outter=copy.copy(current_outter)
									new_internal.remove(j[0])
									new_outter.append(j[0])
									new=self.objective_function([new_internal,new_outter])
									j[5] = j[4] + new - current
						break;

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
		return self.regions, self.area2region, self.objective_function(), self.p, self.verbose

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
            for i in range(initial):
                tmp_regions, tmp_area2region, p = initial_solution(floor_var, floor, id_orders, neighbor)
                if p:
                    val = objective_function(z, tmp_regions, id_orders)
                    initial_wss.append(val)
                    if val < curval:
                        current_regions=copy.copy(tmp_regions)
                        current_area2region=copy.copy(tmp_area2region)
                        curval=val
                    attempts += 1
            return current_regions, current_area2region, curval, initial_wss

if __name__ == '__main__':
    
    import random
    import numpy as np
    import time
    
    random.seed(100)
    np.random.seed(100)
    w=pysal.lat2W(30,30)
    z=np.random.random_sample((w.n,2))
    p=np.random.random(w.n)*100
    p=np.ones((w.n,1),float)
    floor=3
    solution=GlobalMaxp(w,z,floor,floor_variable=p,initial=100)
    time0 = time.clock()
    solution.globalSwap()
    time1 = time.clock()
    print solution.p
    print solution.objective_function()
    print solution.regions[0]
    print "This globalSwap took ", time1 - time0
