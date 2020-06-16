
class Cable_instance():
    def __init__(self, x, y):
        # Shows the position of this point
        self.position_x = x
        self.position_y = y

        # stores information about where the cable came from and is going
        self.next_cable_inst = None
        self.former_cable_inst = None
    
    # returns 'inbetween coordinates' (location of cable to be layed) of cable from imput cable object
    def determine_direction_cable(self):

        # determine relative next point
        if self.next_cable_inst is None:
            # no next point
            return "EMPTY"
        
        # does cable move up
        elif self.position_y > self.next_cable_inst.position_y:
            return "UP"

        # does cable move down
        elif self.position_y < self.next_cable_inst.position_y:
            return "DOWN"

        elif self.position_x > self.next_cable_inst.position_x:
            return "LEFT"
        
        elif self.position_x < self.next_cable_inst.position_x:
            return "RIGHT" 

class Cable_line():
    def __init__(self, start):

        # saves the start of the cable
        self.start = start
        
        # saves the end of the cable
        self.end = None

        # saves cable costs
        self.costs = 0

        # saves the coordinates of the full cable
        self.cable_coordinates = []
        
        # directly saves the start of the cable when fist coordinates are entered
        self.add_cable_instance(start)

    def cal_cable_costs(self):
        self.costs = len(self.cable_coordinates) * 9
        return self.costs

    def add_cable_instance(self, cable_instance):
        
        # adds cable instance to cable line
        self.cable_coordinates.append(cable_instance)

        # add the costs of a cable
        self.costs += 9
        
        # add cable instance as ending of the cable
        self.end = cable_instance

    def print_cable_line_coordinates(self):
        for cables in self.cable_coordinates:
            print(f"x: {cables.position_x}, y: {cables.position_y}")


