from turtle import Turtle

class Score(Turtle):

    def __init__(self):
        super().__init__()
        self.score_text = 0
        self.color("white")
        self.penup()
        self.sety(270)
        self.hideturtle()
        self.write(f"Score: {self.score_text}", move=False, align="center", font=("Arial", 10, "normal"))

    def update_score(self):
        self.score_text += 1
        self.clear()
        self.write(f"Score: {self.score_text}", move=False, align="center", font=("Arial", 10, "normal"))

    def game_over(self):
        self.goto(0,0)
        self.write("GAME OVER", False, "center")