
'''
* simulated_annealing class
* 
*
* Programmeertheorie
* Optimum Prime
*
* The simulated_annealing class distributes the house under the batteries randomly,
* and than suffles the houses based on a simulated annealing algorithm.
* 
*
'''

from algorithms.greedy_algorithm import Greedy
from classes.Configuration import Configuration
from algorithms.cable_algorithm import Cable
import random

class simulated_annealing():
    '''
    The simulated_annealing class contains all the function realing to the simulatee
    annealing algorithm. The simulated annealing algorithm calculates the energy it 
    costs to move a house from its current battery to a radomly choosen different one. 
    This energy cost is calculated based the fullness of the battery the house would move 
    too and the distance of that battery too the house. The energy of in the system diminishes
    over time, making disadvantagose moves less and less common. Simulated annealing will
    increase the change of exploring multiple minima.

    Initialisation requires a district configuration.
    '''
    def __init__(self, district_configuration):

        self.district = district_configuration

        self.max_energy_costs = 100
        self.weight_distance = 0.8
        self.weight_battery_capacity = 1 - self.weight_distance
        
        self.energy = 100

        # keeps track of the amount of moves made -- Tracking variable!!!!!!!!!!!!!!!!!
        self.moves_made = 0

        self.greedy_class_var = Greedy(self.district)

        self.cable_algorithm = Cable(self.district)
    
    # starts with randomly distributing houses amoung batteries
    def creating_starting_possition(self):
        '''
        Creates a starting possition, where all houses are distributed amoungst the batteries
        radomly. Batteries could be filled over their energy capacity. The battery distribtution
        is saved in the configuration.
        '''

        self.random_house_distribution()

    def running_simulated_annealing(self, share_cables):
        '''
        Runs the simulated_annealing algorithm. This algorithm is called after a starting possition
        is created and will run the simulated annealing algorithm untill the energy in the system is
        zero or lower. If the solution contains batteries that have over capacity the function will
        be re-run at full energy level.

        Input: boolean that indicates if cable sharing is allowed (True: cable sharing allowed).
        '''
        while not(self.energy < 0):
            self.distributing_houses_amoung_batteries()
            self.energy -= 20
        
        if self.district.houses_with_ovorcapacity():
            self.energy = 100
            self.running_simulated_annealing(share_cables)
            
    def distributing_houses_amoung_batteries(self):
        '''
        Runs the simulated_annealing algorithm. This algorithm is called after a starting position
        is created and will run the simulated annealing algorithm untill the energy in the system is
        zero or lower. If the solution contains batteries that have over capacity the function will
        be re-run at full energy level.
        '''
        
        # moves houses to different battery if move costs less energy than energy in the system
        for self.house in self.district.all_houses:
            self.choosen_battery = random.choice(self.district.all_batteries)
            if self.make_next_move(self.house, self.choosen_battery):
                if not(self.house.battery == None):
                    self.house.battery.remove_house(self.house)                
                self.choosen_battery.add_house(self.house)
                self.house.battery = self.choosen_battery
        
        # maybe add loop until batteries not over capacity

    def make_next_move(self, house, battery):
        '''
        Calculates the energy cost of moving a house to a different battery based on the battery fullness
        and the distance proximity from the house to the battery. Than desides if the move should be made 
        given the enery in the system.

        Input: a house instance and a battery instance.
        
        Return: boolea, True if the move should be made.
        '''
        
        self.energy_of_move = self.energy_move_distance(house, battery) + self.energy_move_b_cap(battery)
        if self.energy_of_move < self.max_energy_costs:
            return True
        return False

    def energy_move_distance(self, house, battery):
        '''
        Calculates the distance energy cost of moving a house to a different battery. Does this based on the
        distance between the house and the potential battery to move to. The energy cost returned cannot be
        greater than self.max_costs_distance, which is calculated using the maximum energy cost allowed from
        one move and the weight distance has on the move.

        Formula used: max_costs_distance * (1 - 0,1^((distance * mutiplier)/100))

        Input: a house instance and a battery instance.
        
        Return: Int that indicates energy costs of the distance.
        '''

        self.max_costs_distance = self.max_energy_costs * self.weight_distance
        return int(self.max_costs_distance *  (1 - (0.1 ** ((self.cable_algorithm.calculate_distance(house, battery) \
        * 2)/100))))

    def energy_move_b_cap(self, battery):
        '''
        Calculates the battery fullness energy cost of moving a house to a different battery. Does this based 
        on the fullness of the potential battery of the battery to move the hosue to, compared to the average 
        fullness of all batteries. The energy cost returned cannot be greater than self.max_costs_distance, 
        which is calculated using the maximum energy cost allowed from one move and the weight battery fullness 
        has on the move.

        Formula used: max_costs_cap * (1 - 0,1^((distance from average * mutiplier)/10000))

        Input: a house instance and a battery instance.
        
        Return: Int that indicates energy costs added based on how full the other battery is.
        '''
        
        # calculates the max energy the battery fullness can cost
        self.max_costs_cap = self.max_energy_costs * self.weight_battery_capacity
        
        # calculates the energy costs of the battery fullness for the move
        self.avrg_production_bats = 0
        for self.single_battery in self.district.all_batteries:
            self.avrg_production_bats += self.single_battery.energy_production
        self.avrg_production_bats = self.avrg_production_bats/len(self.district.all_batteries)
        self.distance_from_average = 0
        self.distance_from_average -= self.avrg_production_bats
        if self.distance_from_average < 0:
            return 0
        else:
            return self.max_costs_cap *  (1 - (0.1 ** ((self.distance_from_average * 6)/10000)))

    def random_house_distribution(self):
        '''
        Randomly distributes all houses amoung the batteries and saves this distribution into the batteries 
        (houses_in_battery) and the houses (battery) in the configuration.
        '''
        
        for self.a_house in self.district.all_houses:
            self.a_house.battery = random.choice(self.district.all_batteries)
            self.a_house.battery.houses_in_battery.append(self.a_house)