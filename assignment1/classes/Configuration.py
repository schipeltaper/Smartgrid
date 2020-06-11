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

from House import House
from Battery import Battery
import sys
import os
import numpy as np
sys.path.append(os.path.abspath('../algorithms'))
from Algorithms import dijkstra_algo
from scipy.sparse import csr_matrix

# Class defines a configuration of a world on a determined sized grid, with houses, batteries and cables.
class Configuration():
    def __init__(self, width, height):

        # Creates a correctly sized grid of points
        self.configuration = []
        for j in range(height):
            row = []
            for i in range(width):
                point = Point(j, i)
                row.append(point)
            self.configuration.append(row)

    # to put the info of district1 into a configuration object
    def create_district(self, district_info):
        for house in district_info["houses"]:
            self.add_house(house.position_x, house.position_y, house)

        for battery in district_info["batteries"]:
            self.add_battery(battery.position_x, battery.position_y, battery)

    def add_battery(self, x, y, battery):
        self.configuration[x][y].content = battery

    def add_house(self, x, y, house):
        self.configuration[x][y].content = house

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
                    
        return [batteries, houses, int(costs)]
        
    def check(self):
        # check if configuration is valid
        
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
    
        # if valid and costs are smallest ever, save solution
        
        valid = False
        if all_houses_in_battery and bat_cap_not_exceeded and all_houses_connected:
            valid = True
        
        return [valid, all_houses_in_battery, bat_cap_not_exceeded, all_houses_connected, bat_cap_violation, houses_disconnected]


class Point():
    def __init__(self, x, y):
        # Shows the position of this point
        self.x = x
        self.y = y

        # If a cable goes through this point, shows all neighbours of this point for each relevant battery
        self.neighbours = dict()

        # The content on this point. Could be a house or battery
        self.content = None

