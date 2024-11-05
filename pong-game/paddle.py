from turtle import Turtle

class Paddle(Turtle):
    
    def __init__(self, xcor):
        super().__init__()
        self.shape("square")
        self.penup()
        self.y = 0
        self.color("white")
        self.resizemode("user")
        self.shapesize(3,1,None)
        self.setx(xcor)

    def up(self):
        self.y += 20
        self.sety(self.y)
    
    def down(self):
        self.y -= 20
        self.sety(self.y)