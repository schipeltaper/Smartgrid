'''
* configuration and point class
*
* Programmeertheorie
* Optimum Prime
*
* The configuration class saves all information used to fill in the smartgrid and has
* a collection of functions to mutate the configuration and export results.
*
* The point class defines a point on the grid.
* This point saves all its neighbours which are connected through cables
*
'''


import os
import numpy as np
import json

from classes.house import House
from classes.battery import Battery
from scipy.sparse.csr import csr_matrix
from scipy.sparse.csgraph import dijkstra
from classes.map_lists import district_1, district_2, district_3, district_4


class Configuration():
    '''
    Configuration class defines a configuration of a smartgrid with a chosen width and height.
    In a configuration object you can add and delete batteries, houses and cables.
    In the configuration class we use a point-class to define the information on each point.
    Initialisation requires a district id.
    '''

    def __init__(self, district_id):
        # set district var
        if district_id == 1:
            self.district = district_1
        elif district_id == 2:
            self.district = district_2
        elif district_id == 3:
            self.district = district_3
        elif district_id == 4:
            self.district = district_4
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


    # to put the info of district1 into a configuration object
    def create_district(self):
        '''
        Loads all houses and all batteries inside the district into
        the configuration.
        '''

        self.all_houses = []
        self.all_batteries = []
        for self.house in self.district["houses"]:
            self.add_house(self.house)
        for self.battery in self.district["batteries"]:
            self.add_battery(self.battery)


    def lay_cables_in_configuration(self):
        '''
        Puts the cables in self.all_cables inside the configuration.
        '''

        for self.cable_line in self.all_cables:
            battery = self.configuration[self.cable_line.end.position_x][self.cable_line.end.position_y].battery_item
            if battery == None:
                battery = self.configuration[self.cable_line.start.position_x][self.cable_line.start.position_y].battery_item
            for self.cable_point in self.cable_line.cable_coordinates:
                self.configuration[self.cable_point.position_x][self.cable_point.position_y].cable_item.append(self.cable_point)


    def houses_with_ovorcapacity(self):
        '''
        Checks if there are any batteries with overcapacity crullently in all_batteries

        Returns: boolean, True if there are one or more batteries with over capacity
        '''

        for self.bat in self.all_batteries:
            if self.bat.battery_over_capacity():
                return True
        return False


    def refresh_config(self):
        '''
        Clears configuration and than updates it based on the batteries and houses
        inside the district and cables inside the all_cables variable.
        '''

        self.configuration.clear()
        for j in range(self.grid_height):
            row = []
            for i in range(self.grid_width):
                point = Point(j, i)
                row.append(point)
            self.configuration.append(row)
        self.create_district()
        self.lay_cables_in_configuration()


    def cal_costs(self):
        '''
        Uses the self.all_batteries list and self.all_cables to calculate the
        total costs of the configuration.
        '''

        self.refresh_config()
        self.total_costs = 0
        for self.battery in self.all_batteries:
            self.total_costs += self.battery.costs_battery
        for self.cable in self.all_cables:
            self.total_costs += self.cable.cal_cable_costs()

        return self.total_costs


    def add_battery(self, battery):
        '''
        Adds a battery to the configuration
        '''

        # adds the battery object to the points in the grid
        self.configuration[battery.position_x][battery.position_y].content = battery
        self.configuration[battery.position_x][battery.position_y].battery_item = battery

        # add battery to list of batteries if not there yet
        if battery not in self.all_batteries:
            self.all_batteries.append(battery)


    def add_house(self, house):
        '''
        Adds a house to the configuration
        '''
        # adds the house object to the points in the grid
        self.configuration[house.position_x][house.position_y].content = house
        self.configuration[house.position_x][house.position_y].house_item = house

        # add house to list of houses if not there yet
        if house not in self.all_houses:
            self.all_houses.append(house)


    def add_cable(self, point1, point2, battery):
        '''
        Adds a cable line to configuration
        '''
        # makes point2 the neighbour of point1
        if battery not in point1.neighbours:
            point1.neighbours[battery] = [point2]
        else:
            point1.neighbours[battery].append(point2)

        # makes point1 the neighbour of point2
        if battery not in point2.neighbours:
            point2.neighbours[battery] = [point1]
        else:
            point2.neighbours[battery].append(point1)


    def delete_battery(self, x, y):
        '''
        Delete a battery on a given point in the grid
        '''
        if type(self.configuration[x][y].content) is Battery:
            self.configuration[x][y].content = None


    def delete_house(self, x, y, house):
        '''
        Delete a house on a given point in the grid
        '''
        if type(self.configuration[x][y].content) is House:
            self.configuration[x][y].content = None


    def delete_cable(self, point1, point2, battery):
        '''
        Delete a cable on a given line segment in the grid
        '''
        point1.neighbours[battery].remove(point2)
        point2.neighbours[battery].remove(point1)


    def get_lists(self):
        '''
        get_lists iterates over the grid and puts all houses and batteries in lists
        format: houses = [[i,j,House],...]
        format: batteries = [[i,j,Battery,[cable,...]],...]
        format: cable = [[x_1,y_1],[x_2,y_2]]
        '''

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
            costs += battery[2].costs_battery
        return [batteries, houses, int(costs)]


    def text_grid(self):
        '''
        Prints text grid of configuration with batteries, houses and cables (for testing purposes).
        '''

        grid = ''
        for i in range(102):
            grid += '·' * 102
            grid += '\n'
        state = self.get_lists()
        batteries = state[0]
        houses = state[1]
        costs = state[2]
        for battery in batteries:
            i = (2 * battery[0]) * 103 + (2 * battery[1])
            grid = grid[:i] + 'B' + grid[i + 1:]
            for cable in battery[3]:
                char = '|'
                if abs(cable[0][0] - cable[1][0]) == 0:
                    char = '-'
                loc = [cable[0][0] + cable[1][0], cable[0][1] + cable[1][1]]
                i = (loc[0]) * 103 + (loc[1])
                grid = grid[:i] + char + grid[i + 1:]
        for house in houses:
            i = (2 * house[0]) * 103 + (2 * house[1])
            grid = grid[:i] + 'H' + grid[i + 1:]
        return grid


    def check(self, algorithm_name):
        '''
        Checks if configuration is valid and returns some parameters that have to do with the validity.
        '''

        # set height and width of grid
        height = len(self.configuration)
        width = len(self.configuration[0])
        grid_size = width * height

        # get lists of batteries and houses
        state = self.get_lists()
        batteries = state[0]
        houses = state[1]
        costs = state[2]

        #   check constraint 1: all houses belong to a battery
        all_houses_in_battery = False
        house_objs = set({})
        for house in houses:
            house_objs = house_objs.union([house[2]])
        houses_in_battery = set({})
        for battery in batteries:
            houses_in_battery = houses_in_battery.union(battery[2].houses_in_battery)
        if house_objs == houses_in_battery:
            all_houses_in_battery = True

        #  check constraint 2: all houses are connected to a battery by cables
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
            graph = csr_matrix((data, (row, col)), shape=(grid_size, grid_size))
            dist_matrix, predecessors = dijkstra(graph, directed=False, indices=[battery_index], return_predecessors=True)
            dijkstra_0 = predecessors[0]
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
        return [valid, all_houses_in_battery, bat_cap_not_exceeded, all_houses_connected, bat_cap_violation, houses_disconnected]


    def check50_neighbour_variant(self):
        '''
        Returns configuration in check50 format.
        '''

        # get all configuration info
        lists = self.get_lists()
        batteries0 = lists[0]
        costs = 0
        for battery in batteries0:
            costs += battery[2].costs_battery

        # initialize check50_format
        check50_format = [
          {
            "district": self.district_id,
            "shared-costs": costs
          }
        ]

        # put battery and house information in dictionaries conform check50.
        batteries = []
        for battery1 in batteries0:
            battery = battery1[2]
            batteries.append(battery)
        for battery in batteries:
            location = str(battery.position_x) + ',' + str(battery.position_y)
            bat_dict = {
                "location": location,
                "capacity": battery.capacity,
                "houses": []
            }
            house_locs = []
            houses = battery.houses_in_battery
            for house in houses:
                house_location = str(house.position_x) + ',' + str(house.position_y)
                house_dict = {
                    "location": house_location,
                    "output": house.production,
                    "cables": []
                  }
                house_locs.append([house.position_x, house.position_y, house_dict])

            # define paths in the check50 manner, put the paths in their houses, put the houses in their batteries, then check50 format is
            # complete.
            paths = []
            neighbours = []
            if battery in self.configuration[battery.position_x][battery.position_y].neighbours:
                neighbours = self.configuration[battery.position_x][battery.position_y].neighbours[battery]
            for neighbour in neighbours:
                paths.append([[battery.position_x, battery.position_y], [neighbour.x,neighbour.y]])
            while len(paths) > 0:
                for path in paths:
                    end_point = path[-1]
                    prev_point = path[-2]
                    orig_path = path
                    house_at_end = False
                    neighbours = []
                    if battery in self.configuration[end_point[0]][end_point[1]].neighbours:
                        neighbours = self.configuration[end_point[0]][end_point[1]].neighbours[battery]
                    neighbours1 = []
                    for neighbour in neighbours:
                        if neighbour.x == prev_point[0] and neighbour.y == prev_point[1]:
                            pass
                        else:
                            neighbours1.append([neighbour.x,neighbour.y])
                    for i in range(len(house_locs)):
                        if end_point[0] == house_locs[i][0] and end_point[1] == house_locs[i][1]:
                            path.reverse()
                            cable_list = []
                            for point in path:
                                cable_list.append(str(point[0]) + ',' + str(point[1]))
                            check50_format[0]["shared-costs"] += (len(cable_list)) * 9
                            house_locs[i][2]["cables"] = cable_list
                            bat_dict["houses"].append(house_locs[i][2])
                            for neighbour in neighbours1:
                                paths.append([end_point, neighbour])
                            house_at_end = True
                    if house_at_end == False:
                        path.append(neighbours1[0])
                        paths.append(path)
                        if len(neighbours1) > 1:
                            for excess_neighbour in neighbours1[1:]:
                                paths.append([end_point, excess_neighbour])
                    paths.remove(orig_path)
            check50_format.append(bat_dict)
        return check50_format


    def check50_neighbour_variant_own_costs(self):
        '''
        Returns configuration in check50 format.
        '''

        # get all configuration info
        lists = self.get_lists()
        batteries0 = lists[0]
        costs = 0
        for battery in batteries0:
            costs += battery[2].costs_battery

        # initialize check50_format
        check50_format = [
          {
            "district": self.district_id,
            "costs-own": costs
          }
        ]

        # put battery, house and cable information in dictionaries conform check50.
        batteries = []
        for battery1 in batteries0:
            battery = battery1[2]
            batteries.append(battery)
        for battery in batteries:
            bat_location = [battery.position_x, battery.position_y]
            location = str(bat_location[0]) + ',' + str(bat_location[1])
            bat_dict = {
                "location": location,
                "capacity": battery.capacity,
                "houses": []
            }
            houses = battery.houses_in_battery
            for house in houses:
                house_location_str = str(house.position_x) + ',' + str(house.position_y)

                house_location = [house.position_x, house.position_y]
                orientation_x = 1
                orientation_y = 1
                if bat_location[0] < house_location[0]:
                    orientation_x = -1
                if bat_location[1] < house_location[1]:
                    orientation_y = -1
                dist_x = abs(bat_location[0] - house_location[0])
                dist_y = abs(bat_location[1] - house_location[1])
                check50_format[0]["costs-own"] += 9 * (dist_x + dist_y + 1)
                cables = []
                for i in range(dist_x + 1):
                    cable = str(house_location[0] + i * orientation_x) + ',' + str(house_location[1])
                    cables.append(cable)
                for i in range(dist_y):
                    cable = str(bat_location[0]) + ',' + str(house_location[1] + (i + 1) * orientation_y)
                    cables.append(cable)


                house_dict = {
                    "location": house_location_str,
                    "output": house.production,
                    "cables": cables
                  }
                bat_dict["houses"].append(house_dict)
            check50_format.append(bat_dict)

        return check50_format


    def cs50_check(self, cable_shared):
        '''
        Uses the information saves inside all_cables, all_battieres and houses_in_battery inside
        each battery instance to create a list of dictionaries required for the check50.

        Input: boolean, True if cables are allowed to be shared

        Output: lists of dictionaries, [{information about the distric}, {information about batteries}...]
        '''

        # adds the information about the district into the check50_output list
        self.battery
        self.check50_output = [
        #   {
        #     "district": self.district_id,
        #     "costs-shared": self.cal_costs()
        #   }
        ]



        # stores lists of cable coordinates of all cables inside self.all_cables into a list self.list_of_lines
        self.list_of_lines = []
        for self.cable_line in self.all_cables:
            self.cable_line_loc = []
            for self.cable_point in self.cable_line.cable_coordinates:
                self.cable_point = [self.cable_point.position_x, self.cable_point.position_y]
                self.string_cable_loc = [str(coordinate) for coordinate in self.cable_point]
                self.cable_line_loc.append(",".join(self.string_cable_loc))
            self.list_of_lines.append(self.cable_line_loc)

        # stores all location and capcity of batteries inside the add_bat dictionary
        for self.bat in self.all_batteries:
            self.add_bat = {}
            self.location_bat = [self.bat.position_x, self.bat.position_y]
            self.string_loc_bat = [str(coordinate) for coordinate in self.location_bat]
            self.add_bat["location"] = ",".join(self.string_loc_bat)
            self.add_bat["capacity"] = self.bat.capacity
            self.add_bat["houses"] = []

            # place to store lists of cables already stored inside the houses
            self.main_cables = []
            self.house_cables = []

            # stores cooridnates and energy production of the house into the add_house_dict dictionary
            for self.house_in_bat in self.bat.houses_in_battery:
                self.add_house_dict = {}
                self.house_loc = [self.house_in_bat.position_x, self.house_in_bat.position_y]
                self.string_loc_house = [str(coordinate) for coordinate in self.house_loc]
                self.add_house_dict["location"] = (",".join(self.string_loc_house))
                self.add_house_dict["output"] = self.house_in_bat.production
                self.add_house_dict["cables"] = []

                # looking for the cable that starts at house coordinates inside all cables
                self.cable_adding_house = []
                for self.cable in self.list_of_lines:
                    self.cable_match_house = False
                    if self.cable[0] == self.add_house_dict["location"]:
                        self.add_house_dict["cables"] = self.cable
                        self.house_cables.append(self.add_house_dict["cables"])
                        self.cable_match_house = True

                    # also considers that a cable might have been layed reversely
                    elif self.cable[len(self.cable)-1] == self.add_house_dict["location"]:
                        self.add_house_dict["cables"] = list(reversed(self.cable))
                        self.house_cables.append(self.add_house_dict["cables"])
                        self.cable_match_house = True
                    else:
                        continue

                    # moves to next cable if house is connected directly to a battery
                    if self.add_house_dict["cables"][len(self.add_house_dict["cables"])-1] == self.add_bat["location"]:
                        continue

                    # looks for main cable that connects house too battery by combining main and house cable
                    for self.potential_main_cable in self.list_of_lines:
                        self.cable_with_bat_commen_point = []
                        if self.potential_main_cable[0] == self.add_house_dict["cables"][len(self.add_house_dict["cables"])-1]:
                            if self.potential_main_cable[len(self.potential_main_cable)-1] == self.add_bat["location"]:
                                self.cable_with_bat_commen_point = self.potential_main_cable
                        elif self.potential_main_cable[len(self.potential_main_cable)-1] == self.add_house_dict["cables"][len(self.add_house_dict["cables"])-1]:
                            if self.potential_main_cable[0] == self.add_bat["location"]:
                                self.cable_with_bat_commen_point = list(reversed(self.potential_main_cable))

                        # adds main cable too house calbe if the main cable not already inside check50_output
                        if not(self.cable_with_bat_commen_point in self.main_cables):
                            self.main_cables.append(self.cable_with_bat_commen_point)
                            self.add_house_dict["cables"] += self.cable_with_bat_commen_point

                # get rid of dubble coordinates inside cable lists due to connections
                self.cable_temp_list = []
                for self.temp_cable_loc in self.add_house_dict["cables"]:
                    if not(self.temp_cable_loc in self.cable_temp_list):
                        self.cable_temp_list.append(self.temp_cable_loc)

                # updates check50_output with cables into houses and houses into batteries and batteries into check50_output
                self.add_house_dict["cables"] = self.cable_temp_list
                self.add_bat["houses"].append(self.add_house_dict)
            self.check50_output.append(self.add_bat)

        # returns the check50_output
        return self.check50_output


class Point():
    '''
    This class defines a point on the grid. It has all the information for that
    specific coordinate. It is initialized with an x- and y-coordinate.
    '''

    def __init__(self, x, y):
        self.x = x
        self.y = y

        # if a cable goes through this point, shows all neighbours of this point for each relevant battery
        self.neighbours = dict()

        # the content on this point. Could be a house or a battery
        self.content = None

        # place to store all information
        self.cable_item = []
        self.battery_item = None
        self.house_item = None