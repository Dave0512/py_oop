

# Definition of the class Vehicle
class Vehicle:
    """docstring for Vehicle."""
    speed=0 #Attribute
    # Methods
    def speed_up(self,value):
        self.speed += value

    def execute(self):
        print("Speed:",self.speed)


if __name__ == "__main__":

    opel = Vehicle()
    opel.execute()
