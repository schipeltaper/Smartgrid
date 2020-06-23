'''
* Visualization class
*
*
* Programmeertheorie
* Optimum Prime
*
* The Check_to_visualization class creates a visualization of all the houses, batteries and cables of a result.
'''

import matplotlib.pyplot as plt

import json
import numpy as np

def main():
    Check50_to_visualization('../results/output.json')

class Check50_to_visualization():
    '''
    The initialization requires a json file which contains a solution in the format of a
    check50 input. We have imported pyplot to be able to make a more official looking
    visualization.
    '''
    def __init__(self, check50_format_json):
        # we save the list which represents the result in self.check50_format
        with open(check50_format_json) as json_file:
            self.check50_format = json.load(json_file)

        # creates figure object
        fig = plt.figure()

        # adds axes to the figure
        ax = fig.add_subplot(1, 1, 1)

        # we will store all the coordinates in three lists
        houses = []
        batteries = []
        cables = []

        # saving all battery-coordinates
        for battery_index in range(1, len(self.check50_format)):
            battery = self.check50_format[battery_index]["location"].split(",")
            batteries.append((int(battery[0]), int(battery[1])))

            # saving all house-coordinates
            for house_info in self.check50_format[battery_index]["houses"]:
                house = house_info["location"].split(",")
                houses.append((int(house[0]), int(house[1])))

                # saving all cable-coordinates
                for cable_segment in house_info["cables"]:
                    cable = cable_segment.split(",")
                    cables.extend([int(cable[0]), int(cable[1])])
                cables.append("end cable sequence")

        # creates the lists for all x- and y-coordinates for houses and batteries
        houses_x = list(map(lambda x: x[0], houses))
        houses_y = list(map(lambda x: x[1], houses))
        batteries_x = list(map(lambda x: x[0], batteries))
        batteries_y = list(map(lambda x: x[1], batteries))

        # using the scatter function, plots the houses (blue) and batteries (orange)
        plt.scatter(houses_x, houses_y)
        plt.scatter(batteries_x, batteries_y)

        # plots all the cables
        index = 0
        while index < len(cables):
            # plots all cable sequences seperately
            if cables[index + 2] == "end cable sequence":
                index += 3
            else:
                plt.plot([cables[index], cables[index + 2]], [cables[index + 1], cables[index + 3]], 'k-', lw = 0.5)
                index += 2

        # makes sure we have a 51 by 51 grid
        minor_ticks_x = np.arange(0, 51, 1)
        minor_ticks_y = np.arange(0, 51, 1)

        # makes sure we have a line for each row and column in the grid
        ax.set_xticks(minor_ticks_x, minor=True)
        ax.set_yticks(minor_ticks_y, minor=True)

        # makes the lines a little less bright
        ax.grid(which='minor', alpha=0.3)
        ax.grid(which='major', alpha=0.3)

        # shows the plot that has been made
        plt.show()

if __name__ == "__main__":
    main()
