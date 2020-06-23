'''
* Combining_algorithms class
* 
*
* Programmeertheorie
* Optimum Prime
*
* The Combining_algorithms class collects and runs all the different algorithms
* combinations.
* 
*
'''

import copy
import numpy as np

from classes.battery import Battery
from classes.house import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from classes.configuration import Configuration
from algorithms.hill_climber import Hill_climber
from algorithms.simulated_annealing import simulated_annealing


class Combining_algorithms():
    '''
    The Combining_algorithms class brings the two types of algorithms that the 
    Optimum Prime program uses to solve this problem together: the algorithms
    that devide the houses amoungst the batteries in the configuration and the
    algorithms that lay the cables that connect these houses with the cables.
    The initialisation is done using the number of district instance the user
    wants to use.
    '''
    def __init__(self, district_numb):
        # loads the batteries and houses into district variable of type configuration
        self.the_district = Configuration(district_numb)
        self.the_district.create_district()

    # Greedy_house allocation & Astar cable drawing - assumption 1 cable 1 house
    def greedy_house_manhatten_cable(self, cable_sharing):
        '''
        Uses a greedy algorithm with a huristic based on proximity of a house to
        a battery to devide the houses amoungst the batteries. Than uses the manhatten
        distance to lay cables between thouse houses and their batteries. Finally, prints
        the total costs of the solution.
        '''
        
        self.greedy_house_devide = Greedy(self.the_district)
        self.greedy_house_devide.proximity_sort()
        self.astar_cable = Cable(self.the_district)
        self.astar_cable.cable_list_batteries(self.the_district.all_batteries, cable_sharing)
        self.the_district.refresh_config()
        return self.greedy_house_devide.district.cs50_check(cable_sharing)

    def annealing_hill_climber(self, step_num, cable_sharing):
        '''
        This method first applies the simulating annealing algorithm to sort all the houses
        in the batteries. Then it applies the hill climber algorithm to modify this solution
        to an even better one. It takes step_num steps in the hill climber algorithm.
        '''

        self.annealing_house_devide1 = simulated_annealing(self.the_district)
        self.annealing_house_devide1.creating_starting_possition()
        self.annealing_house_devide1.running_simulated_annealing(cable_sharing)
        self.hill = Hill_climber(self.the_district)
        self.hill.climb_the_hill(step_num)
        self.the_district.refresh_config()
        return self.annealing_house_devide1.district.cs50_check(cable_sharing)

    # simulated anealing house distribution & Astar cable drawing - assumption 1 cable 1 house
    def simulated_annealing_house_manhatten_cable(self, cable_sharing):
        '''
        Combines a simulated annealing algorithm with a huristic based on proximity of a house to a
        battery and the fullness of a battery compared to other batteries to devide the houses amoung
        the batteries. Than uses the manhatten distance to lay cables between thouse houses and their 
        batteries. Finally, prints the total costs of the solution.
        '''

        self.sa_distribution = simulated_annealing(self.the_district)
        self.sa_distribution.creating_starting_possition()
        self.sa_distribution.running_simulated_annealing(cable_sharing)
        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, cable_sharing)
        self.the_district.refresh_config()
        return self.sa_distribution.district.cs50_check(cable_sharing)

    def random_greedy_astar_manhatten_cable(self, rounds, cable_sharing):
        '''
        Introduces some randomness too a greedy algorithm with a huristic based on proximity of a house 
        to a battery. Than uses the manhatten distance to lay cables between thouse houses and their 
        batteries. Finally, prints the total costs of the solution.
        '''
        
        self.random_greedy = Greedy(self.the_district)
        self.random_greedy.random_greedy(rounds)
        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, cable_sharing)
        self.the_district.refresh_config()
        return self.random_greedy.district.cs50_check(cable_sharing)






