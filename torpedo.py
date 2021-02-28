# Useful Constants
TORPEDO_RADIUS = 4
class Torpedo:
    """Handles the methods and characteristics of a single Torpedo"""
    def __init__(self, velocity, location, heading, time):
        self.__location_x = location[0]  # Location in X direction
        self.__velocity_x = velocity[0]  # Velocity in X direction
        self.__location_y = location[1]  # Location in Y direction
        self.__velocity_y = velocity[1]  # Velocity in Y direction
        self.__heading = heading
        self.__time_life = time

    def get_velocity(self):
        """
        :return: tuple which represents the velocity of the torpedo in each
        direction
        """
        return self.__velocity_x, self.__velocity_y

    def get_radius(self):
        """
        :return: return the radius of the torpedo (CONSTANT)
        """
        return TORPEDO_RADIUS

    def get_location(self):
        """
        :return: tuple which represents the location on screen of the
        torpedo in each
        direction
        """
        return self.__location_x, self.__location_y

    def get_heading(self):
        """
        :return: integer which represents the heading(angle) of the torpedo
        """
        return self.__heading

    def get_time(self):
        """Get the lifespan of the torpedo according to each game_loop"""
        return self.__time_life

    def update_location(self, location):
        """Update the location coords of the torpedo"""
        self.__location_x = location[0]
        self.__location_y = location[1]

    def update_heading(self, heading):
        """Update the angle of the torpedo"""
        self.__heading = heading

    def update_velocity(self, velocity):
        """Update the velocity of the torpedo in each direction"""
        self.__velocity_x = velocity[0]
        self.__velocity_y = velocity[1]

    def update_time(self):
        """Update the life span of the torpedo since its launch"""
        self.__time_life += 1