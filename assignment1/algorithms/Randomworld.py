
from classes.House import House
from classes.Battery import Battery
from classes.map_lists import district_1, district_2, district_3
import numpy as np


# random solution that doesn't violate max. battery capacities
class Randomworld_1():
    def __init__(self, district):
        self.batteries = district["batteries"]
        self.houses = district["houses"]
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
            battery.empty_battery()
        self.costs = 0
    def run(self):
        valid = False
        while valid == False:
            self.reset_world()
            valid = self.distribute_houses()

# random solution that doesn't violate max. battery capacities
class Nearest_battery_world_1():
    def __init__(self, district):
        self.batteries = district["batteries"]
        self.houses = district["houses"]
        self.costs = 0
        self.violation = 0
    
    def Update_violation(self):
        violation = 0
        self.costs = 0
        for battery in self.batteries:
            violation += max(0,(battery.energy_production - battery.capacity)) ** 2
            self.costs += battery.costs
        self.violation = violation
    
    def reset_world(self):
        for battery in self.batteries:
            battery.empty_battery()
        self.costs = 0
    
    def distribute_houses(self):
        for house in self.houses:
            mindist = float('inf')
            i=0
            while(i < len(self.batteries)):
                dist = self.batteries[i].cable_length(house)
                if dist < mindist:
                    mindist = dist
                    minindex = i
                i += 1
            self.batteries[minindex].add_house(house)
        self.Update_violation()
    
    def Relocate_random_house(self):
        initial_violation = self.violation
        #choose two different random batteries
        b_1 = np.random.randint(0, len(self.batteries))
        while len(self.batteries[b_1].houses_in_battery) == 0:
            b_1 = np.random.randint(0, len(self.batteries))
        b_2 = np.random.randint(0, len(self.batteries))
        while b_2 == b_1:
            b_2 = np.random.randint(0, len(self.batteries))
        #choose a random house in the first battery
        h_1 = np.random.randint(0, len(self.batteries[b_1].houses_in_battery))
        
        violation_dif_1 = max(0,(self.batteries[b_1].energy_production - self.batteries[b_1].capacity - self.batteries[b_1].houses_in_battery[h_1].production)) ** 2 - max(0,(self.batteries[b_1].energy_production - self.batteries[b_1].capacity)) ** 2
        violation_dif_2 = max(0,(self.batteries[b_2].energy_production - self.batteries[b_2].capacity + self.batteries[b_1].houses_in_battery[h_1].production)) ** 2 - max(0,(self.batteries[b_2].energy_production - self.batteries[b_2].capacity)) ** 2
        
        violation_dif = violation_dif_1 + violation_dif_2
        
        if violation_dif < 0:
            self.batteries[b_2].add_house(self.batteries[b_1].houses_in_battery[h_1])
            self.batteries[b_1].remove_house(self.batteries[b_1].houses_in_battery[h_1])
        self.Update_violation()
    
    def Find_valid_sol_1(self):
        same = 0
        while self.violation > 0 and same < 100:
            violation = self.violation
            self.Relocate_random_house()
            if violation == self.violation:
                same += 1
            else:
                same = 0
        if self.violation > 0:
            self.reset_world()
            return False
    
    def Find_valid_sol_2(self):
        self.distribute_houses()
        while self.Find_valid_sol_1() == False:
            self.distribute_houses()
        
            
        



