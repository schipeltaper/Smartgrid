
from classes.Battery import Battery
from classes.House import House
from classes.map_lists import district_1, district_2, district_3
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from classes.Configuration import Configuration

class Combining_algorithms():
    def __init__(self, height, width, district):
        self.the_district = Configuration(height, width)
        self.the_district.create_district(district)

        self.choosen_district = district
 
    # Greedy_house allocation & Astar cable drawing
    def greedy_house_astar_cable(self):
        
        # creating an instant to save greedy object
        self.greedy_house_devide = Greedy(self.choosen_district)
        
        # deviding houses amoung batteries using proximity
        self.greedy_house_devide.proximity_sort()

        self.astar_cable = Cable(self.the_district)
        
        # laying cables for every battery between its own houses
        self.astar_cable.cable_list_batteries(self.greedy_house_devide.batteries)
        
        # quick calculation of how many cables have be layed
        self.cable_leng = 0
        for cable_lines in self.astar_cable.cable_network:
            self.cable_leng += len(cable_lines)

        # adding cable costs to costs
        self.greedy_house_devide.costs += self.cable_leng * 9


# calculate costs for list of batteries
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs


