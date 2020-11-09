''' a slight modification of Kiwi's speed tester
 times greedy
  and prints the result for each students code'''

import random
import string
from timeit import timeit
from collections import namedtuple, deque
Cow = namedtuple("Cow", "weight name")


# students code
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




def jam(cows,limit=10):

    sorted_cows = deque(sorted([Cow(weight, name) for name, weight in cows.items()], reverse = True))
    return list(greedy_recur_cycle(sorted_cows, limit))

def jason_bc(cows,limit):
    avail=limit
    items=cows.copy()
    import operator
    toConsider = list(sorted(items.items(), key=operator.itemgetter(1),reverse=True))
    copy=toConsider.copy()
    v=[]
    record=[]
    def f(toConsider,copy,avail,v,record):
        def maxVal(toConsider, avail,v):
            if not toConsider:
                return v
            if len(toConsider)==1:
                if toConsider[0][1] <= avail:
                    v.append(toConsider[0])
                    return maxVal(toConsider[1:],avail,v)
            if (toConsider[0][1] > avail)and(len(toConsider)>0):
                return maxVal(toConsider[1:], avail,v)
            if toConsider[0][1] <= avail:
                v.append(toConsider[0])
                if len(toConsider)>1:
                    return maxVal(toConsider[1:], avail-toConsider[0][1],v)
        for i in maxVal(toConsider, avail,v):
            record.append(i)
        diff=set(copy)-set(record)
        toConsider=[item for item in copy if item in diff]
        if diff==set():
            return maxVal(toConsider, avail,v)
        else:
            return f(toConsider,copy,avail,v,record)

    ans=f(toConsider,copy,avail,v,record)
    s=[i[1] for i in ans]
    v=[i[0] for i in ans]

    t=s.copy()
    x=[]
    R=[]
    def func(t):
        L=[]
        for i in range(1,len(t)+1):
            if sum(t[:i])<=avail:
                L.append(t[i-1])
        return L

    while True:
        w=func(t)
        R.append(w)
        t=s[len([item for items in R for item in items]):]
        if len([item for items in R for item in items]) == len(s):
            break
    A=[]
    for t in R:
        A.append(len(t))

    for i in range(len(A)):

        x.append(v[sum(A[0:i]):sum(A[0:i+1])])
    return x


def richard_uk(cows, limit=10):

    cowsLeft = cows.copy()                   # so I can mutate dict

    # helper function to choose next cow

    def next_cow(cowsLeft, limit):
        '''
        :param cowsLeft: dict of earthbound cows
        :param limit: weight capacity remaining on ship
        :return: name: string, name of cow, or "" if none will fit
        '''
        if len(cowsLeft) == 0:
            return ""
        trialSet = set(cowsLeft.values())
        trialList = sorted(list(trialSet))   # list of unique weights in asc order
        while len(trialList) > 0:
            trial = trialList.pop()          # heaviest left
            if trial <= limit:
                L = [k for k, v in cowsLeft.items() if v == trial]
                if L != []:                  # list of cows of that weight
                    return L[0]              # doesn't matter which one
        return ""

    schedule = []
    while len(cowsLeft) > 0:
        ship = []
        spare = limit                       # room left on ship, starts as limit
        while spare >= min(cowsLeft.values()):
            next = next_cow(cowsLeft, spare)
            if next == "":
                schedule.append(ship)       # no room on this ship
                break
            ship.append(next)               # add max cow and continue
            spare -= cowsLeft[next]         # try to fit another
            del cowsLeft[next]              # remove cow from earthbound dict
            if len(cowsLeft) == 0 or spare < min(cowsLeft.values()):
                schedule.append(ship)       # no room or no cows
                break
    return schedule


def greedy_cow_transport1(cows,limit=10):

    result = []
    totalweight = 0
    itemcopy = sorted([c for c in cows.items()], key=lambda x: x[1], reverse=True)

    for k,v in itemcopy:
        if totalweight + v <= limit:
            result.append(k)
            totalweight += v

    return result

def mariko_ueno(cows,limit=10):

    cowscopy = cows.copy()
    result=[]
    while len(cowscopy) > 0:
        r = greedy_cow_transport1(cowscopy, limit)
        result.append(r)
        for c in r:
            del cowscopy[c]
    return result

# Renata
def largestcow(cows):
    """
    Parameters:
    cows - a dictionary of name (string), weight (int) pairs

    Returns:
    Pop the largest cow and returns its name
    """
    largest=max(cows.values())
    for name, weight in cows.items():
        if weight==largest:
            onboard=name
            return cows.pop(name), onboard


def renata_kb(cows,limit=10):
    crew=cows.copy()
    travel=[]
    while crew:
        trip=[]
        tripwgt, firstcow = largestcow(crew)
        trip.append(firstcow)
        left=crew.copy()
        while left:
            newwgt, newcow = largestcow(left)
            if tripwgt+newwgt<=limit:
               tripwgt+=crew.pop(newcow)
               trip.append(newcow)
            if tripwgt==limit:
                break
        travel.append(trip)
    return travel


# Finfate bee
def finfate(cows,limit=10):
    cowsCopy = sorted(cows.items(), key=lambda d: d[1], reverse=True)

    limit_left=limit
    ship = []

    transport=[]

    while 0 < len(cowsCopy):
        i=0
        while i < len(cowsCopy):
            if cowsCopy[i][1]<=limit_left:
                ship.append(cowsCopy[i][0])
                limit_left=limit_left-cowsCopy[i][1]
                cowsCopy=cowsCopy[:i]+cowsCopy[i+1:]
                #because I delete cowCopy[i] then cowCopy[i+1] take this place, so I don't need to increase the value of i.
            else:
                i=i+1

        if i==len(cowsCopy) or 0==len(cowsCopy):
            limit_left=limit
            transport.append(ship)
            ship=[]

    return transport

# richwilliams
def richwill(cows,limit=10):
    # Make a list of the cows with the heaviest first
    cow_list = list(cows.items())
    cow_list.sort(key= lambda x:x[1], reverse= True)

    # Make a list to hold the cows shipped
    cows_shipped = []

    # Keep filling up ships until no more shippable cows
    while(True):
        this_trip = []                          # Cows in this trip
        weight_left = limit                     # How much left to fill
        for cow in cow_list.copy():             # Add cows until full
            if cow[1] <= weight_left:           # Does it fit?
                this_trip.append(cow[0])        # Add name to trip
                cow_list.remove(cow)            # Remove it from cows to check
                weight_left -= cow[1]           # Subtract the weight
                if weight_left <= 0:            # Break if trip is full
                    break

        # Finished loading cows for this trip
        # If list empty, no more cows or all too big and we're done
        if len(this_trip) == 0:
            break

        # Add trip to shiiped list loop for next trip
        cows_shipped.append(this_trip)

    # We're done
    return(cows_shipped)



def natasha_c(cows,limit=10):

    newcows =cows.copy()
    trip= result =[]
    weight =limit
    checkcows= sorted(newcows.items(), key= lambda x:x[1] , reverse = True)

    if len(checkcows) == 0:
        return trip

    #start trip if there is space & cows to transport
    for i,(x,y) in enumerate(checkcows):
        if y <= limit:
            trip.append(x)
            limit -= y

    #stop trip as no more cows can fit even if there is space
    #check if there are cows remaining, if so, start next trip
    if len(newcows) != 0:
        for cow in list(newcows.keys()):
            if cow in trip:
                newcows.pop(cow)
        result = ([trip] + natasha_c(newcows,limit=weight))
    return result



def colling(cows,limit=10):

    cowsCopy = sorted(cows.copy().items(), key=lambda x: x[1], reverse = True)
    totalCargo = []

    while len(cowsCopy) > 0: # While cows are in queue
        cargo = []
        weight = 0
        check = []
        for i in range(len(cowsCopy)):
            if weight + cowsCopy[i][1] <= limit: # If weight of cows + new cow does not exceed limit
                cargo.append(cowsCopy[i][0]) # Add cow to cargo
                weight += cowsCopy[i][1] # Count cargo weight
                check.append(cowsCopy[i]) # Add cow to check
        totalCargo.append(cargo)
        cowsCopy[:] = [x for x in cowsCopy if x not in check] # Copy cows not in cargo to return to loop

    return totalCargo

def venbrew(cows,limit=10):

    cow_as_list = [[key, value] for key, value in cows.items()]
    cow_as_list.sort(key=lambda x: x[1], reverse = True)

    list_of_trips = []

    while cow_as_list:
        copy_of_list = cow_as_list[:]
        temporary_list = []
        limit_temp = limit

        for item in cow_as_list:
            if item[1] <= limit_temp:
                limit_temp -= item[1]
                copy_of_list.remove(item)
                temporary_list.append(item[0])

        list_of_trips.append(temporary_list)
        cow_as_list = copy_of_list[:]

    return list_of_trips

def elessime(cows,limit=10):
    pasengers=sorted(cows.items(),reverse=True,key=lambda x:x[1])
    trip, schedule, buffPas = [], [], []
    while (pasengers):
        lim=limit
        trip=[]
        for i in range(len(pasengers)):
            if pasengers[i][1]<=lim:
                lim-=pasengers[i][1]
                trip.append(pasengers[i][0])
            else:
                buffPas.append(pasengers[i])
        pasengers = buffPas
        buffPas = []
        schedule.append(trip)
    return schedule

def anamarshi(cows,limit=10):
    allTrips = []
    copyCows = cows.copy()
    cowsInOrder = sorted(copyCows.items(), key=lambda x: -x[1])
    while sum(copyCows.values())>0:
        thisTrip = []
        thisTotal = 0
        for cow in cowsInOrder:
            if copyCows[cow[0]] > 0 and copyCows[cow[0]] + thisTotal <= limit:
                thisTotal += copyCows[cow[0]]
                thisTrip.append(cow[0])
                copyCows[cow[0]] = 0
        allTrips.append(thisTrip)
    return allTrips


def fastest(cows,limit):
    pasengers = sorted(cows.items(),key=lambda x:x[1],reverse=True)
    schedule, buffPas = [], []
    while (True):
        lim=limit 
        trip=[]
        for i in pasengers:
            var = i[1]
            if var<=lim:
                lim-=var
                trip.append(i[0])
            else:
                buffPas.append(i)
        schedule.append(trip)
        if not buffPas:
            break 
        pasengers = buffPas
        buffPas = []

    return schedule

def hannahig(cows,limit=10):

    # Copy dictionary so don't mutate original
    cowsDict = cows.copy()

    # Find heaviest cow
    heaviest = 0
    sortedCows = []
    cowsNames = []
    while len(cowsDict) > 0:
        for k, v in cowsDict.items():
            if v > heaviest:
                heaviest = v
                cowsNames.append(k)
        # Creates list of cows sorted in weight order
        sortedCows.append(cowsNames.pop())
        # Removes heaviest from dictionary
        cowsDict.pop(sortedCows[-1])
        heaviest = 0

    reverseCows = sortedCows[::-1]
    # Remove any individual cow that is heavier than limit
    for cow in reversed(reverseCows):
        if cows[cow] > limit:
            reverseCows.remove(cow)

    # Keep iterating cows until all have been transported
    trips = []
    while len(reverseCows) > 0:
        # Iterate cows starting with heaviest and add to trip if limit not exceeded
        currentTrip = []
        totalWeight = 0
        for cow in reversed(reverseCows):
            if totalWeight + cows[cow] <= limit:
                currentTrip.append(cow)
                totalWeight += cows[cow]
                reverseCows.remove(cow)
        # Add trip to list of trips
        trips.append(currentTrip)

    return trips
def load_cows(filename):

    cow_dict = dict()

    f = open(filename, 'r')

    for line in f:
        line_data = line.split(',')
        cow_dict[line_data[0]] = int(line_data[1])

    return cow_dict


def create_random_test(limit, lengh):
    '''a random cow dict'''
    cows = {"Cow"+str(i): random.randrange(1, limit) for i in range(lengh)}
    return cows


RANDOM_TEST_LIST = create_random_test(10, 100)
PSET_TESTS = load_cows("ps1_cow_data.txt")

def pset_tester(f):
    return f(PSET_TESTS, 10)

def random_tester(f, limit = 10):
    return f(RANDOM_TEST_LIST, 10)

from bisect import insort
for test_fn in ('pset_tester', 'random_tester'):
    times = []
    for fn in ['fastest', 'jam', 'elessime', 'venbrew', 'natasha_c', 'colling', 'richwill', 'richard_uk', 'renata_kb',  'anamarshi', 'hannahig', 'finfate', 'mariko_ueno']:
        n = 100000 # just change n to 100 after testing pset-dict, it takes too long on 100 dict
      
        insort(times, (timeit(f'{test_fn}({fn})', globals=globals(), number=n), f'{test_fn} {fn}'))
        
    for element in times:
        print (element)
    print()
