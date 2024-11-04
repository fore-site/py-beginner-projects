import turtle
import random

x = 0
class Snake:
    def __init__(self):
        self.snake_list = []
        self.create_snake()
        self.head = self.snake_list[0]

    def create_snake(self):
        global x
        for _ in range(3):
            self.snake = turtle.Turtle(shape="square")
            self.snake.penup()
            self.snake.color("white")
            self.snake.setx(x)
            self.snake_list.append(self.snake)
            x -= 20

    def move(self):
        for snake_num in range(len(self.snake_list) - 1, 0, -1):
            self.snake_list[snake_num].color("white")
            self.snake_list[snake_num].goto(self.snake_list[snake_num - 1].position())
        self.head.forward(20)

    def up(self):
        if self.head.heading() != 270.0:
            self.head.setheading(90)

    def down(self):
        if self.head.heading() != 90.0:
            self.head.setheading(270)
    
    def left(self):
        if self.head.heading() != 0:
            self.head.setheading(180)
    
    def right(self):
        if self.head.heading() != 180.0:
            self.head.setheading(0)

    def extend_snake(self):
        self.new_snake = turtle.Turtle(shape="square")
        self.new_snake.penup()
        # self.new_snake.color("white")
        self.snake_list.append(self.new_snake)
