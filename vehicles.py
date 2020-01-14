

# Definition of the class Vehicle
class Vehicle:
    """docstring for Vehicle."""

    # constructor
    def __init__(self, desc, spe):
        """
        Contructor function
        """
        self.description = desc
        self.speed = spe

    # Methods
    def speed_up(self,value):
        self.speed += value

    def execute(self):
        print("Speed:",self.speed)


if __name__ == "__main__":
    opel = Vehicle("Opel",60)
    opel.execute()
    opel.speed_up(20)
    opel.execute()
