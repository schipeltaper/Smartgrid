from House import *
from Algorithms import *

def main():
    house1 = House(1, 2, 3)
    house2 = House(1, 3, 2)
    house3 = House(1, 6, 9)
    house4 = House(1, 4, 0)
    houses = [house1, house2, house3, house4]
    print(house1.capacity)
    print(house2.capacity)
    print(house3.capacity)
    print(house4.capacity)

    print(sortHouse(houses)[0].capacity)
    print(sortHouse(houses)[1].capacity)
    print(sortHouse(houses)[2].capacity)
    print(sortHouse(houses)[3].capacity)

    adding_houses()

if __name__ == "__main__":
    main()
