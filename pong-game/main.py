from turtle import Turtle, Screen
from paddle import Paddle
from ball import Ball
from divider import CreateDivide
import time
from score import Score

screen = Screen()
screen.bgcolor("black")
screen.setup(800,600)
screen.tracer(0)

game_on = True

paddle_r = Paddle(370)
paddle_l = Paddle(-380)

ball = Ball()
divider = CreateDivide()

score_left = Score(-50)
score_right = Score(50)

SPEED = 0.1

screen.listen()
screen.onkey(key="Up", fun=paddle_r.up)
screen.onkey(key="Down", fun=paddle_r.down)

screen.onkey(key="w", fun=paddle_l.up)
screen.onkey(key="s", fun=paddle_l.down)

while game_on:
    screen.update()
    time.sleep(SPEED)
    ball.move()

    # detect collision with up or down walls
    if ball.ycor() >= 280 or ball.ycor() <= -280:
        ball.bounce_y()

    # detect collision with paddles and the left or right wall     
    if ball.distance(paddle_r) <= 30 and ball.xcor() >= 370 or ball.distance(paddle_l) <= 30 and ball.xcor() <= -370:
        ball.bounce_x()
        SPEED *= 0.9

    # detect if right paddle misses ball    
    if ball.xcor() >= 400:
        ball.reset()
        SPEED = 0.1
        score_left.update_scoreboard(-50)

    # detect if left paddle misses ball
    if ball.xcor() <= -400:
        ball.reset()
        SPEED = 0.1
        score_right.update_scoreboard(50)

screen.exitonclick()