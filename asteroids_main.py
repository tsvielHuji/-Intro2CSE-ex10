from screen import Screen
import sys
import math
from ship import Ship
import random
from asteroid import Asteroid
from torpedo import Torpedo

SCREEN_BORDER_X = range(-500, 501)
SCREEN_BORDER_Y = range(-500, 501)
DEFAULT_ASTEROIDS_NUM = 5
SHIP_RADIUS = 1
SHIP_LIFE = 3
TURN_LEFT = "l"
TURN_RIGHT = "r"
VALID_MOVE_KEY = {TURN_RIGHT, TURN_LEFT}
INITIAL_AS_SIZE = 3
MIN_SPEED_AS = 1
MAX_SPEED_AS = 4
SPEED_RANGE = [-4, -3, -2, -1, 1, 2, 3, 4]
TORPEDO_LIMIT = 10
TORPEDO_EXPIRY_TIME = 200

# Messages
GAME_OVER_TITLE = "GAME OVER"
LOSER = "You ran out of life, you lose"
WINNER = "CONGRATULATION YOU WIN"
HIT_TITLE = "MAYDAY MAYDAY, I AM GOING DOWN"
HIT_MESSAGE = "YOU LOSE 1 LIFE POINT"
QUITTER = "Thank you for playing"


class GameRunner:
    """The main class of the game. Handles most of the game"""
    def __init__(self, asteroids_amount):
        # Calls the screen and sets its borders
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y

        # Randomizes coordinates for the ship in each of the axis
        random_x = random.randint(self.__screen_min_x, self.__screen_max_x)
        random_y = random.randint(self.__screen_min_y, self.__screen_max_y)
        self.__ship = Ship((random_x, random_y), (0, 0), 0)  # Our ship
        self.__asteroid_list = []  # The list of asteroids the are in the game
        # Handles the initialization of the asteroids when the game starts
        for current_asteroid_i in range(asteroids_amount):
            location = random.randint(self.__screen_min_x,
                                      self.__screen_max_x), random.randint(
                self.__screen_min_x, self.__screen_max_x)
            velocity = random.choice(SPEED_RANGE), random.choice(SPEED_RANGE)
            asteroid = Asteroid(location, velocity, INITIAL_AS_SIZE)
            while asteroid.has_intersection(self.__ship):
                asteroid = Asteroid(location, velocity, INITIAL_AS_SIZE)
            self.__asteroid_list.append(asteroid)
        for asteroid in self.__asteroid_list:
            self.__screen.register_asteroid(asteroid, INITIAL_AS_SIZE)
        self.__torpedo_list = []  # The list which stores shouted torpedoes
        self.__points = 0  # stores the points of the player
        self.__screen.set_score(self.__points)  # Register the intialized
        # points to the screen

    def run(self):
        """The run function of the game - DO NOT TOUCH"""
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        """handles the outer loop of the game - DO NOT TOUCH"""
        # You don't need to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def __move_object(self, old_spot, speed):
        """
        :param old_spot: tuple of the old coords for each axis
        :param speed: tuple of the old velocity for each axis
        :return: the new coords of the object
        """
        delta_x = self.__screen_max_x - self.__screen_min_x  # the Delta of x
        # Change the spot of the object on the X axis
        new_spot_x = self.__screen_min_x + ((old_spot[0] + speed[0] -
                                             self.__screen_min_x) % delta_x)
        delta_y = self.__screen_max_y - self.__screen_min_y
        # Change the spot of the object on the Y axis
        new_spot_y = self.__screen_min_y + ((old_spot[1] + speed[1] -
                                             self.__screen_min_y) % delta_y)
        return new_spot_x, new_spot_y  # Update the location of ship

    def _game_loop(self):
        """Loop that runs every second of the game"""
        self.__add_ship(self.__ship)  # adds a ship and move it on screen
        for asteroid in self.__asteroid_list:
            self.__screen.draw_asteroid(asteroid,
                                        asteroid.get_location()[0],
                                        asteroid.get_location()[1])
            asteroid.update_location(
                self.__move_object(asteroid.get_location(),
                                   asteroid.get_velocity()))
            self.__ship_intersection()  # Check if there is intersections
        # if space is pressed, a new torpedo is created
        if self.__screen.is_space_pressed():  # When space is pressed
            self.__add_torpedo()  # Add torpedo to the game
        self.__move_torpedo()  # Move the torpedo from its shootout
        if self.__screen.should_end():
            self.__screen.show_message(QUITTER, QUITTER)
            self.__screen.end_game()
            sys.exit()
        if len(self.__asteroid_list) == 0:  # If all asteroids are destroyed
            self.__screen.show_message(WINNER, WINNER)  # Send win msg
            self.__screen.end_game()  # End the game
            sys.exit()  # Exit the program

    def __add_torpedo(self):
        """The function handles the creation of torpedo throughout the game"""
        if len(self.__torpedo_list) < TORPEDO_LIMIT:
            # Creates every time a new torpedo object
            torpedo = Torpedo((self.__ship.get_velocity()[0],
                               self.__ship.get_velocity()[1]),
                              (self.__ship.get_location()[0],
                               self.__ship.get_location()[1]),
                              self.__ship.get_heading(), 0)
            # there can be only 10 torpedoes on screen at the same time
            self.__shoot_torpedo(torpedo)  # Process the shootout of the
            # torpedo
            self.__torpedo_list.append(torpedo)  # To make sure there
            # Handles the movement of the torpedo from its moment of launch

    def __shoot_torpedo(self, torpedo):
        """
        The function handles the process of shooting a torpedo including
        drawing it on board, register it in screen class and provide its
        velocity.
        :param torpedo: an object of Torpedo type we want to get its velocity
        """
        velocity_x = torpedo.get_velocity()[0] + 2 * math.cos(math.radians(
            torpedo.get_heading()))  # The new velocity in the x direction
        velocity_y = torpedo.get_velocity()[1] + 2 * math.sin(math.radians(
            torpedo.get_heading()))  # The new velocity in the y direction
        # The following update the new velocity of the torpedo
        torpedo.update_velocity((velocity_x, velocity_y))
        self.__screen.register_torpedo(torpedo)  # Register on screen
        self.__screen.draw_torpedo(torpedo, torpedo.get_location()[0],
                                   torpedo.get_location()[1],
                                   torpedo.get_heading())  # Draw it

    def __remove_torpedo(self, torpedo):
        """The function removes the torpedo after the expiry time"""
        if torpedo.get_time() >= TORPEDO_EXPIRY_TIME:
            self.__screen.unregister_torpedo(torpedo)
            self.__torpedo_list.remove(torpedo)

    def __move_torpedo(self):
        """Handles the entire life session of a Torpedo from the moment of
        its launch to its expiry time"""
        for single_torpedo in self.__torpedo_list:
            single_torpedo.update_location(self.__move_object(
                single_torpedo.get_location(),
                single_torpedo.get_velocity()))  # Updates the torpedo location
            self.__screen.draw_torpedo(single_torpedo,
                                       single_torpedo.get_location()[0],
                                       single_torpedo.get_location()[1],
                                       single_torpedo.get_heading())
            self.__torpedo_hit(single_torpedo)  # Handles the case for hit
            single_torpedo.update_time() # Update the life time of the torpedo
            self.__remove_torpedo(single_torpedo)  # Remove torpedo

    def __add_ship(self, ship):
        """
        draws a new ship into the game, and handles it three
        processes of acceleration, movement and turning
        :param ship: object of ship type
        """
        self.__screen.draw_ship(ship.get_location()[0],
                                ship.get_location()[1],
                                ship.get_heading())  # Draw a new ship
        if self.__screen.is_left_pressed():  # If left is presesd
            self.__turn_ship(TURN_LEFT)  # Turn the ship left
        if self.__screen.is_right_pressed():  # If right is pressed
            self.__turn_ship(TURN_RIGHT)  # Turn the ship right
        if self.__screen.is_up_pressed():  # If up is pressed
            self.__accelerate_ship() # Accelerate the ship
        # Update its new location according to the new coords
        self.__ship.update_location(
            self.__move_object(self.__ship.get_location(),
                               self.__ship.get_velocity()))

    def __turn_ship(self, movekey):
        """ Turns the head of the ship
        :param movekey: the key that represents the direction of the turn
        :return: True upon success and False upon failing
        """
        if movekey not in VALID_MOVE_KEY:  # Fallback for invalid key
            return False
        if movekey is TURN_RIGHT:  # Case for turn right
            new_head = self.__ship.get_heading() - 7
            self.__ship.update_heading(new_head)
        if movekey is TURN_LEFT:  # Case for turn left
            new_head = self.__ship.get_heading() + 7
            self.__ship.update_heading(new_head)
        return True

    def __accelerate_ship(self):
        """ The function handles the acceleration of the ship"""
        velocity_x = self.__ship.get_velocity()[0] + math.cos(math.radians(
            self.__ship.get_heading()))
        velocity_y = self.__ship.get_velocity()[1] + math.sin(math.radians(
            self.__ship.get_heading()))
        self.__ship.update_velocity((velocity_x, velocity_y))

    def __torpedo_hit(self, torpedo):
        """The function handles the intersection of the ship with an object"""
        for asteroid in range(len(self.__asteroid_list)):
            if self.__asteroid_list[asteroid].has_intersection(
                    torpedo):
                self.__split_asteroid(self.__asteroid_list[asteroid])
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedo_list.remove(torpedo)
                break

    def __ship_intersection(self):
        """The function handles the intersection of the ship with an object"""
        for asteroid in range(len(self.__asteroid_list)):
            if self.__asteroid_list[asteroid].has_intersection(self.__ship):
                if self.__ship.reduce_life() is False:
                    self.__screen.show_message(GAME_OVER_TITLE, LOSER)
                    self.__screen.end_game()  # End the game
                    sys.exit()
                self.__ship.reduce_life()
                self.__screen.remove_life()
                self.__screen.show_message(HIT_TITLE, HIT_MESSAGE)
                self.__screen.unregister_asteroid(
                    self.__asteroid_list[asteroid])
                self.__asteroid_list.remove(self.__asteroid_list[asteroid])
                break

    def __split_asteroid(self, asteroid):
        """The function handles the split of an asteroid upon hit"""
        location = asteroid.get_location()  # T
        velocity = asteroid.get_velocity()
        new_size = asteroid.get_size() - 1
        if asteroid.get_size() > 1:  # As long as the size is greater than 1
            if asteroid.get_size() == 3:  # Case for asteroid of size 3 (MAX)
                self.__points += 20  # adds 20 points
                self.__screen.set_score(self.__points)  # points to screen
            elif asteroid.get_size() == 2:  # Case for asteroid of size 2
                self.__points += 50  # adds 50 points
                self.__screen.set_score(self.__points)  # points to screen
            # Here we begin the process of splitting the asteroid
            self.__screen.unregister_asteroid(
                asteroid)
            self.__asteroid_list.remove(asteroid)
            new_asteroid1 = Asteroid(location, velocity, new_size)
            negative_velocity_tup = ((-1)*velocity[0], (-1)*velocity[1])
            new_asteroid2 = Asteroid(location, negative_velocity_tup, new_size)
            self.__asteroid_list.append(new_asteroid1)
            self.__asteroid_list.append(new_asteroid2)
            self.__screen.register_asteroid(new_asteroid1,
                                            new_asteroid1.get_size())
            self.__screen.register_asteroid(new_asteroid2,
                                            new_asteroid1.get_size())
        elif asteroid.get_size() == 1:  # Case for asteroid of size 1
            self.__points += 100  # adds 100 points
            self.__screen.set_score(self.__points)  # Update the screen
            # Remove the asteroid as the Radius of the Asteroid is less than 1
            self.__screen.unregister_asteroid(
                asteroid)
            self.__asteroid_list.remove(asteroid)


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
