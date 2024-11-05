from turtle import Turtle
import random

class Ball(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.penup()
        self.color("white")
        self.is_moving = True
        self.X_CONSTANT = 10
        self.Y_CONSTANT = 10
    
    def move(self):
        self.x = self.xcor() + self.X_CONSTANT
        self.y = self.ycor() + self.Y_CONSTANT
        self.goto(self.x, self.y)

    def bounce_y(self):
        self.Y_CONSTANT *= -1

    def bounce_x(self):
        self.X_CONSTANT *= -1

    def reset(self):
        self.goto(0,0)
        self.bounce_x()