from tkinter import *
import time


class Dot:
    __x = 0
    __y = 0
    __radius = 0

    def __init__(self, x, y, radius):
        self.__x = x
        self.__y = y
        self.__radius = radius

    def setx(self, x):
        self.__x = x

    def getx(self):
        return self.__x

    def sety(self, y):
        self.__y = y

    def gety(self):
        return self.__y

    def setradius(self, radius):
        self.__radius = radius

    def getradius(self):
        return self.__radius

