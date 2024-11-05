from turtle import Turtle

class Score(Turtle):

    def __init__(self, xcor):
        super().__init__()
        self.color("white")
        self.teleport(xcor, 200)
        self.score_left = 0
        self.score_right = 0
        self.write(f"{self.score_left}", False, "center", ("Arial", 60, "normal"))
        self.hideturtle()

    def update_scoreboard(self,xcor):
        self.teleport(xcor, 200)
        self.clear()
        if xcor == 50:
            self.score_right += 1
            self.write(f"{self.score_right}", False, "center", ("Arial", 60, "normal"))
        else:
            self.score_left += 1
            self.write(f"{self.score_left}", False, "center", ("Arial", 60, "normal"))

    def game_over(self):
        self.teleport(0,0)
        self.write("GAME OVER", False, "center", ("Arial", 30, "normal"))
