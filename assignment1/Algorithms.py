from House import *
from configuration import *

# Maybe TODO: use more efficient sorting algorithm
def sortHouse(houses):
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

# calculate costs for list of batteries
def totalCosts(batteries):
    total_costs = 0
    for battery in batteries:
        total_costs += battery.costs
    return total_costs

# function to make a configuration of batteries with connected houses
def adding_houses():
    houses = sortHouse(district_1["houses"])
    batteries = district_1["batteries"]

    for battery in batteries:
        for house in houses:
            # add house to battery
            if battery.add_house(house):
                houses.remove(house)
                # go to next house
                continue

