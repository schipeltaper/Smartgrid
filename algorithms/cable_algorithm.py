'''
* Cable class
* 
*
* Programmeertheorie
* Optimum Prime
*
*
* This file contains the Cable class, which is used to lay cables to connect houses with batteries
* inside the grid.
* 
*
'''


import random

from classes.cable import Cable_instance
from classes.cable import Cable_line


class Cable():
    '''
    Cable class contains an algorthm that lays cables between points inside the configuration.
    This class is initialised with an configuration class instance. After which the cable_list_batteries
    funtion is called. This itterates through the batteries inputted, which already has to be filled with 
    houses. The houses in the batteries are connected using a cable. These cables are loaded into the 
    all_cables variable in configuration class.

    Initialisation requires a configuration instance.
    '''
    
    def __init__(self, district_instance):
        self.cable_network = []

        self.district_instance = district_instance
    

    def cable_list_batteries(self, batteries, cable_sharing):
        '''
        Iterates through the batteries inputted and inputs the individual batteries and cable
        sharing boolian into the connect_battery_houses function.

        Input: list of batteries and a boolian that indicates if cable sharing is allowed 
        (True means cable sharing is allowed).
        '''   

        for battery in batteries:
            self.connect_battery_houses(battery, cable_sharing)
    

    def connect_battery_houses(self, battery, cable_sharing):
        '''
        Calls connecting_cables if cable_sharing is True, inputting a list of houses pulled from
        the inputted batteries, the list of batteries and the radius. Than adds cable to cable_network
        and too the all_cables variable in the configuration. If cable_sharing is not True than
        manhattan_dist_cable is called, which is given a battery and a house. The cables are put inside
        the all_cables variable in the configuration.

        Input: a battery and a boolian that indicates if cable sharing is allowed 
        (True means cable sharing is allowed).
        '''   

        # adds cables into district using shared cables
        if cable_sharing is True:
            self.list_houses = battery.houses_in_battery
            battery.list_cables.append(self.connecting_cables(self.list_houses, battery, 10))
            self.add_cable = self.connecting_cables(self.list_houses, battery, 10)
            for self.cable in self.add_cable:
                self.cable_network.append(self.cable)
                self.district_instance.all_cables.append(self.cable)

        # adds cables into district using individual cables
        else:
            for house in battery.houses_in_battery:
                battery.list_cables.append(self.manhattan_dist_cable(battery, house))
                self.add_cable = self.manhattan_dist_cable(battery, house)
                self.cable_network.append(self.add_cable)
                self.district_instance.all_cables.append(self.add_cable)


    def manhattan_dist_cable(self, start, end):
        '''
        Draws the shortest route for every point shortest distance!!! cable between two 
        points using the manhattan distance. The manhatten cable distances is the distance 
        between two points measured using a grid to connect the two points.

        Input: starting and ending objects with position_x and position_y variables.
        
        Output: Cable_line object with a list of Cable_instance's inside its 
        cable_coordinates variable. This object will also save the start and end of 
        the cable inside the start and end variable respectively.
        '''

        # saves the variables used in function
        self.current_point = Cable_instance(start.position_x, start.position_y)
        self.end_point = Cable_instance(end.position_x, end.position_y)
        self.former_point = Cable_instance(start.position_x, start.position_y)
        self.current_cable = Cable_line(self.current_point)

        # run while end point not found
        while (self.current_point.position_x != self.end_point.position_x) or \
            (self.current_point.position_y != self.end_point.position_y):

            # remembers former point and adds all option too cable_options
            self.former_point = self.current_point
            self.cable_options = []
            if self.current_point.position_x - self.end_point.position_x < 0:
                self.cable_options.append(Cable_instance(self.current_point.position_x + 1, self.current_point.position_y))
            else:
                self.cable_options.append(Cable_instance(self.current_point.position_x - 1, self.current_point.position_y))
            if self.current_point.position_y - self.end_point.position_y < 0:
                self.cable_options.append(Cable_instance(self.current_point.position_x, self.current_point.position_y + 1))
            else:
                self.cable_options.append(Cable_instance(self.current_point.position_x, self.current_point.position_y - 1))

            # chooses next cable point based on shortest direct distance to the end point and adds that point to the cable
            if self.calculate_distance(self.cable_options[0], self.end_point) \
            < self.calculate_distance(self.cable_options[1], self.end_point):
                self.current_point = self.cable_options[0]
                self.current_cable.add_cable_instance(self.cable_options[0])
            else:
                self.current_point = self.cable_options[1]
                self.current_cable.add_cable_instance(self.cable_options[1])
            
            # update cable_instance's within cable
            self.former_point.next_cable_inst = self.current_point
            self.current_point.former_cable_inst = self.former_point
            
        # returns Cable_line object with a list of Cable_instance inside cable_coordinates
        return self.current_cable


    def connecting_cables(self, houses, battery, range):
        '''
        Chooses a random house in the battery, than finds the middle point between all houses inside 
        the choosen radius around that randomly choosen house. Draws a cable between that middle point
        and the battery. Than draws a cable between every house inside radius with the middelpoint and
        adds the first cable instance of the main cable too the last cable instance of those individual
        house cables. Cable sharing means that multiple houses can connect to a common cable to connect 
        to a battery.

        Input: A list of houses, a battery, and a radius that allows houses within that radius 
        around a randomly choosen house to be connected.

        Output: a list of cables of Cable_line class
        '''
        
        # store the different lists that houses pass through to be connected
        self.houses_not_connected = houses.copy()
        self.too_connect = []
        self.houses_connected = []
        self.all_new_cables = []
        
        # chooses random not connected house, calculates the range and adds cooridinates values into avarage variables
        while not(self.houses_not_connected == []):
            self.a_house = random.choice(self.houses_not_connected)         
            if self.a_house not in self.houses_not_connected:
                continue
            self.x_min = self.a_house.position_x - range
            self.x_max = self.a_house.position_x + range
            self.y_min = self.a_house.position_y - range
            self.y_max = self.a_house.position_y + range
            self.average_x = self.a_house.position_x
            self.average_y = self.a_house.position_y
            
            # moves houses within range from houses_not connected too too_connect list
            self.too_connect.append(self.a_house)
            self.houses_not_connected.remove(self.a_house)
            for self.connect_house in self.houses_not_connected:
                if (self.x_min < self.connect_house.position_x < self.x_max) and \
                (self.y_min < self.connect_house.position_y < self.y_max):
                    self.too_connect.append(self.connect_house)
                    self.houses_not_connected.remove(self.connect_house)
                    self.average_x += self.connect_house.position_x
                    self.average_y += self.connect_house.position_y
            
            # calculates middelpoint between all houses in range and loads into cable_instance
            self.average_x /= (len(self.too_connect))
            self.average_y /= (len(self.too_connect))
            self.mid_point = Cable_instance(int(self.average_x), int(self.average_y))
            
            # layes cable between middle point and battery using the manhatten distance
            self.main_cable = self.manhattan_dist_cable(self.mid_point, battery)
            self.all_new_cables.append(self.main_cable)            
            
            # layes cable between houses and main cable
            for self.connect_house_now in self.too_connect:
                self.new_cable = self.manhattan_dist_cable(self.connect_house_now, self.mid_point)
                self.new_cable.add_cable_instance(self.main_cable.cable_coordinates[0])
                self.all_new_cables.append(self.new_cable)
            
            # moves connected houses from too_connect too houses_connected
            self.houses_connected.append(self.too_connect)
            self.too_connect.clear()
        
        # returns a lists of all cables used to connect all houses within radius to battery
        return self.all_new_cables


    def calculate_distance(self, obj_one, obj_two):
        '''
        Calculates the driect distance between two object. The direct distance between two objects 
        is calculated using a straight line.

        Input: Two objects with a position_x and position_y variable.
        
        Output: An intigure type that dindicates the length of a direct line between the objects
        '''

        return abs(obj_one.position_x - obj_two.position_x) + abs(obj_one.position_y - obj_two.position_y)

