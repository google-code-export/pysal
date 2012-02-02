Next steps


Next steps


## Coding
 - implement other version of fisher (done)
 - implement our own version of fisher (done)
	 - using numpy arrays  seems to be expensive time wise
	 - implementation decomposes the calculation of the variance and the indexing of the optimal subsets
	 - need to see if moving to lists with the decomposition gets us back to speed of the original implementation
	 - requires nxn variance matrix so not applicable for large n cases
	 - we could still compare for smaller n
 - parallelize our version
 	- cl (done)
	- multiprocessing 
	- after mp, see where we are
 - random sampling version (maybe put on hold)
 - parallelize random sampling version (put on hold)

 - idea for algorithm
	 - if n < NLARGE
		 - parallelized decompositional approach
	 - else
		 - parallelized random sample of nondecomposed approach
 
## Experiment
 - design experiment for comparison
 - small n
	 - compare sampling approach to brute force for accuracy tradeoff
 - large n
	 - time comparisons across the above implementations
	 
## Presentation

 - brainstorm presentation
 - 15 minutes max

 
## Paper
  
  - Introduction
	  - Problem statement
	  - Organization
  - Components
	  - PySAL
	  - Parallelizationterminal
	  - 
  - Fisher-Jenks
	  - Alternative implementations
  - Illustration
	  - Random sampling experiment
	  - Efficiency comparisons
  - Conclusion
