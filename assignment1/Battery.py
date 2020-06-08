'''
* battery class
*
* Programmeertheorie
* Optimum Prime
*
* battery class for smartgrid problem
*
'''

from House import *
from configuration import *
from Algorithms import *

class Battery():

    # initialises a battery with a location and capacity
    def __init__(self, x_axis, y_axis, capacity):

        # saves battery location on grid
        self.position_x = x_axis

        self.position_y = y_axis

        # saves battery capacity
        self.capacity = capacity

        # total energy usage of all houses connected to battery
        self.energy_production = 0

        # length of connected cables
        self.length_cables = 0

        # total costs of cable length & battery
        self.costs = 5000

        # list of houses connected to battery
        self.houses_in_battery = []

    # calculate how much cable has to layed to add house - Sam
    def cable_length(self, house):
        return abs(self.position_x - house.position_x) + abs(self.position_y - house.position_y)

    # return true if battery is not full
    def battery_full(self, new_house):
        return self.capacity < self.energy_production + new_house.production

    # return true if house added and False if not
    def add_house(self, new_house):

        # make sure house fits in battery
        #if self.battery_full(new_house):

            # battery not enough capacity
            #return False

        # add battery
        self.energy_production += new_house.production

        # add house to houses
        self.houses_in_battery.append(new_house)

        # add costs
        self.costs += self.cable_length(new_house) * 9

        return True

    # removes house from battery and returns if battery removed
    def remove_house(self, del_house):
        
        #  remove house if in battery
        if del_house in self.houses_in_battery:
            
            self.energy_production -= del_house.production
            
            self.houses_in_battery.remove(del_house)
            
            self.costs -= self.cable_length(del_house) * 9
            
            # house removed from battery
            return True
        
        # house not in battery
        return False
        

    # empty
    def empty_battery(self):
        self.houses_in_battery = []
        self.energy_production = 0
        self.costs = 5000