
from classes.House import House
from classes.map_lists import district_1, district_2, district_3
import copy
import random

class Greedy():

    # initialises a battery with a location and capacity
    def __init__(self, district_configuration):

        self.district = district_configuration
        
        # place to store batteries
        self.batteries = self.district.all_batteries

        # saves the costs in this object
        self.costs = 0
        
        # adding batteries
        self.adding_batteries()

        # temp location to store list of all houses
        self.all_houses = self.district.all_houses
        self.connected_houses = []


    # sorting houses hight too low
    def sort_house(self, houses):
        
        # Selection Sort
        for self.house_numb in range(len(houses)):
            biggest_location = self.house_numb

            # We're searching for the highest production
            for self.house_numb2 in range(self.house_numb, len(houses)):
                if houses[self.house_numb2].production > houses[biggest_location].production:
                    biggest_location = self.house_numb2

            self.temp = houses[self.house_numb]
            houses[self.house_numb] = houses[biggest_location]
            houses[biggest_location] = self.temp

        return houses
    
    # sorting houses low too high production
    def house_low_sort(self, houses):

        # Selection Sort
        for self.house_numb in range(len(houses)):

            # We're searching for the highest production
            for self.house_numb2 in range(self.house_numb, len(houses)):
                if houses[self.house_numb2].production < houses[self.house_numb].production:
                    self.temp = houses[self.house_numb]

                    houses[self.house_numb] = houses[self.house_numb2]

                    houses[self.house_numb2] = self.temp

        return houses
    
    # sorting batteries by closest battery
    def proximity_sort(self):

        # sorting houses high too low production
        self.all_houses = self.sort_house(self.all_houses)
        
        # itterate through all houses
        for self.the_house in self.all_houses:

            # itterate through batteries
            for self.battery_numb in range(len(self.batteries)):

                # itterate through remaining batteries
                for self.battery_numb2 in range(self.battery_numb, len(self.batteries)):
                    
                    # check if contested battery is closses to other battery further down
                    if self.batteries[self.battery_numb2].distance(self.the_house) < self.batteries[self.battery_numb].distance(self.the_house):
                        
                        # switch batteries in list
                        self.temp_save = self.batteries[self.battery_numb]

                        self.batteries[self.battery_numb] = self.batteries[self.battery_numb2]

                        self.batteries[self.battery_numb2] = self.temp_save
            
            # add house to closest none full house
            for self.the_battery in self.batteries:

                # make sure battery is not full
                if self.the_battery.battery_full(self.the_house) is not True:
                    
                    # add house to battery
                    self.the_battery.add_house(self.the_house)

                    # go to next house
                    break

                else:
                    # warn user if not all houses allocated
                    if self.the_battery == self.batteries[len(self.batteries)-1]:
                        print("Not all houses added to batteries because all batteries full!")
                
        self.district.all_batteries = self.batteries
    
    # adds batteries too battiers in Greedy object
    def adding_batteries(self):
        # adds the costs of the battery
        self.costs += 5000 * len(self.district.all_batteries)
        self.batteries = copy.deepcopy(self.district.all_batteries)
    
    # function to add houses to batteries
    def adding_houses(self):

        # sorting houses
        self.sort_house(self.all_houses)

        # battery currently storing houses in
        self.battery_numb = 0
            
        # looping through houses
        for self.house in self.all_houses:
            
            # make sure house is not already in battery
            if not self.house in self.connected_houses:
                
                # loop through batteries for every house
                self.battery_numb += 1

                if self.battery_numb >= len(self.batteries):
                    self.battery_numb = 0
                
                # check if battery is full and add house to battery
                if self.batteries[self.battery_numb].battery_full(self.house):
                    
                    # move to next battery
                    self.battery_numb += 1

                # add house in next battery
                self.batteries[self.battery_numb].add_house(self.house)
                    
                # add house to already sorted house
                self.connected_houses.append(self.house)

    # random Greedy
    def random_greedy(self, rounds):
        from algorithms.simulated_annealing import simulated_annealing
        
        # getting access to functions in simulated anneaaling
        self.functions_in_sa_class = simulated_annealing(self.district)
        
        # distributing houses randomly amoung batteries
        self.functions_in_sa_class.distributing_houses_amoung_batteries()

        self.rounds_done = 0
        # consier move for all houses rounds times
        while self.rounds_done < rounds:
            
            for self.one_house in self.district.all_houses:
                self.proximity_move(self.one_house)

            self.rounds_done += 1


    # choosing if house should move to different battery
    def proximity_move(self, house):
        
        # move if option better than current situation
        self.choosen_battery = random.choice(self.district.all_batteries)

        if self.choosen_battery.distance(house) < house.battery.distance(house):
            
            # removing house from former battery
            house.battery.remove_house(house)
                
            # adding house to battery & battery to house
            self.choosen_battery.add_house(house)

            house.battery = self.choosen_battery
