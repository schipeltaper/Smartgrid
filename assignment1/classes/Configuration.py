'''
* configuration and point class
*
* Programmeertheorie
* Optimum Prime
*
* Configuration class defines a configuration of a smartgrid with a chosen width and height.
* In a configuration object you can add and delete batteries, houses and cables.
* In the configuration class we use a point-class to define the information on each point.
*
* The point class defines a point on the grid.
* This point saves all its neighbours which are connected through cables
*
'''

import os
from classes.House import House
from classes.Battery import Battery
import numpy as np
from scipy.sparse.csr import csr_matrix
from scipy.sparse.csgraph import dijkstra
from classes.map_lists import district_1, district_2, district_3

# Class defines a configuration of a world on a determined sized grid, with houses, batteries and cables.
class Configuration():
    def __init__(self, district_id):
        # set district var
        if district_id == 1:
            self.district = district_1
        elif district_id == 2:
            self.district = district_2
        elif district_id == 3:
            self.district = district_3
        else:
            return False
        
        # saving grid information
        self.grid_width = 51
        self.grid_height = 51

        # saving grid content information
        self.all_batteries = []
        self.all_houses = []
        self.all_cables = []
        self.district_id = district_id
        
        # Creates a correctly sized grid of points
        self.configuration = []
        for j in range(self.grid_height):
            row = []
            for i in range(self.grid_width):
                point = Point(j, i)
                row.append(point)
            self.configuration.append(row)
        
        self.visualise_grid = []
        
        # loading in all houses & batteries
        self.create_district()

        self.houses_with_ovorcapacity()
    
    # returns True if there are one or more batteries over capacity
    def houses_with_ovorcapacity(self):
        #  make batteries not over capacity
        for self.bat in self.all_batteries:
            if self.bat.battery_over_capacity():
                return True
            return False
    
    def refresh_config(self):

        self.configuration.clear()

        # reloading all points
        for j in range(self.grid_height):
            row = []
            for i in range(self.grid_width):
                point = Point(j, i)
                row.append(point)
            self.configuration.append(row)

        # loading in all houses & batteries
        self.create_district()

        self.lay_cables_in_configuration()
    
    # calculating total costs of configuration
    def cal_costs(self):

        # put houses and batteries in grid
        self.refresh_config()
        self.total_costs = 0

        for self.battery in self.all_batteries:
            self.total_costs += self.battery.costs_battery

        for self.cable in self.all_cables:
            self.total_costs += self.cable.cal_cable_costs()
        
        return self.total_costs

    def print_the_dam_thing(self):
        
        self.refresh_config()
        self.load_hb_in_beta_visiualisation()
        self.load_cables_in_beta_visiualisation()

        # itterate through visualise_grid y_axis
        for self.y_axis in self.visualise_grid:
            
            # itterate through visualise_grid x_axis
            for self.x_axis in self.y_axis:
                print(self.x_axis, end = '')
            
            # print next line
            print()

    # load houses and batteries into visiualisation without cables
    def load_hb_in_beta_visiualisation(self):
                
        # itterate through the lenght
        for self.y_axis_lines in self.configuration:

            self.y_axis_row1 = []
            self.y_axis_row2 = []
            
            # itterate through the width
            for self.x_axis_lines in self.y_axis_lines:
                
                # display B if battery present
                if self.x_axis_lines.battery_item is not None:
                    self.y_axis_row1.append("B")
                    
                # display H if house present
                elif self.x_axis_lines.house_item is not None:
                    self.y_axis_row1.append("H")
                    
                # display . if neither battery nor house present
                else:
                    self.y_axis_row1.append(".")
                
                self.y_axis_row1.append(".")
                self.y_axis_row2.append(".")
                self.y_axis_row2.append(".")
            
            # adding items to grid in visualise_grid
            self.visualise_grid.append(self.y_axis_row1)
            self.visualise_grid.append(self.y_axis_row2)

    # loads cables into array of visualisation
    def load_cables_in_beta_visiualisation(self):
        
        # itterating through configuration
        for self.y_axis in self.configuration:
            for self.x_axis in self.y_axis:

                # find coordinates of the cable
                if self.x_axis.cable_item != []:
                    for self.cable_point in self.x_axis.cable_item:

                        # get direction of cable
                        self.cable_direction = self.cable_point.determine_direction_cable()
                        
                        # add cable to visualise_grid
                        if self.cable_direction == "EMPTY":
                            continue
                        
                        # ok so the up, down, left and right are all wrong but now it prints it good
                        elif self.cable_direction == "UP":
                            # UP 
                            self.visualise_grid[self.cable_point.position_x*2][self.cable_point.position_y*2-1] = "-"

                        elif self.cable_direction == "DOWN":
                            # DOWN
                            self.visualise_grid[self.cable_point.position_x*2][self.cable_point.position_y*2+1] = "-"

                        elif self.cable_direction == "LEFT":
                            # LEFT
                            self.visualise_grid[self.cable_point.position_x*2-1][self.cable_point.position_y*2] = "|"

                        elif self.cable_direction == "RIGHT":
                            # RIGHT
                            self.visualise_grid[self.cable_point.position_x*2+1][self.cable_point.position_y*2] = "|"
    
    
    # to put the info of district1 into a configuration object
    def create_district(self):
        
        self.all_houses = []
        self.all_batteries = []

        for self.house in self.district["houses"]:
            self.add_house(self.house)

        for self.battery in self.district["batteries"]:
            self.add_battery(self.battery)

    # adds multiple batteries to the configuration
    def add_multiple_batteries(self, batteries):
        for self.battery_put in batteries:
            self.add_battery(self.battery_put)
    
    def add_battery(self, battery):   
        
        # adds battery to configuration
        self.configuration[battery.position_x][battery.position_y].content = battery
        self.configuration[battery.position_x][battery.position_y].battery_item = battery

        # add battery to list of batteries if not there yet
        if battery not in self.all_batteries:
            self.all_batteries.append(battery)

    def add_house(self, house):
        # adds house to configuration
        self.configuration[house.position_x][house.position_y].content = house
        self.configuration[house.position_x][house.position_y].house_item = house

        # add house to list of houses if not there yet
        if house not in self.all_houses:
            self.all_houses.append(house)

    # adding a cable line to configuration
    def lay_cables_in_configuration(self):
        for self.cable_line in self.all_cables:
            for self.cable_point in self.cable_line.cable_coordinates:
                self.configuration[self.cable_point.position_x][self.cable_point.position_y].cable_item.append(self.cable_point)
    
    def add_cable(self, point1, point2, battery):
        if point1.neighbours[battery] is None:
            point1.neighbours[battery] = [point2]
        else:
            point1.neighbours[battery].append(point2)

        if point2.neighbours[battery] is None:
            point2.neighbours[battery] = [point1]
        else:
            point2.neighbours[battery].append(point1)

    def delete_battery(self, x, y):
        if type(self.configuration[x][y].content) is Battery:
            self.configuration[x][y].content = None

    def delete_house(self, x, y, house):
        if type(self.configuration[x][y].content) is House:
            self.configuration[x][y].content = None

    def delete_cable(self, point1, point2, battery):
        point1.neighbours[battery].remove(point2)
        point2.neighbours[battery].remove(point1)
        
    def get_lists(self):
        # get_lists iterates over the grid and puts all houses and batteries in lists
        # format: houses = [[i,j,House],...]
        # format: batteries = [[i,j,Battery,[cable,...]],...]
        # format: cable = [[x_1,y_1],[x_2,y_2]]
        
        # put all batteries and houses in grid in lists and calculate costs
        costs = 0
        batteries = []
        houses = []
        for i in range(len(self.configuration)):
            row = []
            for j in range(len(self.configuration[0])):
                if isinstance(self.configuration[i][j].content, Battery):
                    batteries.append([i,j,self.configuration[i][j].content,[]])
                if isinstance(self.configuration[i][j].content, House):
                    houses.append([i,j,self.configuration[i][j].content])
        
        # put all cables in battery
        for i in range(len(self.configuration)):
            row = []
            for j in range(len(self.configuration[0])):
                for k in range(len(batteries)):
                    neighbours = []
                    if batteries[k][2] in self.configuration[i][j].neighbours:
                        neighbours = self.configuration[i][j].neighbours[batteries[k][2]]
                    for neighbour in neighbours:
                        batteries[k][3].append([[i,j],[neighbour.x,neighbour.y]])
                        costs += 9/2
                        
        for battery in batteries:
            costs += battery[2].costs
                    
        # updating the information of the grid
        self.all_batteries = batteries
        self.all_houses = houses
        
        return [batteries, houses, int(costs)]
        
    def check(self, algorithm_name):
        # check if configuration is valid
        
        # check district_id
        
        if self.district_id not in [1,2,3]:
            return('Set district_id!')
        
        # set height and width of grid
        height = len(self.configuration)
        width = len(self.configuration[0])
        N = width * height
        
        # get lists of batteries and houses
        state = self.get_lists()
        batteries = state[0]
        houses = state[1]
        costs = state[2]

        #for house in houses:
        #    batteries[0][2].add_house(house[2])
        
        #   constraint 1: all houses are belong to a battery
        all_houses_in_battery = False
        house_objs = set({})
        for house in houses:
            house_objs = house_objs.union([house[2]])
        
        houses_in_battery = set({})
        for battery in batteries:
            houses_in_battery = houses_in_battery.union(battery[2].houses_in_battery)
        
        if house_objs == houses_in_battery:
            all_houses_in_battery = True
        
        #   constraint 2: are houses are connected to a battery by cables 
        
        houses_disconnected = len(houses)
        for battery in batteries:
            row = []
            col = []
            data = []
            
            for cable in battery[3]:
                row.append(cable[0][0] * width + cable[0][1])
                col.append(cable[1][0] * width + cable[1][1])
                data.append(1)
            
            battery_index = battery[0] * width + battery[1]
            graph = csr_matrix((data, (row, col)), shape=(N, N))
            
            dijkstra_0 = dijkstra_algo(graph,[battery_index])[1][0]
            houses = battery[2].houses_in_battery
            for house in houses:
                i = house.position_x
                j = house.position_y
                if dijkstra_0[i * width + j] != -9999:
                    houses_disconnected -= 1
        
        all_houses_connected = False
        if houses_disconnected == 0:
            all_houses_connected = True
        
        #   constraint 3: battery capacity is not exceeded 
        bat_cap_violation = 0
        for battery in batteries:
            battery = battery[2]
            bat_cap_violation += max(0,(battery.energy_production - battery.capacity)) ** 2
        
        bat_cap_not_exceeded = False
        if bat_cap_violation == 0:
            bat_cap_not_exceeded = True
    
        valid = False
        if all_houses_in_battery and bat_cap_not_exceeded and all_houses_connected:
            valid = True
            self.result_reg(costs,algorithm_name)
        
        # if valid and costs are smallest ever, save solution
        
        
        return [valid, all_houses_in_battery, bat_cap_not_exceeded, all_houses_connected, bat_cap_violation, houses_disconnected]
    
    def result_reg(self, costs, class_name):
        district_id = self.district_id
        with open("../results.txt","r") as f:
            new_file = ''
            f.seek(0)
            rank = 1
            new_cost_placed = False
            for i in range(34):
                line = f.readline()
                if(-1 < i + 9 - 11 * district_id < 10):
                    rank_cost = int(line[11:17])
                    if rank_cost > costs and new_cost_placed == False and rank < 11:
                        costs_str = str(costs).zfill(6)
                        row = str(rank).zfill(2) + ': costs: ' + costs_str + ', algorithm: ' + str(class_name)
                        new_file += row + '\n'
                        rank += 1
                        new_cost_placed = True
                    if rank < 11:
                        row = str(rank).zfill(2) + line[2:-1]
                        new_file += row + '\n'
                        rank += 1
                else:
                    new_file += line
            f.close()
        with open("../results.txt", 'w') as f2:
            f2.seek(0)
            f2.write(new_file)
            f2.close()

class Point():
    def __init__(self, x, y):
        # Shows the position of this point
        self.x = x
        self.y = y

        # If a cable goes through this point, shows all neighbours of this point for each relevant battery
        self.neighbours = dict()

        # The content on this point. Could be a house or battery
        self.content = None

        # place to store all things
        self.cable_item = []
        self.battery_item = None
        self.house_item = None