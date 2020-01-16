

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
        """
        method to speed up an object
        """
        self.speed += value

    def execute(self):
        """
        main def
        """
        print("Speed:",self.speed)

    # Methods to compare objects
    def __gt__(self,other):
        """
        first method to compare objects
        """
        return self.speed > other.speed

    def __eq__(self,other):
        """
        first method to compare objects
        """
        return self.speed == other.speed

    def __del__(self):
        """
        destructor method
        """
        print("Object: " + self.description + " deleted")



if __name__ == "__main__":
    opel = Vehicle("Opel",11)
    volvo = Vehicle("Volvo",50)

    opel.execute()
    opel.speed_up(20)
    opel.execute()

    # Compare objects
    if opel > volvo:
        print("Opel is faster")
    elif opel == volvo:
        print("Both cars have the same speed!")
    else:
        print("Volvo is faster")

    del volvo
    del opel
