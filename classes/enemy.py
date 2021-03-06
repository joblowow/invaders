from classes.ship import Ship
from classes.laser import Laser
from utilities.constants import *


class Enemy(Ship):
    # Pass a color to the color map to get the corresponding img
    COLOR_MAP = {
        "red": (RED_SPACE_SHIP, RED_LASER),
        "blue": (BLUE_SPACE_SHIP, BLUE_LASER),
        "green": (GREEN_SPACE_SHIP, GREEN_LASER)
    }
    # Enemies also have a color attribute
    def __init__(self, x, y, color, health=100):
        # Use ship's initialization method
        super().__init__(x, y, health)
        self.color=color
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    # Move the ship downward when this is called
    def move(self, velocity):
        self.y += velocity

    def returnColor(self):
        return self.color

    def stop_lasers(self):

        for laser in self.lasers.copy():
            del laser

        self.lasers = []

    def shoot(self):
        # Only shoot laser if the cooldown counter is 0
        if self.cool_down_counter == 0:
            # Offset the laser x position a little so it comes from the center of the enemy ship
            laser = Laser(self.x+(abs(self.ship_img.get_width())/2) - (self.laser_img.get_width() / 2), self.y + self.ship_img.get_height() - (self.laser_img.get_height()/2), self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
