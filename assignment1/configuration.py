# Class defines a configuration of a world on a determined sized grid, with houses, batteries and cables.
class Configuration():
    def __init__(width, height):

        # Creates a correctly sized grid of points
        self.configuration = []
        for j in range(height):
            row = []
            for i in range(width):
                point = Point()
                row.append(point)
            self.configuration.append(row)

    def add_battery(x, y, battery):
        self.configuration[x][y].content = battery

    def add_house(x, y, house):
        self.configuration[x][y].content = house

    def add_cable(x, y, orientation, battery):
        if orientation == "right":
            self.configuration[x][y].right.append(battery)

        if orientation == "down":
            self.configuration[x][y].down.append(battery)

    def delete_battery(x, y):
        if type(self.configuration[x][y].content) == 'Battery.Battery':
            self.configuration[x][y].content = None

    def delete_house(x, y, house):
        if type(self.configuration[x][y].content) == 'House.House':
            self.configuration[x][y].content = None

    def delete_cable(x, y, orientation, battery):
        if orientation == "right":
            if battery in self.configuration[x][y].right:
                self.configuration[x][y].right.remove(battery)

        if orientation == "down":
            if battery in self.configuration[x][y].down:
                self.configuration[x][y].down.remove(battery)

class Point():
    def __init__(x, y):
        # Shows the position of this point
        self.x = x
        self.y = y

        # Here comes the list of batteries that is connected to a cable to the right of this point
        self.right = []

        # Here comes the list of batteries that is connected to a cable below this point
        self.down = []

        # The content on this point. Could be a house or battery
        self.content = None

