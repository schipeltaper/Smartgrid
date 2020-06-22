'''
* Visualization class
*
*
* Programmeertheorie
* Optimum Prime
*
* Visualization class, creates a visualization of the world with houses, batteries and cables.
* For the initialization of a Visualization object, we input a configuration object.
* This class is used by calling the function show, which then visualizes the configuration.
*
'''

import numpy as np
import matplotlib.pyplot as plt


from classes.Battery import Battery
from classes.house import House
from classes.Configuration import *
from classes.map_lists import district_1, district_2, district_3

class Visualization():
    '''
    Initialization requires a Configuration object
    '''
    def __init__(self, configuration):
        self.configuration = configuration
        # self.battery = battery

    def show(self):

        '''
        The show function determines the coordinates of all houses, batteries and cables
        Then function then creates a grid with length and width such as in the configuration object.
        Then the the function plots the information using pyplot.
        '''

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        houses = [(x, y) for x in range(self.configuration.grid_width) for y in range(self.configuration.grid_height) if type(self.configuration.configuration[x][y].content) is House]
        batteries = [(x, y) for x in range(self.configuration.grid_width) for y in range(self.configuration.grid_height) if type(self.configuration.configuration[x][y].content) is Battery]

        houses_x = list(map(lambda x: x[0], houses))
        houses_y = list(map(lambda x: x[1], houses))

        batteries_x = list(map(lambda x: x[0], batteries))
        batteries_y = list(map(lambda x: x[1], batteries))

        plt.scatter(houses_x, houses_y)
        plt.scatter(batteries_x, batteries_y)

        # Major ticks every 20, minor ticks every 5
        minor_ticks_x = np.arange(0, self.configuration.grid_width, 1)
        minor_ticks_y = np.arange(0, self.configuration.grid_height, 1)

        ax.set_xticks(minor_ticks_x, minor=True)
        ax.set_yticks(minor_ticks_y, minor=True)

        # And a corresponding grid
        ax.grid(which='both')

        # Or if you want different settings for the grids:
        ax.grid(which='minor', alpha=0.2)
        ax.grid(which='major', alpha=0.5)

        plt.show()