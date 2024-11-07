from turtle import Turtle

class CrossingTurtle(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("turtle")
        self.penup()
        self.setheading(90)
        self.teleport(0, -180)

    def move(self):
        self.forward(20)
        