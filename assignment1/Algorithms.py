from House import *

# Maybe TODO: use more efficient sorting algorithm
def sortHouse(houses):
    # Selection Sort
    for i in range(len(houses)):
        grootste_locatie = i

        # We zoeken naar de grootste capaciteit
        for j in range(i, len(houses)):
            if houses[j].capaciteit > houses[grootste_locatie].capaciteit:
                grootste_locatie = j

        temp = houses[i]
        houses[i] = houses[grootste_locatie]
        houses[grootste_locatie] = temp

    return houses
    
# calculate costs for list of batteries
def totalCosts(batteries):
    total_costs = 0
    for all battery in batteries:
        total_costs += battery.costs
    return total_costs