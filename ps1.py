###########################
# 6.00.2x Problem Set 1: Space Cows


from collections import namedtuple, deque
import random
from ps1_partition import*
#================================
# Part A: Transporting Space Cows
#================================

def load_cows(filename):

    cow_dict = dict()

    f = open(filename, 'r')

    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])

    return cow_dict



# Problem 1
Cow = namedtuple("Cow", "weight name")


def greedy_recur_cycle(sorted_cows, limit):
    '''Inputs,
     sorted_cows: a deque of sorted Cow objects
        limit: an int
    Yields list of cows in each trip'''
    if sorted_cows:
        cow, *other = sorted_cows
        sorted_cows.popleft()
        trip = [cow] # use .name in cow for adding only the names
        weight = cow.weight
        for cow in other:
            if cow.weight + weight <= limit:
                trip.append(cow) # use .name
                sorted_cows.remove(cow)
                weight += cow.weight
        yield trip
        yield from greedy_recur_cycle(sorted_cows, limit)




def greedy_cow_transport(cows,limit=10):
    """
    Uses a greedy heuristic to determine an allocation of cows that attempts to
    minimize the number of spaceship trips needed to transport all the cows. The
    returned allocation of cows may or may not be optimal.
    The greedy heuristic should follow the following method:

    1. As long as the current trip can fit another cow, add the largest cow that will fit
        to the trip
    2. Once the trip is full, begin a new trip to transport the remaining cows

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """
    sorted_cows = deque(sorted([Cow(weight, name) for name, weight in cows.items()], reverse = True))
    return list(greedy_recur_cycle(sorted_cows, limit))



# Problem 2
def brute_force_cow_transport(cows,limit):
    """
    Finds the allocation of cows that minimizes the number of spaceship trips
    via brute force.  The brute force algorithm should follow the following method:

    1. Enumerate all possible ways that the cows can be divided into separate trips
    2. Select the allocation that minimizes the number of trips without making any trip
        that does not obey the weight limitation

    Does not mutate the given dictionary of cows.

    Parameters:
    cows - a dictionary of name (string), weight (int) pairs
    limit - weight limit of the spaceship (an int)

    Returns:
    A list of lists, with each inner list containing the names of cows
    transported on a particular trip and the overall list containing all the
    trips
    """

    object_cows = [Cow(weight, name) for name, weight in cows.items()]
    winner = None
    for trip in get_partitions(object_cows):
        weights = [sum([cow.weight for cow in item]) for item in trip]
        if any(weight > limit for weight in weights):
            pass
        elif winner == None or len(trip) < len(winner):
            winner = [[cow for cow in item] for item in trip] # use cow.name for getting only the names

    return winner



def fast_non_brute_force(cows,limit):
    '''Uses greedy_recur_cycle to test for best possibility
    rotating sorted cows len(sorted_cows) - 1 times'''

    object_cows = sorted([Cow(weight, name) for name, weight in cows.items()], reverse = True)
    winner = None
    for i in range(len(object_cows)):
        sorted_cows = deque(object_cows)
        sorted_cows.rotate(-i)
        current = list(greedy_recur_cycle(sorted_cows, limit))

        if winner == None or len(winner) > len(current):
            winner = current

    return winner


# Problem 3
from time import perf_counter
from tabulate import tabulate
from statistics import mean


def time_it(f, cows, limit):
    '''Times a function 10 times, returns the average time'''
    times = []
    for i in range(5):
        start_time = perf_counter()
        f(cows, limit)
        elapsed_time = perf_counter() - start_time
        times.append(elapsed_time)
    return mean(times)

def compare_cow_transport_algorithms():
    '''prints the time it took for each algorithms to complete using
        the dictionary provided by the course,
    prints the trips for each algorithm in table format'''

    cows = load_cows("ps1_cow_data.txt")

    print ("\n", cows)
    limit = 10
    for algo in [greedy_cow_transport, brute_force_cow_transport,fast_non_brute_force]:

            itinerary = algo(cows, limit)
            a_time = time_it(algo, cows, limit)
            time_data = [["Algorithm", "Average time in seconds"],[algo.__name__, a_time]]
            print ("\n")
            print (tabulate(time_data, headers='firstrow'))
            trip_data = [["Trip"]] + [[trip] for trip in itinerary]
            print (tabulate(trip_data, headers='firstrow', showindex='always', tablefmt='fancy_grid' ))


# tests
from collections import defaultdict

def create_random_test(limit, lengh):
    '''yields 10 random dicts for testing'''
    for i in range(10):
        cows = {"Cow"+str(i): random.randrange(1, limit) for i in range(lengh)}
        yield cows


def tests(limit, test_scope):
    '''runs 10 different tests for dicts of lengh 1 to test scope
        times each function, raises error if results from brute_force and non_brute_force differ
    returns defaultdict containing algorithm names and list of times'''

    algos = [greedy_cow_transport, brute_force_cow_transport,fast_non_brute_force]
    result = defaultdict(list)
    print (f"\nRunning random tests in scope: 1 - {test_scope - 1}. Please be patient...\n")
    for i in range(1,test_scope):
        times = defaultdict(set)
        for cows in create_random_test(limit, i):
            lenghts = set()
            for algo in algos:
                time = time_it(algo, cows, limit)
                if algo in [brute_force_cow_transport,fast_non_brute_force]:
                    lenghts.add(len(algo(cows, limit)))
                times[algo.__name__].add(time)
            if len(lenghts) > 1:
                raise Exception("TEST FAILED FOR COWS: ", cows)
        for time in times:
            result[time].append(mean(times[time]))
    return result


def represent_it(limit, test_scope):
    '''Represents the time results of tests
        in table format
    '''
    num_cows = list(range(1, test_scope))
    result = tests(limit, test_scope)
    head = ["Num Cows"] + [key+" (s)" for key in result.keys()]
    rows = []
    for i in range(len(num_cows)):
        row = [num_cows[i]] + [result[algo][i] for algo in result]
        rows.append(row)
    print (tabulate(rows, headers= head, tablefmt="fancy_grid"))
















if __name__ == "__main__":
    compare_cow_transport_algorithms()
    represent_it(10, 11)
