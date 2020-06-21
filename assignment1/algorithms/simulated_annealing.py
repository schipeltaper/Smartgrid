
from algorithms.greedy_algorithm import Greedy
from classes.Configuration import Configuration
from algorithms.cable_algorithm import Cable
import random

class simulated_annealing():
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

        self.distributing_houses_amoung_batteries()

    def running_simulated_annealing(self, share_cables):

        while not(self.energy < 0):
            self.distributing_houses_amoung_batteries()
            
            self.energy -= 20
        
        if self.district.houses_with_ovorcapacity():
            self.energy = 100
            self.running_simulated_annealing(share_cables)
            
    # distributes all houses in district randomly
    def distributing_houses_amoung_batteries(self):
        
        for self.house in self.district.all_houses:
            
            self.choosen_battery = random.choice(self.district.all_batteries)

            if self.make_next_move(self.house, self.choosen_battery):
            
                if not(self.house.battery == None):
                    # removing house from former battery
                    self.house.battery.remove_house(self.house)
                
                # adding house to battery & battery to house
                self.choosen_battery.add_house(self.house)

                self.house.battery = self.choosen_battery

    def make_next_move(self, house, battery):
        
        self.energy_of_move = self.energy_move_distance(house, battery) + self.energy_move_b_cap(battery)
        
        if self.energy_of_move < self.max_energy_costs:

            return True

        return False

    # determines the amount of energy costs added from distance to next battery
    def energy_move_distance(self, house, battery):

        # max energy costs of distance
        self.max_costs_distance = self.max_energy_costs * self.weight_distance

        # max_costs_distance * (1 - 0,1^((distance * mutiplier)/100))
        return self.max_costs_distance *  (1 - (0.1 ** ((self.cable_algorithm.calculate_distance(house, battery) * 2)/100)))

    def energy_move_b_cap(self, battery):
        
        # max energy costs of distance
        self.max_costs_cap = self.max_energy_costs * self.weight_battery_capacity

        # calculate average energy production of houses in battery
        self.avrg_production_bats = 0
        for self.single_battery in self.district.all_batteries:
            self.avrg_production_bats += self.single_battery.energy_production
        self.avrg_production_bats = self.avrg_production_bats/len(self.district.all_batteries)
        self.distance_from_average = 0
        self.distance_from_average -= self.avrg_production_bats
        if self.distance_from_average < 0:
            return 0
        else:
            # max_costs_cap * (1 - 0,1^((distance * mutiplier)/100))
            return self.max_costs_cap *  (1 - (0.1 ** ((self.distance_from_average * 6)/10000)))

    # then randomly jumps too different battery
        # the energy of the jump is determined by the distance between the house and the next battery and..
        # ..and the fullness of the battery compared to the other batteries

    