
'''
* Greedy class
*
*
* Programmeertheorie
* Optimum Prime
*
* Greedy class contains a collection of greedy algorthm distribute the houses amoung the batteries inside a
* configuration. This class is initialised with an configuration class instance. The class is used by calling
* a greedy function inside the class: proximity_sort or random_greedy. The algorithms will divide the houses
* amoungst the batteries in the configuration and update the filled batteries inside the configuration.
*
*
'''


from classes.House import House
from classes.map_lists import district_1, district_2, district_3
from algorithms.cable_algorithm import Cable

import copy
import random

class Greedy():
    '''
    The greedy class is a collection of house distributing algorithms and functions that support these.

    Initialisation requires a district configuration.
    '''

    def __init__(self, district_configuration):

        # varibles to save values used in class
        self.district = district_configuration
        self.batteries = self.district.all_batteries # potentially make NONE
        self.all_houses = self.district.all_houses
        self.connected_houses = []


    def random_greedy(self, rounds):
        from algorithms.simulated_annealing import simulated_annealing

        '''
        Random greedy algorithms includes an aspect of randomness into a greedy
        model. A greedy algorithm will always choose the best option for a problem
        without considering the effects further down the line.

        Input: the amount of times the houses will be moved between batteries.

        Distributes the houses randomly under the batteries and than reshuffles the
        houses by randomly choosing one of the batteries and deciding to change battery
        if that battery is at closer proximity than the current battery.
        '''

        # distributing houses randomly amoung batteries
        self.functions_in_sa_class = simulated_annealing(self.district)
        self.functions_in_sa_class.distributing_houses_amoung_batteries()


        # attempts to move a house rounds amount of times into a random battery, choice proximity based
        self.to_cal_distance = Cable(self.district)
        self.rounds_done = 0
        while self.rounds_done < rounds:
            for self.a_house in self.district.all_houses:
                self.ran_chosen_bat = random.choice(self.district.all_batteries)
                if self.to_cal_distance.calculate_distance(self.a_house, self.a_house.battery) > \
                self.to_cal_distance.calculate_distance(self.a_house, self.ran_chosen_bat):
                    self.a_house.battery.houses_in_battery.remove(self.a_house)
                    self.a_house.battery = self.ran_chosen_bat
                    self.ran_chosen_bat.houses_in_battery.append(self.a_house)
            self.rounds_done += 1


    def proximity_sort(self):

        '''
        A greedy algorithm will always choose the best option for a problem
        without considering the effects further down the line. This greedy algorithm
        uses the distance between a houses and the potential batteries as the heuristic
        choose the battery to be put in.

        The houses are saved inside the battery instances, inside the houses_in_battery
        and these filled batteries update the batteries stored inside the all_batteries
        list in the configuration class.
        '''

        # sorts houses from high too low production
        self.all_houses = self.sort_house(self.all_houses)

        # orders the batteries from closses to furthest for every house
        for self.the_house in self.all_houses:
            for self.battery_numb in range(len(self.batteries)):
                for self.battery_numb2 in range(self.battery_numb, len(self.batteries)):
                    if self.batteries[self.battery_numb2].distance(self.the_house) < \
                    self.batteries[self.battery_numb].distance(self.the_house):
                        self.temp_save = self.batteries[self.battery_numb]
                        self.batteries[self.battery_numb] = self.batteries[self.battery_numb2]
                        self.batteries[self.battery_numb2] = self.temp_save

            # add house to closest none full house
            for self.the_battery in self.batteries:
                if self.the_battery.battery_full(self.the_house) is not True:
                    self.the_battery.add_house(self.the_house)
                    break
                else:
                    # warns user if not all houses allocated
                    if self.the_battery == self.batteries[len(self.batteries)-1]:
                        print("Not all houses added to batteries because all batteries full!")
                        return 1

        # updates the batteries in the configuration
        self.district.all_batteries = self.batteries


    def sort_house(self, houses):
        '''
        Sorts a list of houses from high to low based on energy production.

        Input: list of houses

        Return: sorted list of houses
        '''
        # Selection sort, high too low based on energy production
        for self.house_numb in range(len(houses)):
            biggest_location = self.house_numb
            for self.house_numb2 in range(self.house_numb, len(houses)):
                if houses[self.house_numb2].production > houses[biggest_location].production:
                    biggest_location = self.house_numb2
            self.temp = houses[self.house_numb]
            houses[self.house_numb] = houses[biggest_location]
            houses[biggest_location] = self.temp

        # sorted list of houses
        return houses


    def house_low_sort(self, houses):
        '''
        Sorts a list of houses from low to high based on energy production.

        Input: list of houses

        Return: sorted list of houses
        '''

        # Selection Sort, low too high based on energy production
        for self.house_numb in range(len(houses)):
            for self.house_numb2 in range(self.house_numb, len(houses)):
                if houses[self.house_numb2].production < houses[self.house_numb].production:
                    self.temp = houses[self.house_numb]
                    houses[self.house_numb] = houses[self.house_numb2]
                    houses[self.house_numb2] = self.temp

        # sorted list of houses
        return houses


    ''' Delete !!!!!!!!! '''
    # function to add houses to batteries
    def adding_houses(self):

        # sorting houses
        self.sort_house(self.all_houses)

        # battery currently storing houses in
        self.battery_numb = 0

        # looping through houses
        for self.house in self.all_houses:

            # make sure house is not already in battery
            if not self.house in self.connected_houses:

                # loop through batteries for every house
                self.battery_numb += 1

                if self.battery_numb >= len(self.batteries):
                    self.battery_numb = 0

                # check if battery is full and add house to battery
                if self.batteries[self.battery_numb].battery_full(self.house):

                    # move to next battery
                    self.battery_numb += 1

                # add house in next battery
                self.batteries[self.battery_numb].add_house(self.house)

                # add house to already sorted house
                self.connected_houses.append(self.house)

    ''' Delete !!!!!!!!! '''
    # choosing if house should move to different battery
    def proximity_move(self, house):

        # move if option better than current situation
        self.choosen_battery = random.choice(self.district.all_batteries)

        if self.choosen_battery.distance(house) < house.battery.distance(house):

            # removing house from former battery
            house.battery.remove_house(house)

            # adding house to battery & battery to house
            self.choosen_battery.add_house(house)

            house.battery = self.choosen_battery
