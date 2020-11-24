

import unittest
import ps1 as ct
from itertools import chain
improt time

def one_sec():
    return time.sleep(1)

class testHelperFunctions(unittest.TestCase):
    '''test helper functions that are not inside the class cowTransAlgo'''

    def testPartitions(self):
        '''test all combinations given by partitions on abc'''
        combinations = [{'c', 'b', 'a'}, {'c', 'b'}, {'a'}, {'c', 'a'},
                         {'b'}, {'c'}, {'b', 'a'}, {'c'}, {'a'}, {'b'}]

        parts = list(chain.from_iterable(ct.partitions(['a','b','c'])))
        self.assertTrue(all(combination in parts for combination in combinations) and len(combinations)==len(parts))


    def testOptimizedPartitions(self):
        '''test all combinations given by optimizedPartitions using a large limit(50) for all to fit in ship'''

        combinations = [{(15, 'pirate'), (5, 'fields'), (10, 'kid')}, {(15, 'pirate'), (5, 'fields')},
                         {(10, 'kid')}, {(5, 'fields'), (10, 'kid')}, {(15, 'pirate')}, {(5, 'fields')}, 
                         {(15, 'pirate'), (10, 'kid')}, {(5, 'fields')}, {(10, 'kid')}, {(15, 'pirate')}]


        parts = list(chain.from_iterable(ct.optimizedPartitions([(10,"kid"), (15,"pirate"), (5, "fields")], 50)))
        self.assertTrue(all(combination in parts for combination in combinations) and len(combinations)==len(parts))


    def testOptimizedWeighed(self):
        '''test that sets given by optimizedPartitions is correct with a weight limit of 20'''
        combinations = [{(15, 'pirate'), (5, 'fields')},{(5, 'fields'), (10, 'kid')}, {(10, 'kid')},
                        {(15, 'pirate')}, {(5, 'fields')}, {(10, 'kid')}, {(15, 'pirate')}]
        parts = list(chain.from_iterable(ct.optimizedPartitions([(10,"kid"), (15,"pirate"), (5, "fields")], 20)))
        self.assertTrue(all(combination in parts for combination in combinations) and len(combinations)==len(parts))


    def testComparePartitions(self):
        '''compares that both partitions function yield the same partitions'''
        parts1 = list(chain.from_iterable(ct.partitions([(10,"kid"), (15,"pirate"), (5, "fields")])))
        parts2 = list(chain.from_iterable(ct.optimizedPartitions([(10,"kid"), (15,"pirate"), (5, "fields")], 50)))
        self.assertListEqual(parts1, parts2)


    def testGreedyCycle(self):
        '''test greedy_recursive_cycle'''
        sorted_cows = ct.deque(sorted([(10,"kid"), (15,"pirate"), (5, "fields")], reverse = True))
        result = list(ct.greedy_recur_cycle(sorted_cows, 20))
        self.assertEqual(result, [["pirate", "fields"], ["kid"]])



class testLoading(unittest.TestCase):
    '''test loading dictionary from file and creating random dictionary'''

    def testPsetDict(self):
        '''test that the loaded cows dictionary is as desired'''
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        cows, _ = space.getParams()
        self.assertDictEqual(cows, {'Maggie': 3, 'Herman': 7, 'Betsy': 9, 'Oreo': 6, 
                                    'Moo Moo': 3, 'Milkshake': 2, 'Millie': 5, 'Lola': 2, 
                                        'Florence': 2, 'Henrietta': 9})

    def testPsetLimit(self):
        '''test limit is passed correctly by load_cows function'''
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        _, limit = space.getParams()
        self.assertEqual(limit, 10)

    def testRandomLimit(self):
        '''test limit is passed correctly by create_random_test'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 100)
        _, limit = space.getParams()
        self.assertEqual(limit, 100)


    def testRandomWeights(self):
        '''Test weights are in limit for random dictionary'''
        space = ct.cowTransAlgos()
        limit = 100
        lengh = 100
        space.create_random_test(limit, lengh)
        cows, _ = space.getParams()
        self.assertTrue(all(cows[cow]<= limit for cow in cows))


    def testRandomLengh(self):
        '''Test random dictionary is of desired lenght'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 1000)
        cows, _ = space.getParams()
        self.assertEqual(1000, len(cows))

        
    def testTimeIt(self):
        '''tests timeIt function'''
        space = ct.cowTransAlgos()
        result = space.time_it(one_sec, 1)
        self.assertEqual(round(result, 2), 1.0)

class testGreedy(unittest.TestCase):
    '''test greedyCowTransport function'''

    def testPsetWeights(self):
        '''test all weights are within the limit for ps1_cow_data.txt'''
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        weights = space.getWeights(space.greedyCowTransport)
        _, limit = space.getParams()
        self.assertTrue(all(weight <= limit for weight in weights))


    def testPsetLen(self):
        """ Test that the output lengh of result is as expected"""
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        result = len(space.greedyCowTransport())
        self.assertEqual(result, 6)

    def testRandomWeight(self):
        '''test with random dictionary
        limit = 100, lengh of dictionary = 100'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 100)
        weights = space.getWeights(space.greedyCowTransport)
        self.assertTrue(all(weight <= 100 for weight in weights))
        


class testBruteForce(unittest.TestCase):
    '''test brute force cow transport function'''

    def testPsetWeights(self):
        '''test all weights are within limit for ps1_cow_data.txt'''
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        weights = space.getWeights(space.brute_force_cow_transport)
        _, limit = space.getParams()
        self.assertTrue(all(weight <= limit for weight in weights))


    def testPsetLen(self):
        """Test that the output lenght of result is as expected"""
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        result = len(space.brute_force_cow_transport())
        self.assertEqual(result, 5)

    def testRandomWeight(self):
        '''test with random dictionary
        limit = 100, lengh of dictionary = 10'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 10)
        weights = space.getWeights(space.brute_force_cow_transport)
        self.assertTrue(all(weight <= 100 for weight in weights))
        

class testOptimizedBrute(unittest.TestCase):
    '''test optimizedBrute function'''

    def testPsetWeights(self):
       '''test all weights are within limit for ps1_cow_data.txt'''
       space = ct.cowTransAlgos()
       space.load_cows("ps1_cow_data.txt", 10)
       weights = space.getWeights(space.optimizedBrute)
       _, limit = space.getParams()
       self.assertTrue(all(weight <= limit for weight in weights))


    def testPsetLen(self):
        """Test that the output lengh of result is as expected for ps1_cow_data.txt """
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        result = len(space.optimizedBrute())
        self.assertEqual(result, 5)

    def testRandomWeight(self):
        '''test with random dictionary
        limit = 100, lengh of dictionary = 11'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 11)
        weights = space.getWeights(space.optimizedBrute)
        self.assertTrue(all(weight <= 100 for weight in weights))


class testRecursiveGreed(unittest.TestCase):
    '''test recursiveGreed function'''

    def testPsetWeights(self):
        '''test all weights are within limit for ps1_cow_data.txt'''
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        weights = space.getWeights(space.recursiveGreed)
        _, limit = space.getParams()
        self.assertTrue(all(weight <= limit for weight in weights))


    def testPsetLen(self):
        """Test that the output lengh of result is as expected """
        space = ct.cowTransAlgos()
        space.load_cows("ps1_cow_data.txt", 10)
        result = len(space.recursiveGreed())
        self.assertEqual(result, 5)

    def testRandomWeight(self):
        '''test with random dictionary
        limit = 100, lengh of dictionary = 100'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 100)
        weights = space.getWeights(space.recursiveGreed)
        self.assertTrue(all(weight <= 100 for weight in weights))
        

class testResultsLengh(unittest.TestCase):
    '''Random test cases for testing lenght of results, all load limit = 100'''

    def testRandomShort(self):
        '''test lenght is correct for all algorithms using random 9 items dictionary'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 9)
        lenghs = [len(space.greedyCowTransport()), len(space.brute_force_cow_transport()), len(space.optimizedBrute()), len(space.recursiveGreed())]
        self.assertTrue(all(l == lenghs[0] for l in lenghs[1:]) and lenghs[0] >= lenghs[1])

    def testRandomLong(self):
        '''test lenght is correct for optimizedBruete and recursiveGreed using random 11 item dictionary'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 11)
        lenghs = [len(space.optimizedBrute()), len(space.recursiveGreed())]
        self.assertEqual(lenghs[0], lenghs[1])


    def testRandomLonger(self):
        '''test lenght is correct for greedyCowTransport and recursiveGreed using random 15 item dictionary'''
        space = ct.cowTransAlgos()
        space.create_random_test(100, 15)
        lenghs = [len(space.greedyCowTransport()), len(space.recursiveGreed())]
        self.assertGreaterEqual(lenghs[0], lenghs[1])



if __name__ == '__main__':
    unittest.main()



