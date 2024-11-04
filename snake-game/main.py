from turtle import Screen
import snake
import food
import random
import time
import scoreboard

screen = Screen()
screen.setup(height=600, width=600)
screen.bgcolor("black")
screen.title("My snake game")
screen.tracer(0)

game_is_on = True

snake = snake.Snake()
screen.listen()
food = food.Food()

scoreboard = scoreboard.Score()

screen.onkey(key='Up',fun=snake.up)
screen.onkey(key='Down',fun=snake.down)

screen.onkey(key='Left',fun=snake.left)
screen.onkey(key='Right',fun=snake.right)

while game_is_on:
    screen.update()
    time.sleep(0.1)
    snake.move()

    #check if snake eats food
    if int(snake.head.distance(food)) <= 15:
        scoreboard.update_score()
        snake.extend_snake()
        food.teleport(random.randint(-280,280), random.randint(-280,280))

    #check if snake hits wall
    if int(snake.head.xcor()) >= 300 or int(snake.head.xcor()) <= -300 or int(snake.head.ycor()) >= 300 or int(snake.head.ycor() <= -300):
        scoreboard.game_over()
        game_is_on = False

    #check if snake hits itself
    for each_snake in snake.snake_list[1:]:
        if snake.head.distance(each_snake) < 10:
                scoreboard.game_over()
                game_is_on = False


screen.exitonclick()