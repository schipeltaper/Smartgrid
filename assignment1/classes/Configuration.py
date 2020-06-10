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

# Class defines a configuration of a world on a determined sized grid, with houses, batteries and cables.
class Configuration():
    def __init__(self, width, height):

        self.height_district = height

        self.width_disditrict = width
        
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


class Point():
    def __init__(self, x, y):
        # Shows the position of this point
        self.position_x = x
        self.position_y = y

        # If a cable goes through this point, shows all neighbours of this point for each relevant battery
        self.neighbours = dict()

        # The content on this point. Could be a house or battery
        self.content = None
