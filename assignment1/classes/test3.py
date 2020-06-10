# Example of how to create a configuration object with the info of district_1

from Battery import Battery
from House import House
from Configuration import *
from map_lists import district_1, district_2, district_3

con = Configuration(51, 51)

con.create_district(district_1)

print(con.configuration)