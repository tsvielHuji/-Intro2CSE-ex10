import math


class Asteroid:
    """Handles the methods and characteristics of a single asteroid"""
    def __init__(self, location, velocity, size_asteroid):
        self.__x_ast_coo = location[0]
        self.__y_ast_coo = location[1]
        self.__x_ast_speed = velocity[0]
        self.__y_ast_speed = velocity[1]
        self.__size_asteroid = size_asteroid

    def get_velocity(self):
        """
        :return: A tuple representing the current velocity of an asteroid
        """
        return self.__x_ast_speed, self.__y_ast_speed

    def get_location(self):
        """
        :return: A tuple representing the current location of an asteroid
        """
        return self.__x_ast_coo, self.__y_ast_coo

    def get_size(self):
        """
        :return: the size of the asteroid
        """
        return self.__size_asteroid

    def get_radius(self):
        """
        :return: the current radius of an asteroid
        """
        return self.__size_asteroid * 10 - 5

    def minimize_asteroids(self, size_asteroid):
        """
        The function reduce the radius of the asteroid
        :return: True upon success, False upon fail
        """
        if size_asteroid > 0:
            self.__size_asteroid -= 1
            return True
        return False
        
    def has_intersection(self, obj):
        """
        The function checks for intersection of given object with asteroid
        :return: True for intersection, False if not
        """
        location = obj.get_location()
        radius = obj.get_radius()
        distance = math.sqrt(
            (location[0] - self.get_location()[0]) ** 2 +
            (location[1] - self.get_location()[1]) ** 2)
        if distance <= (self.get_radius() + radius):
            return True
        return False

    def update_location(self, location):
        """
        The function updates the current location of an asteroid
        :param location: A tuple representing the new location of an asteroid
        """
        self.__x_ast_coo = location[0]
        self.__y_ast_coo = location[1]


