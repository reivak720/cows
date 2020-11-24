###########################
# 6.00.2x Problem Set 1: Space Cows


#author @reivaJ
from collections import deque
from time import perf_counter
from tabulate import tabulate
import random

#From codereview.stackexchange.com
def partitions(set_):
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:
            parts[i&1].add(item)
            i >>= 1
        for b in partitions(parts[1]):
            yield [parts[0]]+b


# This is a helper function that will fetch all of the available
# partitions for you to use for your brute force algorithm.
def get_partitions(set_):
    for partition in partitions(set_):
        yield [list(elt) for elt in partition]


# this is an improvement of partitions function designed specifically for this exercesise
# takes advantage of memoization
# this was not required by the exercise but the key was given in lectures
# using memoization to improve recursive fibbonacci

def optimizedPartitions(set_, limit,  memo = []):
    '''
    Parameters
    set: a list of tuples containing (cow.weight, cow.name)
    limit: type int, maximimum load capacity of spaceship
    memo: a list for noGo partitions
    yields partitions in limit scope
    '''
    if not set_:
        yield []
        return
    for i in range(2**len(set_)//2):
        parts = [set(), set()]
        for item in set_:        
            parts[i&1].add(item)
            i >>= 1       
        if parts[0] in memo:
            continue
        elif  sum([part[0] for part in parts[0]]) > limit:
            memo.append(parts[0])
            continue

        for b in optimizedPartitions(parts[1], limit):            
            yield [parts[0]]+b

# and this is it's helper function
def getOptimizedPartitions(set_, limit, winner = None):
    '''
    Parameters:
    set_: a list containing tuples(cow.weight, cow.name)
    limit: type int: maximum load capacity of spaceshift  
    returns the shortest correct answer from optimizedPartitions
    '''
   
    for partition in optimizedPartitions(set_, limit):        
        if winner == None or len(partition)< len(winner):
            winner = partition
        
    return [[cow[1] for cow in trip] for trip in winner]


def greedy_recur_cycle(sorted_cows, limit):
    '''
    Parameters:
     sorted_cows: a deque of sorted cows tuples (weight, name)
        limit: type int
    Yields list of cow names in each trip
    '''
    if sorted_cows:
        cow, *other = sorted_cows   
        sorted_cows.popleft()
        trip = [cow[1]] 
        weight = cow[0]
        for c in other:
            if c[0] + weight <= limit:
                trip.append(c[1]) 
                sorted_cows.remove(c)
                weight += c[0]   
        yield trip        
        yield from greedy_recur_cycle(sorted_cows, limit)




class cowTransAlgos(object):

    def load_cows(self, filename, limit):
        '''
        Parameters:
        filename: a path to a file name containing cows names and weights
        limit: type int, the maximum load capacity of the spaceship
        loads cows from file and creates a dictionary
        '''
        cow_dict = dict()
        with open(filename, 'r') as f:
            for line in f:
                line_data = line.split(',')
                cow_dict[line_data[0]] = int(line_data[1])
        self.cows =  cow_dict
        self.limit = limit


    def create_random_test(self, limit, lengh):
        '''
        Parameters:
        limit: type int, maximum load capacity of spaceship
        lengh: type int, lengh of desired cow dict
        creates a random cow dict
        '''
        cows = {"Cow_"+str(i): random.randrange(1, limit) for i in range(lengh)}
        self.cows = cows
        self.limit = limit

    def getParams(self):
        return self.cows, self.limit

    def greedyCowTransport(self):
        """     
        Uses a greedy heuristic to determine an allocation of cows that attempts to
        minimize the number of spaceship trips needed to transport all the cows. The
        returned allocation of cows may or may not be optimal.
        Returns:
        A list of lists, with each inner list containing the names of cows
        transported on a particular trip and the overall list containing all the
        trips
        """
        sorted_cows = sorted(zip(self.cows.values(), self.cows.keys()), reverse =True)
        schedule = []
        while sorted_cows:
            cow = sorted_cows[0]
            trip, weight= [cow[1]], cow[0]
            sorted_cows.remove(cow)

            for cow in sorted_cows.copy():
                if cow[0]+ weight <= self.limit:
                    trip.append(cow[1])
                    sorted_cows.remove(cow)
                    weight += cow[0]
            schedule.append(trip)
        return schedule

    def brute_force_cow_transport(self):
        """
        Uses bit shift partitions function
        Parameters:
        cows - a dictionary of name (string), weight (int) pairs
        limit - weight limit of the spaceship (an int)

        Returns:
        A list of lists, with each inner list containing the names of cows
        transported on a particular trip and the overall list containing all the
        trips
        """

        object_cows = list(zip(self.cows.values(), self.cows.keys()))
        winner = None
        for trip in get_partitions(object_cows):
            weights = [sum([cow[0] for cow in item]) for item in trip]
            if  any(weight > self.limit for weight in weights) or (winner != None and len(trip)>= len(winner)):
                pass
            else:
                winner = trip        
        return [[cow[1] for cow in item] for item in winner]


    def optimizedBrute(self):
        '''
        improved brute force with memoization using optimizedPartitions function
        '''
        object_cows = list(zip(self.cows.values(), self.cows.keys()))        
        return  getOptimizedPartitions(object_cows, self.limit)


    def recursiveGreed(self):
        """
        Improves greedy heuristic for finding (in many ocations) an optimal result
        """
        object_cows =sorted(zip(self.cows.values(), self.cows.keys()), reverse =True)

        winner = None
        for i in range(len(object_cows)):
            sorted_cows = deque(object_cows)
            sorted_cows.rotate(-i)
            current = list(greedy_recur_cycle(sorted_cows, self.limit))

            if winner == None or len(winner) > len(current):
                winner = current
        return winner


    def time_it(self, f, n):
        '''
        Times a function(f) n times, returns the mean
        '''
        times = 0
        for i in range(n):
            start_time = perf_counter()
            f()
            times += perf_counter() - start_time        
        return times/n

    def compareResults(self):
        '''
        prints the results given by all four algorithms in table format
        does not return anything
        '''       
        print ("Passengers:\n", self.cows, "\n", "Max Load Limit: ", self.limit, "\n")
        name_res = [["Algorithm", "Itinerary", "Length"]]
        for algo in (self.greedyCowTransport, self.brute_force_cow_transport, self.optimizedBrute, self.recursiveGreed):
            result = algo()
            name_res.append([algo.__name__, result, len(result)])
        print (tabulate(name_res, headers='firstrow', tablefmt='fancy_grid' ), "\n")


    def compareTimes(self):
        '''
        prints a comparison of the times it takes to complete each algorithm
        times a function 10 times
        returns nothing
        '''
        print ("Timing algorithms for passengers:\n", self.cows, "\n")
        time_res = [["Algorithm", "Time(s)"]]
        for algo in (self.greedyCowTransport, self.brute_force_cow_transport, self.optimizedBrute, self.recursiveGreed):
            time_res.append([algo.__name__, self.time_it(algo, 10)])        
        print (tabulate(time_res, headers='firstrow'), "\n")

    def getWeights(self,f):
        '''
        returns the weight for each trip given by a cow_transport function
        '''
        weights = []
        for trip in f():
            w = [self.cows[cow] for cow in trip]
            weights.append(sum(w))
        return weights


if __name__=="__main__":
    space = cowTransAlgos()
    space.load_cows("ps1_cow_data.txt", 10)
    space.compareTimes()
    space.compareResults()
