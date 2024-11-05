from turtle import Turtle

class CreateDivide(Turtle):

    def __init__(self):
        super().__init__()
        self.color("white")
        self.is_moving = True
        self.pensize(3)
        self.teleport(0,400)
        self.setheading(270)
        self.score_left = 0
        self.score_right = 0

        while self.is_moving:
            self.forward(10)
            self.penup()
            self.forward(10)
            self.pendown()
            if self.pos()[1] <= -400:
                self.is_moving = False
