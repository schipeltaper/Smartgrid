from House import *
import Battery.py

# Maybe TODO: use more efficient sorting algorithm
def sortHouse(houses):
    # Selection Sort
    for house_numb in range(len(houses)):
        biggest_location = house_numb

        # We're searching for the highest capacity
        for house_numb2 in range(house_numb, len(houses)):
            if houses[house_numb2].capacity > houses[biggest_location].capacity:
                biggest_location = house_numb2

        temp = houses[house_numb]
        houses[house_numb] = houses[biggest_location]
        houses[biggest_location] = temp

    return houses
    
# calculate costs for list of batteries
def totalCosts(batteries):
    total_costs = 0
    for all battery in batteries:
        total_costs += battery.costs
    return total_costs

def adding_houses():
    
    battery_numb = 0
    
    for house in district_1["houses"]:
        
       # add house to battery
        if Battery.add_house(house):
            
            # go to next house
            continue
        else:
           
            # go to next battery
            battery_numb += 1

        if battery_numb >= len(district_1[batteries]):
            # all batteries full!
            return 1