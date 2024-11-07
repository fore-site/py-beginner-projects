from turtle import Screen
from traffic import Traffic
from crossing_turtle import CrossingTurtle
from scoreboard import ScoreBoard
import time
import random

screen = Screen()
screen.setup(600,400)
screen.tracer(0)

y = -150

# initialize the crossing turtle and scoreboard

crossing_turtle = CrossingTurtle()
scoreboard = ScoreBoard()

screen.listen()
screen.onkey(key="Up", fun=crossing_turtle.move)

is_moving = True

traffic_list = []

# initialize the traffic
for _ in range(16):
    traffic = Traffic()
    traffic_list.append(traffic)


while is_moving:
    screen.update()
    for traffic in traffic_list:
        # move traffic from right to left
        traffic.move()
            # move turtle back to starting position for each new level
        if crossing_turtle.ycor() >= 200:
            crossing_turtle.teleport(0, -180)
            scoreboard.update_level()
                # increase speed of each turtle for each new level
            for each_traffic in traffic_list:
                each_traffic.increase_speed()
                # detect when game is over if turtle hits traffic
        if crossing_turtle.distance(traffic) <= 20:
            scoreboard.game_over()
            is_moving = False
            break


screen.exitonclick()