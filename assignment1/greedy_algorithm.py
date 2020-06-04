from House import *
from configuration import *

class Greedy():

    # initialises a battery with a location and capacity
    def __init__(self):

        self.batteries = []

    # sorting houses
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

    # function to add houses to batteries
    def adding_houses(self):
        
        # temp location to store list of all houses
        self.all_houses = self.sort_house(district_1["houses"])
        self.connected_houses = []
        self.batteries = district_1["batteries"]

        # battery currently storing houses in
        self.battery_numb = 0
            
        # looping through houses
        for house in self.all_houses:

            # make sure house is not already in battery
            if not house in self.connected_houses:
                
                # check if battery is full and add house to battery
                if battery.battery_full(house):
                    
                    # move to next battery
                    self.battery_numb += 1

                # add house in next battery
                battery.add_house(house)
                    
                # add house to already sorted house
                self.connected_houses.append(house)
