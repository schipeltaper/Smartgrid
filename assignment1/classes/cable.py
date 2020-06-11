class Cable_instance():
    def __init__(self, x, y):
        # Shows the position of this point
        self.position_x = x
        self.position_y = y

        # stores information about where the cable came from and is going
        self.next_cable_inst = None
        self.former_cable_inst = None