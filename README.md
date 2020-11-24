# cows
make sure you have requirements installed and python 3.5+
# Usage Examples:

>>> import ps1 as ct

>>> space = ct.cowTransAlgos()

you can load cows from any file as fallows, where limit is spaceship load limit:

space.load_cows('<path_to_file>', limit)

>>> space.load_cows('ps1_cow_data.txt', 10)

if you rather use a random dictionary you can costum make it
specify the desired weight limit and lenght as fallows:

>>> space.create_random_test(100, 10)

will create a dictionary of lengh 10 and max weight 100.


to get the dictionary and limit:

>>> space.getParams()

to see the result given by an algorithm use the following after loading or creating the parametes

greedyCowTranport:

>>> space.greedyCowTransport()

brute_force_cow_transport:

>>> space.brute_force_cow_transport()

optimizedBrute:

>>> space.optimizedBrute()

recursiveGreed:

>>> space.recursiveGreed()


compare results and times of all four algorithms with the following functions:

>>> space.compareResults()

>>> space.compareTimes()

it will print results in tabulated format
each algorithm will only be timed 10 times



time a function individually any number of times

>>> space.time_it(space.greedyCowTransport, 100000)

will time greedyCowTransport 100000 times and return the mean
this give a more accurate timing result,
but don't try timing the brutes 100000 times

view the weights associated with each trip for a given function with the 
following command

>>> space.getWeights(space.optimizedBrute)

will get the weights given by optimizedBrute algorithm


Original instructions given for this exercise
by the MIT course:


Space Cows Introduction

A colony of Aucks (super-intelligent alien bioengineers) has landed on Earth and has created new species of farm animals! 
The Aucks are performing their experiments on Earth, and plan on transporting the mutant animals back to their home planet of Aurock.
In this problem set, you will implement algorithms to figure out how the aliens should shuttle their experimental animals back across space.

Transporting Cows Across Space!

The aliens have succeeded in breeding cows that jump over the moon! Now they want to take home their mutant cows. 
The aliens want to take all chosen cows back, but their spaceship has a weight limit and they want to minimize the number of trips they have to take across the universe.
Somehow, the aliens have developed breeding technology to make cows with only integer weights.

You can expect the data to be formatted in pairs of x,y on each line, where x is the name of the cow and y is a number indicating how much the cow weighs in tons,
and that all of the cows have unique names. Here are the first few lines of ps1_cow_data.txt:

Maggie,3
Herman,7
Betsy,9
...
