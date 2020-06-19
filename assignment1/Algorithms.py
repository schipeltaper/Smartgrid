
from classes.Battery import Battery
from classes.House import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from classes.Configuration import Configuration
from algorithms.simulated_annealing import simulated_annealing
import numpy as np


class Combining_algorithms():
    def __init__(self, height, width, district):
        self.the_district = Configuration(height, width, district)
        self.the_district.create_district()

        self.choosen_district = district
 
    # Greedy_house allocation & Astar cable drawing - assumption 1 cable 1 house
    def greedy_house_astar_cable(self):
        
        # creating an instant to save greedy object
        self.greedy_house_devide = Greedy(self.the_district)
        
        # deviding houses amoung batteries using proximity
        self.greedy_house_devide.proximity_sort()

        # save the cable algorithm object
        self.astar_cable = Cable(self.the_district)
        
        # laying cables for every battery between its own houses
        self.astar_cable.cable_list_batteries(self.the_district.all_batteries)

        self.the_district.cal_costs()
        print(f"The total costs of configuration: {self.the_district.total_costs}")

    
    # simulated anealing house distribution & Astar cable drawing - assumption 1 cable 1 house
    def simulated_annealing_house_astar_cable(self):
        self.sa_distribution = simulated_annealing(self.the_district)
        self.sa_distribution.creating_starting_possition()

        self.sa_distribution.running_simulated_annealing()

        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries)
        

        self.the_district.cal_costs()
        print(f"The total costs of configuration: {self.the_district.total_costs}")

# calculate costs for list of batteries
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs
    
class optimum_deluxe():
    def __init__(self, district_id):
        self.world = Configuration(district_id)
    
    def connect_house(self, world, house, battery):
        battery.add_house(house)
        battery_points = []
        lists = world.get_lists()
        
        # create list of points connected to battery
        for battery0 in lists[0]:
            if battery0[2] == battery:
                battery_points.append([battery0[0], battery0[1]])
                for cable in battery0[3]:
                    battery_points.append(cable[0])
                    battery_points.append(cable[1])
        
        nearest_point = [-1, -1]
        dist = float('inf')
        house_point = [house.position_x, house.position_y]
        
        # get connected point nearest to house
        for point in battery_points:
            dist1 = abs(house_point[0] - point[0]) + abs(house_point[1] - point[1])
            if dist1 < dist:
                dist = dist1
                nearest_point = point
                
        # make random path to nearest point
        x_orientation = 1
        y_orientation = 1
        
        if nearest_point[0] - house_point[0] < 0:
            x_orientation = -1
        if nearest_point[1] - house_point[1] < 0:
            y_orientation = -1
        
        x_dist = abs(nearest_point[0] - house_point[0])
        y_dist = abs(nearest_point[1] - house_point[1])
        
        current_point = house_point
        
        while x_dist + y_dist > 0:
            if np.random.randint(0, x_dist + y_dist) < x_dist:
                self.world.add_cable(self.world.configuration[current_point[0]][current_point[1]], self.world.configuration[current_point[0] + x_orientation][current_point[1]], battery)
                current_point = [current_point[0] + x_orientation, current_point[1]]
                x_dist -= 1
            else:
                self.world.add_cable(self.world.configuration[current_point[0]][current_point[1]], self.world.configuration[current_point[0]][current_point[1] + y_orientation], battery)
                current_point = [current_point[0], current_point[1] + y_orientation]
                y_dist -= 1
            
    def disconnect_house(self, world, house, battery):
        battery.remove_house(house)
        current_point = world.configuration[house.position_x][house.position_y]
        neighbours0 = self.neighbours_list(current_point, battery)
        neighbour_count = len(neighbours0)
        points_to_exclude = [[battery.position_x, battery.position_y]]
        for house1 in battery.houses_in_battery:
            points_to_exclude.append([house1.position_x, house1.position_y])
        
        while neighbour_count == 1 and [current_point.x,current_point.y] not in points_to_exclude:
            next_point = neighbours0[0]
            world.delete_cable(current_point, neighbours0[0], battery)
            current_point = next_point
            neighbours0 = self.neighbours_list(current_point, battery)
            neighbour_count = len(neighbours0)
    
    def neighbours_list(self, point, battery):
        neighbours = []
        if battery in point.neighbours:
            neighbours = point.neighbours[battery]
        return neighbours
        
    def check_costs_to_connect_house_to_battery(self, house, battery):
        costs = self.world.get_lists()[2]
        self.connect_house(self.world, house, battery)
        new_costs = self.world.get_lists()[2]
        self.disconnect_house(self.world, house, battery)
        return new_costs - costs
        
    def get_disconnected_houses_and_all_batteries(self, world):
        lists = world.get_lists()
        houses0 = lists[1]
        batteries0 = lists[0]
        houses = []
        batteries = []
        for house in houses0:
            houses.append(house[2])
        
        houses2 = []
        for battery1 in batteries0:
            battery = battery1[2]
            batteries.append(battery)
            houses_in_battery = battery.houses_in_battery
            for house2 in houses_in_battery:
                houses2.append(house2)
                
        houses3 = []
        for house4 in houses:
            if house4 not in houses2:
                houses3.append(house4)
        return houses3, batteries
    
    def connect_cheapest_house(self):
        houses, batteries = self.get_disconnected_houses_and_all_batteries(self.world)
        if len(houses) == 0:
            return False
        else:
            house0 = None
            battery0 = None
            cost = float('inf')
            for house in houses:
                for battery in batteries:
                    cost1 = self.check_costs_to_connect_house_to_battery(house, battery)
                    if cost1 < cost:
                        house0 = house
                        battery0 = battery
                        cost = cost1
            self.connect_house(self.world, house0, battery0)
            return True
    
    def connect_all_houses(self):
        while self.connect_cheapest_house():
            pass
            
    def check_costs_to_relocate_house(self, house, battery_1, battery_2):
        old_costs = self.world.get_lists()[2]
        old_bat_violation = self.world.check('Optimum Deluxe')[4]
        self.disconnect_house(self.world, house, battery_1)
        self.connect_house(self.world, house, battery_2)
        new_costs = self.world.get_lists()[2]
        new_bat_violation = self.world.check('Optimum Deluxe')[4]
        bat_gained = old_bat_violation - new_bat_violation
        extra_costs = new_costs - old_costs
        self.disconnect_house(self.world, house, battery_2)
        self.connect_house(self.world, house, battery_1)
        return bat_gained, extra_costs
        
    def do_best_relocation_of_house(self):
        houses, batteries = self.get_disconnected_houses_and_all_batteries(self.world)
        battery0_1 = None
        battery0_2 = None
        house0 = None
        min_cost_per_bat_gained = float('inf')
        
        for i in range(len(batteries)):
            for house in batteries[i].houses_in_battery:
                for j in range(len(batteries)):
                    if(j != i):
                        bat_gained, extra_costs = self.check_costs_to_relocate_house(house, batteries[i], batteries[j])
                        if bat_gained > 0:
                            cost_per_bat_gained = extra_costs / bat_gained
                            if cost_per_bat_gained < min_cost_per_bat_gained:
                                battery0_1 = batteries[i]
                                battery0_2 = batteries[j]
                                house0 = house
                                min_cost_per_bat_gained = cost_per_bat_gained
        if battery0_1 == None:
            return False
        else:
            self.disconnect_house(self.world, house0, battery0_1)
            self.connect_house(self.world, house0, battery0_2)
            return True
            
    def relocate_untill_convergence(self):
        while self.do_best_relocation_of_house():
            pass
    
    def switch_houses(self, world, battery_1, house_1, battery_2, house_2):
        self.disconnect_house(world, house_1, battery_1)
        self.disconnect_house(world, house_2, battery_2)
        self.connect_house(world, house_1, battery_2)
        self.connect_house(world, house_2, battery_1)
        
    def check_costs_to_switch_houses(self, battery_1, house_1, battery_2, house_2):
        old_costs = self.world.get_lists()[2]
        old_bat_violation = self.world.check('Optimum Deluxe')[4]
        self.switch_houses(self.world, battery_1, house_1, battery_2, house_2)
        print(self.world.check('Optimum Deluxe'))
        print (self.world.text_grid())
        new_costs = self.world.get_lists()[2]
        new_bat_violation = self.world.check('Optimum Deluxe')[4]
        bat_gained = old_bat_violation - new_bat_violation
        extra_costs = new_costs - old_costs
        self.switch_houses(self.world, battery_2, house_2, battery_1, house_1)
        return bat_gained, extra_costs
    
    def do_best_switch_of_houses(self):
        houses, batteries = self.get_disconnected_houses_and_all_batteries(self.world)
        battery0_1 = None
        battery0_2 = None
        house0_1 = None
        house0_2 = None
        min_cost_per_bat_gained = float('inf')
        
        for i in range(len(batteries)):
            for house_1 in batteries[i].houses_in_battery:
                for j in range(len(batteries)):
                    if(j != i):
                        for house_2 in batteries[j].houses_in_battery:
                            bat_gained, extra_costs = self.check_costs_to_switch_houses(batteries[i], house_1, batteries[j], house_2)
                            if bat_gained > 0:
                                print('!')
                                cost_per_bat_gained = extra_costs / bat_gained
                                if cost_per_bat_gained < min_cost_per_bat_gained:
                                    battery0_1 = batteries[i]
                                    battery0_2 = batteries[j]
                                    house0_1 = house_1
                                    house0_2 = house_2
                                    min_cost_per_bat_gained = cost_per_bat_gained
        if battery0_1 == None:
            return False
        else:
            switch_houses(self.world, battery0_1, house0_1, battery0_2, house0_2)
            return True
            
    def switch_houses_until_convergence(self):
        while self.do_best_switch_of_houses():
            pass
#[valid, all_houses_in_battery, bat_cap_not_exceeded, all_houses_connected, bat_cap_violation, houses_disconnected]
optimization = optimum_deluxe(4)


print(optimization.world.get_lists()[2])
print(optimization.world.check('Optimum Deluxe'))
print (optimization.world.text_grid())


optimization.connect_all_houses()




print(optimization.world.get_lists()[2])
print(optimization.world.check('Optimum Deluxe'))
print (optimization.world.text_grid())

optimization.connect_all_houses()

print(optimization.world.get_lists()[2])
print(optimization.world.check('Optimum Deluxe'))
print (optimization.world.text_grid())

optimization.relocate_untill_convergence()

print(optimization.world.get_lists()[2])
print(optimization.world.check('Optimum Deluxe'))
print (optimization.world.text_grid())

optimization.switch_houses_until_convergence()

print(optimization.world.get_lists()[2])
print(optimization.world.check('Optimum Deluxe'))
print (optimization.world.text_grid())
            
        
        