from House import *
from configuration import *

class Greedy():

    # sorting houses
    def sortHouse(self, houses):
        
        # Selection Sort
        for house_numb in range(len(houses)):
            biggest_location = house_numb

            # We're searching for the highest production
            for house_numb2 in range(house_numb, len(houses)):
                if houses[house_numb2].production > houses[biggest_location].production:
                    biggest_location = house_numb2

            temp = houses[house_numb]
            houses[house_numb] = houses[biggest_location]
            houses[biggest_location] = temp

        return houses


    # function to make a configuration of batteries with connected houses
    def adding_houses(self):

        houses = self.sortHouse(district_1["houses"])
        batteries = district_1["batteries"]

        for battery in batteries:
            for house in houses:
                # add house to battery
                if battery.add_house(house):
                    houses.remove(house)
                    # go to next house
                    continue