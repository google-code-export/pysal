import math, sys, time
import pp

def isprime(n):
    """Returns True if n is prime and False otherwise"""
    if not isinstance(n, int):
        raise TypeError("argument passed to is_prime is not of 'int' type")
    if n < 2:
        return False
    if n == 2:
        return True
    max = int(math.ceil(math.sqrt(n)))
    i = 2
    while i <= max:
        if n % i == 0:
            return False
        i += 1
    return True

def sum_primes(n):
    """Calculates sum of all primes below given integer n"""
    return sum([x for x in xrange(2,n) if isprime(x)])

print """Usage: python sum_primes.py [ncpus]
    [ncpus] - the number of workers to run in parallel, 
    if omitted it will be set to the number of processors in the system
"""
"""
# tuple of all parallel python servers to connect with
ppservers = ()
#ppservers = ("10.0.0.1",)

if len(sys.argv) > 1:
    ncpus = int(sys.argv[1])
    # Creates jobserver with ncpus workers
    job_server = pp.Server(ncpus, ppservers=ppservers)
else:
    # Creates jobserver with automatically detected number of workers
    job_server = pp.Server(ppservers=ppservers)

print "Starting pp with", job_server.get_ncpus(), "workers"

# Submit a job of calulating sum_primes(100) for execution. 
# sum_primes - the function
# (100,) - tuple with arguments for sum_primes
# (isprime,) - tuple with functions on which function sum_primes depends
# ("math",) - tuple with module names which must be imported before sum_primes execution
# Execution starts as soon as one of the workers will become available
job1 = job_server.submit(sum_primes, (100,), (isprime,), ("math",))

# Retrieves the result calculated by job1
# The value of job1() is the same as sum_primes(100)
# If the job has not been finished yet, execution will wait here until result is available
result = job1()

print "Sum of primes below 100 is", result

start_time = time.time()

# The following submits 8 jobs and then retrieves the results
inumpyuts = (100000, 100100, 100200, 100300, 100400, 100500, 100600, 100700)
jobs = [(inumpyut, job_server.submit(sum_primes,(inumpyut,), (isprime,), ("math",))) for inumpyut in inumpyuts]
for inumpyut, job in jobs:
    print "Sum of primes below", inumpyut, "is", job()

print "Time elapsed: ", time.time() - start_time, "s"
job_server.print_stats()
"""


import pysal as ps
import numpy 


n = 5000
coords = numpy.random.randint(0, 100, (n,2))
dmat = numpy.zeros((n,n))

def d_mat(coords, position, ncols):
    start,end = position
    nr = end-start
    mat = numpy.zeros((nr,ncols))
    for r,i in enumerate(range(start,end)):
        x1 = coords[i,0]
        y1 = coords[i,1]
        for j in range(ncols):
            x2 = coords[j,0]
            y2 = coords[j,1]
            mat[r,j] = (x1-x2)*(x1-x2) + (y2-y1)*(y2-y1)
    return mat

ppservers = ()
job_server = pp.Server(ppservers=ppservers)

ncpu = job_server.get_ncpus()
step = n / ncpu
start = range(0, n, step)
end = start[1:]
end.append(n)
positions = zip(start,end)

t1 = time.time()
mat0 = d_mat(coords, (0,n), n)
t2 = time.time()
seq0time = t2 - t1
print seq0time

mats = {}
t1 = time.time()
m1 = numpy.zeros((n,n))
for position in positions:
    start,end = position
    mats[position] = d_mat(coords, position, n)
    m1[start:end,:] = mats[position]
t2 = time.time()
seqtime = t2 - t1

print seqtime
t1 = time.time()
jobs = []
m2 = numpy.zeros((n,n))
for position in positions:
    start,end = position
    jobs.append( (position,job_server.submit(d_mat, (coords, position, n,), (), ("numpy",))) )
for position,job in jobs:
    start,end = position
    m2[start:end,:] = job()
ptime= time.time()-t1
print "seq0: ", seq0time
print "seq: ", seqtime
print "pp: ", ptime
job_server.print_stats()
