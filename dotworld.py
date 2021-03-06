"""The module that handles the front-end representations of the backend"""

import occupant
import plant
from occupant import ConvenientOccupant
from spawner import *


class World:

    def __init__(self):
        self.occupants = []
        self.plants = []
        self.spawners = []
        self.wheight = 0
        self.wwidth = 0
        self.__largest_radius = 0

    def add(self, occupant, x, y):
        c = Dot(occupant, x, y)
        self.test_largest_radius(c.get_radius())
        self.occupants.append(c)
        if isinstance(occupant, plant.Plant):
            self.plants.append(c)
        return c

    def add_occupant(self, x, y, gencode, behaviors, energy):
        return self.add(Occupant(gencode, behaviors, energy), x, y)

    def add_convenient(self, x, y, gencode, behaviors, energy):
        return self.add(ConvenientOccupant(gencode, behaviors, energy), x, y)

    def add_reproducing(self, x, y, gencode, behaviors, energy, parent):
        return self.add(ReproducingOccupant(gencode, behaviors, energy, parent), x, y)

    def add_creature(self, x, y, gencode, behaviors, energy, parent):
        return self.add(Creature(gencode, behaviors, energy, parent), x, y)

    def add_plant(self, x, y, energy):
        return self.add(Plant(energy), x, y)

    def add_spawner(self, spawner):
        self.spawners.append(spawner)
        return spawner

    def add_plant_spawner(self, timer, height, width, x, y):
        return self.add_spawner(PlantSpawner(timer, height, width, x, y))

    def test_largest_radius(self, r):
        if r > self.__largest_radius:
            self.set_largest_radius(r)

    def set_largest_radius(self, r):
        self.__largest_radius = r

    @staticmethod
    def fight(dot1, dot2):
        dot1power = random.normalvariate(dot1.get_occupant().get_power(), dot1.get_occupant().get_power() * .1)
        dot2power = random.normalvariate(dot2.get_occupant().get_power(), dot2.get_occupant().get_power() * .1)
        if dot1power > dot2power:
            dot1.get_occupant().subtract_energy(dot2power)
            dot1.get_occupant().add_energy(dot2.get_occupant().extract_energy() / 3)
            dot2.kill_trigger()
        elif dot1power < dot2power:
            dot2.get_occupant().subtract_energy(dot1power)
            dot2.get_occupant().add_energy(dot1.get_occupant().extract_energy() / 3)
            dot1.kill_trigger()
        else:
            dot1.kill_trigger()
            dot2.kill_trigger()

    def handle_wall_collision(self):
        for dot in self.occupants:
            r = dot.get_radius()
            if dot.getx() < 0:
                dot.setx(0)
                dot.get_occupant().hit_side()
            elif dot.getx2() > self.wwidth:
                dot.setx2(self.wwidth)
                dot.get_occupant().hit_side()
            if dot.gety() < 0:
                dot.sety(0)
                dot.get_occupant().hit_lid()
            elif dot.gety2() > self.wheight:
                dot.sety2(self.wheight)
                dot.get_occupant().hit_lid()

    def handle_collisions(self, dot, dots):
        for c in dots:
            distance = int((math.sqrt((((dot.get_centerx() - c.get_centerx()) * (dot.get_centerx() - c.get_centerx()))
                             + ((dot.get_centery() - c.get_centery()) * (dot.get_centery() - c.get_centery()))))))
            if distance <= (dot.get_radius() + c.get_radius()):
                if c != dot and occupant.similarity(dot.get_occupant(), c.get_occupant()) > 0:
                    self.fight(c, dot)

    @staticmethod
    def update_visions(dot, dots):
        nearby = []
        for c in dots:
            if c is not dot:
                if (dot.get_radius() / c.get_radius()) <= 10:
                    dx = dot.get_centerx() - c.get_centerx()
                    dy = dot.get_centery() - c.get_centery()
                    distance = int(math.sqrt(((dx*dx) + (dy*dy))))
                    if distance <= (dot.get_vision_radius() + c.get_vision_radius()) and distance != 0:
                       if dot.get_radius()/c.get_radius() <= 5:
                            nearby.append((c.get_occupant(), dx, dy, distance))
        dot.get_occupant().set_nearby(nearby)


class Dot:
    HIGHLIGHT_OFFSET = "#22AAFF"

    def __init__(self, occupant, x, y):
        self.__occupant = 0
        self.__x = 0
        self.__y = 0
        self.__x2 = 0
        self.__y2 = 0
        self.__radius = 0
        self.__reference = None
        self.__collide_trigger = False
        self.__kill_trigger = False
        self.__highlight_trigger = False
        self.__color_trigger = False
        self.__reproducing_trigger = False
        self.special = -1
        self.__occupant = occupant
        self.set_radius(occupant.get_size())
        self.setx(x-self.__radius)
        self.sety(y-self.__radius)
        self.__color = occupant.get_color()

    def to_string(self):
        result = "(" + str(self.get_centerx()) + ", " + str(self.get_centery()) + ")\n"
        result += str(self.get_occupant().to_string())
        return result

    def setx(self, x):
        self.__x = x
        self.__x2 = x + (2 * self.__radius)

    def getx(self):
        return self.__x

    def sety(self, y):
        self.__y = y
        self.__y2 = y + (2 * self.__radius)

    def gety(self):
        return self.__y

    def setx2(self, x2):
        self.__x2 = x2
        self.__x = x2 - (2 * self.__radius)

    def getx2(self):
        return self.__x2

    def sety2(self, y2):
        self.__y2 = y2
        self.__y = y2 - (2 * self.__radius)

    def gety2(self):
        return self.__y2

    def set_radius(self, radius):
        if self.__radius == radius:
            return
        self.__x = self.get_centerx() - radius
        self.__y = self.get_centery() - radius
        self.__radius = radius
        self.__occupant.set_size(radius)

    def get_radius(self):
        return self.__radius

    def get_vision_radius(self):
        return self.__radius + self.__occupant.get_vision()

    def get_occupant(self):
        return self.__occupant

    def set_color(self, color):
        self.__occupant.set_color(color)
        self.color_trigger()

    def get_color(self):
        return self.__occupant.get_color()

    def get_center(self):
        x = self.__x + self.__radius
        y = self.__y + self.__radius
        return x, y

    def get_centerx(self):
        return self.get_center()[0]

    def get_centery(self):
        return self.get_center()[1]

    def set_x_velocity(self, v):
        self.__occupant.set_x_velocity(v)

    def get_x_velocity(self):
        return self.__occupant.get_x_velocity()

    def set_y_velocity(self, v):
        self.__occupant.set_y_velocity(v)

    def get_y_velocity(self):
        return self.__occupant.get_y_velocity()

    def set_speed(self, v):
        self.__occupant.set_speed(v)

    def get_speed(self):
        return self.__occupant.get_speed()

    def set_reference(self, reference):
        self.__reference = reference
        self.__x2 = self.__x + (2 * self.__radius)
        self.__y2 = self.__y + (2 * self.__radius)

    def get_reference(self):
        return self.__reference

    def move(self):
        self.setx(self.__x + self.__occupant.get_x_velocity())
        self.sety(self.__y + self.__occupant.get_y_velocity())

    def reproduce(self):
        if isinstance(self.__occupant, ReproducingOccupant):
            self.__reproducing_trigger = False
            return self.__occupant.reproduce()

    def needs_vision(self):
        return self.get_occupant().needs_vision

    def is_plant(self):
        return isinstance(self.__occupant, plant.Plant)

    def update(self):
        self.__occupant.update()
        self.set_radius(self.__occupant.get_size())
        self.move()
        if isinstance(self.__occupant, ReproducingOccupant):
            if self.__occupant.reproducing():
                self.reproducing_trigger()
        if not self.__occupant.alive():
            self.kill_trigger()

    def collide_trigger(self):
        self.__collide_trigger = True

    def collide_triggered(self):
        return self.__collide_trigger

    def kill_trigger(self):
        self.__kill_trigger = True

    def kill_triggered(self):
        return self.__kill_trigger

    def highlight_trigger(self):
        self.__highlight_trigger = not self.__highlight_trigger

    def highlight_triggered(self):
        return self.__highlight_trigger

    def color_trigger(self):
        self.__color_trigger = not self.__highlight_trigger

    def color_triggered(self):
        return self.__color_trigger

    def ucolor_triggered(self):
        tf = self.__color_trigger
        self.__color_trigger = False
        return tf

    def reproducing_trigger(self):
        self.__reproducing_trigger = not self.__reproducing_trigger

    def reproducing_triggered(self):
        return self.__reproducing_trigger
