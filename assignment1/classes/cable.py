
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


