from car import Car

class Battery:

    def __init__(self, battery_size=75) -> None:
        self.battery_size = battery_size
    
    def describe_battery(self):
        return f"This car has a {self.battery_size}-kWh battery"
    
    def get_range(self):
        if self.battery_size == 75:
            range = 200
        elif self.battery_size == 100:
            range = 315
    
        return f"This car can go about {range} miles on a full charge."
    

class ElectricCar(Car):

    def __init__(self, make, model, year) -> None:
        super().__init__(make, model, year)
        self.battery = Battery()
