from turtle import Turtle, colormode
import random

colormode(255)

colors_list = [(149, 75, 50), (222, 201, 136), (53, 93, 123), (170, 154, 
41), (138, 31, 20), (134, 163, 184), (197, 92, 73), (47, 121, 86), (73, 43, 35), (145, 178, 149), (14, 98, 70), (232, 176, 165), (160, 142, 158), (54, 45, 50), (101, 75, 77), (183, 205, 171), (36, 60, 74), (19, 86, 89), (82, 148, 129), (147, 17, 19), (27, 68, 102), (12, 70, 64), (107, 127, 153), (176, 192, 208), (168, 99, 102), (66, 64, 60), (219, 178, 183), (178, 198, 202), (112, 139, 141), (254, 194, 0)]

rainbow = ['red', 'blue', 'green', 'indigo', 'orange', 'yellow', 'violet', 'purple', 'black']

class Traffic(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(1,2,None)
        self.color(random.choice(rainbow))
        self.setx(random.randint(300,1000))
        self.SPEED = 0.5
        self.sety(random.randint(-150,150))

    def move(self):
        self.backward(self.SPEED)
        if self.xcor() < -320:
            self.teleport(320, random.randint(-150, 150))

    def increase_speed(self):
        if self.speed() < 10:
            self.SPEED += 0.5
        else:
            pass
