from House import *
from Configuration import *
import copy

class Greedy():

    # initialises a battery with a location and capacity
    def __init__(self):

        # place to store batteries
        self.batteries = []

        # adding batteries
        self.adding_batteries()

        # temp location to store list of all houses -- specificly for district_1 for now
        self.all_houses = district_1["houses"]
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
    
    # sorting houses low too high
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

        self.house_low_sort(self.all_houses)

        self.closses_batteries = self.batteries.copy()
        
        # itterate through all houses
        for self.the_house in self.all_houses:

            # itterate through batteries
            for self.battery_numb in range(len(self.closses_batteries)):

                # itterate through remaining batteries
                for self.battery_numb2 in range(self.battery_numb, len(self.closses_batteries)):
                    
                    # check if contested battery is closses to other battery further down
                    if self.closses_batteries[self.battery_numb2].cable_length(self.the_house) < self.closses_batteries[self.battery_numb].cable_length(self.the_house):
                        
                        # switch batteries in list
                        self.temp_save = self.closses_batteries[self.battery_numb]

                        self.closses_batteries[self.battery_numb] = self.closses_batteries[self.battery_numb2]

                        self.closses_batteries[self.battery_numb2] = self.temp_save
            
            # add house to closest none full house
            for self.the_battery in self.closses_batteries:

                # make sure battery is not full
                if self.the_battery.battery_full(self.the_house) is not True:
                    
                    # add house to battery
                    self.the_battery.add_house(self.the_house)
                    
                    # go to next house
                    break
    
    
    # adds batteries too battiers in Greedy object
    def adding_batteries(self):
        self.batteries = copy.deepcopy(district_1["batteries"])
    
    # function to add houses to batteries
    def adding_houses(self):

        # sorting houses
        self.sort_house(self.all_houses)

        # battery currently storing houses in
        self.battery_numb = 0
            
        # looping through houses
        for house in self.all_houses:
            
            # make sure house is not already in battery
            if not house in self.connected_houses:
                
                # loop through batteries for every house
                self.battery_numb += 1

                if self.battery_numb >= len(self.batteries):
                    self.battery_numb = 0
                
                # check if battery is full and add house to battery
                if self.batteries[self.battery_numb].battery_full(house):
                    
                    # move to next battery
                    self.battery_numb += 1

                # add house in next battery
                self.batteries[self.battery_numb].add_house(house)
                    
                # add house to already sorted house
                self.connected_houses.append(house)
