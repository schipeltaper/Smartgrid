'''
Given a solution, this class can use the principle of hill-climbing to find a better solution
'''

from random import choice
from algorithms.cable_algorithm import Cable
from classes.cable import Cable_instance


class Hill_climber():
    def __init__(self, solved_configuration):
        self.config = solved_configuration

    def climb_the_hill(self):
        for i in range(3000):
            if self.possible_change():
                print(self.config.cal_costs())
        # return new_configuration #TODO

    # Swaps two houses or replaces one house at random
    def possible_change(self):
        coinflip = choice([0, 1, 2, 3])
        costs = self.config.cal_costs()

        print(f"The total costs of simulated annealing hill climber: {self.config.cal_costs()}")


        # 25% chance: choose random house, assign it to random other battery
        if coinflip == 0:
            chosen_battery = choice(self.config.all_batteries)
            print(chosen_battery)
            chosen_house = choice(chosen_battery.houses_in_battery)
            new_battery = choice(self.config.all_batteries)

            new_battery.houses_in_battery.append(chosen_house)
            chosen_battery.houses_in_battery.remove(chosen_house)

            self.astar_cable2 = Cable(self.config)
            self.astar_cable2.cable_list_batteries(self.config.all_batteries)

            # checks if new configuration is better and valid. Otherwize undo changes
            if costs < self.config.cal_costs() or self.config.houses_with_ovorcapacity():
                chosen_battery.houses_in_battery.append(chosen_house)
                new_battery.houses_in_battery.remove(chosen_house)

                self.astar_cable2 = Cable(self.config)
                self.astar_cable2.cable_list_batteries(self.config.all_batteries)
                return False

            return True

        # 75% chance: choose two random houses from different batteries and swap them
        elif coinflip > 0:
            chosen_battery1 = choice(self.config.all_batteries)
            print(chosen_battery1)
            chosen_house1 = choice(chosen_battery1.houses_in_battery)
            chosen_battery2 = choice(self.config.all_batteries)
            chosen_house2 = choice(chosen_battery2.houses_in_battery)

            # swap the two houses
            chosen_battery1.houses_in_battery.append(chosen_house2)
            chosen_battery1.houses_in_battery.remove(chosen_house1)
            chosen_battery2.houses_in_battery.append(chosen_house1)
            chosen_battery2.houses_in_battery.remove(chosen_house2)

            self.astar_cable2 = Cable(self.config)
            self.astar_cable2.cable_list_batteries(self.config.all_batteries)

        # checks if new configuration is better and valid. Otherwize undo changes
        if costs < self.config.cal_costs() or self.config.houses_with_ovorcapacity():
            chosen_battery1.houses_in_battery.append(chosen_house1)
            chosen_battery1.houses_in_battery.remove(chosen_house2)
            chosen_battery2.houses_in_battery.append(chosen_house2)
            chosen_battery2.houses_in_battery.remove(chosen_house1)

            self.astar_cable2 = Cable(self.config)
            self.astar_cable2.cable_list_batteries(self.config.all_batteries)

            return False

        return True