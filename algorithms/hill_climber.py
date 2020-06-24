'''
* Hill_climber class
*
*
* Programmeertheorie
* Optimum Prime
*
* This Hill_climber class is made for solutions where we are not aloud to share cables. The class is made for using
* the principle of hill descending to find a better solution.
*
*
'''

from random import choice
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance


class Hill_climber():
    '''
    We initialize the object with a configuration object which is a correct solution. Then we can call a function
    which takes a number of steps to find a local minimum. Each step consists of either swapping two houses or giving
    a house a different battery. If the step results in an invalid solution or a higher cost, then the step is made
    undone and we move on to the next step.
    '''
    def __init__(self, solved_configuration):
        self.config = solved_configuration

    def climb_the_hill(self, step_amount):
        '''
        * this function takes step_amount number of steps, using the possible change function.
        * If the solution has improved or stayed the same in costs, we print the new cost.
        * The function finally returns the new configuration.
        '''

        for index in range(step_amount):
            if self.possible_change():
                print(self.config.cal_costs())
        return self.config

    def possible_change(self):
        '''
        This function Swaps two houses or replaces one house at random, with a 75% chance to
        swap and a 25% chance to replace a house. If the step results in a worse or invalid
        solution, the step is undone.
        '''

        # Decides which step will be taken
        coinflip = choice([0, 1, 2, 3])

        # calculates and print costs of current solution
        costs = self.config.cal_costs()
        print(f"The total costs: {costs}")

        # 25% chance: choose random house, assign it to random other battery
        if coinflip == 0:
            # takes a random house and assigns it to a new battery
            chosen_battery = choice(self.config.all_batteries)
            chosen_house = choice(chosen_battery.houses_in_battery)
            new_battery = choice(self.config.all_batteries)
            new_battery.houses_in_battery.append(chosen_house)
            chosen_battery.houses_in_battery.remove(chosen_house)

            # lays down the cables with the new configuration
            self.config.all_cables = []
            self.astar_cable2 = Cable(self.config)
            self.astar_cable2.cable_list_batteries(self.config.all_batteries, False)

            # checks if new configuration is better and valid. Otherwize undo changes
            if costs < self.config.cal_costs() or self.config.houses_with_ovorcapacity():
                chosen_battery.houses_in_battery.append(chosen_house)
                new_battery.houses_in_battery.remove(chosen_house)

                # lays down the cables with the current/original configuration
                self.config.all_cables = []
                self.astar_cable2 = Cable(self.config)
                self.astar_cable2.cable_list_batteries(self.config.all_batteries, False)

                return False

            return True

        # 75% chance: choose two random houses from different batteries and swap them
        elif coinflip > 0:
            # chooses two random houses and then swaps them
            chosen_battery1 = choice(self.config.all_batteries)
            chosen_house1 = choice(chosen_battery1.houses_in_battery)
            chosen_battery2 = choice(self.config.all_batteries)
            chosen_house2 = choice(chosen_battery2.houses_in_battery)
            chosen_battery1.houses_in_battery.append(chosen_house2)
            chosen_battery1.houses_in_battery.remove(chosen_house1)
            chosen_battery2.houses_in_battery.append(chosen_house1)
            chosen_battery2.houses_in_battery.remove(chosen_house2)

            # lays down the cables with the new configuration
            self.config.all_cables = []
            self.astar_cable2 = Cable(self.config)
            self.astar_cable2.cable_list_batteries(self.config.all_batteries, False)

            # checks if new configuration is better and valid. Otherwize undo changes
            if costs < self.config.cal_costs() or self.config.houses_with_ovorcapacity():
                chosen_battery1.houses_in_battery.append(chosen_house1)
                chosen_battery1.houses_in_battery.remove(chosen_house2)
                chosen_battery2.houses_in_battery.append(chosen_house2)
                chosen_battery2.houses_in_battery.remove(chosen_house1)

                # lays down the cables with the current/original configuration
                self.config.all_cables = []
                self.astar_cable2 = Cable(self.config)
                self.astar_cable2.cable_list_batteries(self.config.all_batteries, False)

                return False

        return True
