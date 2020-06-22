'''
* battery class
*
* Programmeertheorie
* Optimum Prime
*
* The battery class saves all the information concering the batteries inside the configuration.
*
'''


from classes.house import House

class Battery():
    '''
    The battery class saves all the important information too the battery in the configuration
    and has a collection of functions that can alter that information. Initialisation requires
    a x_axis and y_axis location and the capacity of the battery.
    '''

    def __init__(self, x_axis, y_axis, capacity):

        # variables that save information of battery
        self.position_x = x_axis
        self.position_y = y_axis
        self.capacity = capacity
        self.energy_production = 0
        self.length_cables = 0
        self.list_cables = []
        self.costs_battery = 5000
        self.houses_in_battery = []


    def distance(self, house):
        '''
        Calculates the distance between the battery and a house using a streight line.
        
        Input: house instance.

        Returns: direct distance as an Int.
        '''

        return int(abs(self.position_x - house.position_x) + abs(self.position_y - house.position_y))


    def battery_full(self, new_house):
        '''
        Checks if by adding the house inputted house can be add too the battery without
        it going over capacity.

        Input: house instance.

        Returns: boolean, True if added house goes over battery capacity.
        '''

        return self.capacity < self.energy_production + new_house.production


    def battery_over_capacity(self):
        '''
        Recalculates the energy production stored in battery and checks if battery is 
        over capacity.

        Returns: boolean, True if battery is over capacity.
        '''
        
        self.cal_bat_production()
        return self.capacity < self.energy_production

    def cal_bat_production(self):
        '''
        Resets energy_production in battery to 0 and recalculates the energy production
        stored in battery based on houses in battery.
        '''
        
        self.energy_production = 0
        for self.a_house in self.houses_in_battery:
            self.energy_production += self.a_house.production
    

    # return true if house added and False if not
    def add_house(self, new_house):
        '''
        Adds house to houses_in_battery in battery and updates the energy productin stored
        in the battery.
        '''

        self.houses_in_battery.append(new_house)
        self.cal_bat_production()


    def remove_house(self, del_house):
        '''
        Removes house from houses_in_battery in battery if house is in battery and updates
        the energy productin stored in the battery.

        Returns: Boolean, True if house removed.
        '''

        if del_house in self.houses_in_battery:
            self.houses_in_battery.remove(del_house)
            self.cal_bat_production()
            return True
        return False


    def empty_battery(self):
        '''
        Resets battery to empty.
        '''        
        self.houses_in_battery = []
        self.energy_production = 0
        self.costs_battery = 5000
