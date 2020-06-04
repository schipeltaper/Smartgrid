from House import *
from Algorithms import *
from Battery import *
from configuration import *
import numpy as np
#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt


# random solution that doesn't violate max. battery capacities
class Randomworld_1():
    def __init__(self, district):
        self.batteries = district["batteries"]
        self.houses = sortHouse(district["houses"])
        self.costs = 0
    
    def distribute_houses(self):
        for house in self.houses:
            done = False
            negmaxcapacityleft = 0
            for battery in self.batteries:
                negcapleft = battery.energy_production - battery.capacity
                if negcapleft < negmaxcapacityleft:
                    negmaxcapacityleft = negcapleft
            maxcapleft = -negmaxcapacityleft
            if maxcapleft < house.production:
                return False
            while done == False:
                i = np.random.randint(0, len(self.batteries))
                done = self.batteries[i].add_house(house)
        for battery in self.batteries:
            self.costs += battery.costs
        return True
    def reset_world(self):
        for battery in self.batteries:
            battery.energy_production = 0

            # length of connected cables
            battery.length_cables = 0

            # total costs of cable length & battery
            battery.costs = 5000

            # list of houses connected to battery
            battery.houses_in_battery = []
            
            self.costs = 0

costs = []
k = 0
world = Randomworld_1(district_1)
while k < 10000:
    valid = False
    tries = 0
    while valid == False:
        world.reset_world()
        valid = world.distribute_houses()
        tries += 1
    costs.append(world.costs)
    k += 1

#num_bins = 50
#plt.hist(costs, num_bins, facecolor='blue', alpha=0.5)
#plt.show()
print(costs)       
            
            
