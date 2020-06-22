
from classes.Battery import Battery
from classes.House import House
from classes.map_lists import district_1, district_2, district_3, district_test
from algorithms.greedy_algorithm import Greedy
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance
from classes.Configuration import Configuration
from algorithms.hill_climber import Hill_climber
from algorithms.simulated_annealing import simulated_annealing
import numpy as np
import copy

class Combining_algorithms():

    def __init__(self, district_numb):
        self.the_district = Configuration(district_numb)
        self.the_district.create_district()

    # Greedy_house allocation & Astar cable drawing - assumption 1 cable 1 house
    def greedy_house_astar_cable(self):

        # creating an instant to save greedy object
        self.greedy_house_devide = Greedy(self.the_district)

        # deviding houses amoung batteries using proximity
        self.greedy_house_devide.proximity_sort()

        # save the cable algorithm object
        self.astar_cable = Cable(self.the_district)

        # laying cables for every battery between its own houses
        self.astar_cable.cable_list_batteries(self.the_district.all_batteries, False)

        print(f"The total costs of greedy astar: {self.the_district.cal_costs()}")

        self.the_district.cal_costs()
        print(f"The total costs of greedy astar: {self.the_district.total_costs}")

    # simulated annealing hill climber
    def annealing_hill_climber(self):
        # creating an instant to save greedy object
        self.annealing_house_devide1 = simulated_annealing(self.the_district)

        # deviding houses among batteries using
        self.annealing_house_devide1.creating_starting_possition()
        self.annealing_house_devide1.running_simulated_annealing()

        self.hill = Hill_climber(self.the_district)

        self.hill.climb_the_hill()

        print(f"Final total costs of simulated annealing hill climber: {self.the_district.cal_costs()}")

    # simulated anealing house distribution & Astar cable drawing - assumption 1 cable 1 house
    def simulated_annealing_house_astar_cable(self):
        self.sa_distribution = simulated_annealing(self.the_district)
        self.sa_distribution.creating_starting_possition()
        self.sa_distribution.running_simulated_annealing(True)
        self.astar_cable2 = Cable(self.the_district)

        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, True)

        self.the_district.print_the_dam_thing()

        print(f"The total costs simulated annealing astar: {self.the_district.cal_costs()}")

    def random_greedy_astar_cable(self, rounds):
        self.random_greedy = Greedy(self.the_district)
        self.random_greedy.random_greedy(rounds)

        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, False)

        return self.the_district.cal_costs()

    # simulated anealing house distribution & Astar cable sharing drawing - assumption cable sharing
    def sa_cable_share_astar(self):
        self.sa_distribution = simulated_annealing(self.the_district)
        self.sa_distribution.creating_starting_possition()
        self.sa_distribution.running_simulated_annealing(True)
        self.astar_cable2 = Cable(self.the_district)
        self.astar_cable2.cable_list_batteries(self.the_district.all_batteries, True)
        self.the_district.print_the_dam_thing()

        print(f"The total costs simulated annealing astar: {self.the_district.cal_costs()}")

# calculate costs for list of batteries Get rid of this!!!!!!!!!!!!!!!!!!!
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs



# optimum_deluxe optimizes in 3 steps. 
# 1: connect the house that is the cheapest to a battery, repeat untill all houses are connected. 
# 2: relocate the house that results in the lowest cost per decreased battery violation, repeat untill convergence.
# 3: switch the pair of houses that results in the lowest cost per decreased battery violation, repeat untill convergence.

class optimum_deluxe():
    def __init__(self, district_id):
        self.world = Configuration(district_id)
    
    # connect house to battery the cheapest way
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
    
    # disconnect house (also removes excess cable)
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
    
    # returns neigbours in list
    def neighbours_list(self, point, battery):
        neighbours = []
        if battery in point.neighbours:
            neighbours = point.neighbours[battery]
        return neighbours
    
    # checks what it would cost to connect a house to a battery
    def check_costs_to_connect_house_to_battery(self, house, battery):
        costs = self.world.get_lists()[2]
        self.connect_house(self.world, house, battery)
        new_costs = self.world.get_lists()[2]
        self.disconnect_house(self.world, house, battery)
        return new_costs - costs
    
    # returns lists of house that are not connected to a battery and all batteries
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
    
    # connect the house that is the cheapest to connect
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
            print(self.world.get_lists()[2])
            print(self.world.check('Optimum Deluxe'))
            print (self.world.text_grid())
            return True
    
    # connect the cheapest house untill all houses are connected
    def connect_all_houses(self):
        while self.connect_cheapest_house():
            pass
    
    # check what it would cost to relocate a battery to another battery and what the decrease of the battery capacity violation would be    
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
    
    # relocate the house that results in the lowest cost per decreased battery violation
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
            print(self.world.get_lists()[2])
            print(self.world.check('Optimum Deluxe'))
            print (self.world.text_grid())
            return True
    
    # relocate houses untill convergence
    def relocate_untill_convergence(self):
        while self.do_best_relocation_of_house():
            pass
    
    # switch houses (between two batteries)
    def switch_houses(self, world, battery_1, house_1, battery_2, house_2):
        self.disconnect_house(world, house_1, battery_1)
        self.disconnect_house(world, house_2, battery_2)
        self.connect_house(world, house_1, battery_2)
        self.connect_house(world, house_2, battery_1)
    
    # check what it would cost to switch two houses between batteries
    def check_costs_to_switch_houses(self, battery_1, house_1, battery_2, house_2):
        old_costs = self.world.get_lists()[2]
        old_bat_violation = self.world.check('Optimum Deluxe')[4]
        self.switch_houses(self.world, battery_1, house_1, battery_2, house_2)
        new_costs = self.world.get_lists()[2]
        new_bat_violation = self.world.check('Optimum Deluxe')[4]
        bat_gained = old_bat_violation - new_bat_violation
        extra_costs = new_costs - old_costs
        self.switch_houses(self.world, battery_2, house_1, battery_1, house_2)
        return bat_gained, extra_costs
    
    # perform the switch of houses that results in the lowest cost per decreased battery violation
    def do_best_switch_of_houses(self):
        houses, batteries = self.get_disconnected_houses_and_all_batteries(self.world)
        battery0_1 = None
        battery0_2 = None
        house0_1 = None
        house0_2 = None
        min_cost_per_bat_gained = float('inf')
        for i in range(len(batteries)):
            houses_3 = copy.copy(batteries[i].houses_in_battery)
            for house_1 in houses_3:
                for j in range(len(batteries)):
                    if(j != i):
                        houses_4 = copy.copy(batteries[j].houses_in_battery)
                        for house_2 in houses_4:
                            bat_gained, extra_costs = self.check_costs_to_switch_houses(batteries[i], house_1, batteries[j], house_2)
                            if bat_gained > 0:
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
            self.switch_houses(self.world, battery0_1, house0_1, battery0_2, house0_2)
            print(self.world.get_lists()[2])
            print(self.world.check('Optimum Deluxe'))
            print (self.world.text_grid())
            return True
    # switch houses untill battery violation is zero
    def switch_houses_until_convergence(self):
        while self.do_best_switch_of_houses():
            pass
    # run algorithm    
    def run(self):
        self.connect_all_houses()
        self.relocate_untill_convergence()
        self.switch_houses_until_convergence()
        


            
        
        
