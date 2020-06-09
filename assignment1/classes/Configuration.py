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

from Battery import Battery
from House import House

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

    def add_battery(self, x, y, battery):
        self.configuration[x][y].content = battery

    def add_house(self, x, y, house):
        self.configuration[x][y].content = house

    # Cables are saved by saving the neighbours of each point
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
        if type(self.configuration[x][y].content) == 'Battery.Battery':
            self.configuration[x][y].content = None

    def delete_house(self, x, y, house):
        if type(self.configuration[x][y].content) == 'House.House':
            self.configuration[x][y].content = None

    def delete_cable(self, point1, point2, battery):
        point1.neighbours[battery].remove(point2)
        point2.neighbours[battery].remove(point1)

# Defines a point on the grid
class Point():
    def __init__(self, x, y):
        # Shows the position of this point
        self.x = x
        self.y = y

        # If a cable goes through this point, shows all neighbours of this point for each relevant battery
        self.neighbours = dict()

        # The content on this point. Could be a house or battery
        self.content = None



