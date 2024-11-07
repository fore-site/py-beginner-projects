from turtle import Turtle

class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.penup()
        self.hideturtle()
        self.teleport(-240,170)
        self.level = 1
        self.write(f"Level: {self.level}", False, "center",("Courier", 15, "normal"))

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", False, "center", ("Courier", 20, "normal"))

    def update_level(self):
        self.level += 1
        self.clear()
        self.write(f"Level: {self.level}", False, "center",("Courier", 15, "normal"))
