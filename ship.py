# Relevant Constants
SHIP_RADIUS = 1
SHIP_LIFE = 3
TURN_LEFT = "l"
TURN_RIGHT = "R"
VALID_MOVE_KEY = {TURN_RIGHT, TURN_LEFT}


class Ship:
    """Handles the methods and characteristics of a single Ship"""
    def __init__(self, location, velocity, heading):
        self.__location_x = location[0]   # Location in X direction
        self.__velocity_x = velocity[0]   # Velocity in X direction
        self.__location_y = location[1]   # Location in Y direction
        self.__velocity_y = velocity[1]   # Velocity in Y direction
        self.__heading = heading    # The angle of the head of the ship
        self.__life = SHIP_LIFE

    def get_velocity(self):
        """
        :return: return the current velocity of the ship
        """
        return self.__velocity_x, self.__velocity_y

    def get_location(self):
        """
        :return: return the current location of the ship
        """
        return self.__location_x, self.__location_y

    def get_heading(self):
        """
        :return: return the angle of the head of the ship in Radians
        """
        return float(self.__heading)

    def get_radius(self):
        """
        :return: The radius of the ship based on the declared constant
        """
        return SHIP_RADIUS

    def reduce_life(self):
        """
        The function reduce the life of the ship
        :return: True upon success and False upon failing
        """
        if self.__life <= 0:
            return False
        self.__life -= 1
        return True

    def update_location(self, location):
        """Updates the location of the ship"""
        self.__location_x = location[0]
        self.__location_y = location[1]

    def update_heading(self, heading):
        """Updates the heading of the ship"""
        self.__heading = heading

    def update_velocity(self, velocity):
        """Updates the velocity of the ship"""
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]


