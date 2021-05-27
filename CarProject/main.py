from car import Car
from electric_car import ElectricCar

my_new_car = Car("audi", "A4", 2020)

print(my_new_car.get_long_name())

my_electric_car = ElectricCar("tesla", "model x", 2021)

print(my_electric_car.get_long_name())
print(my_electric_car.battery.describe_battery())