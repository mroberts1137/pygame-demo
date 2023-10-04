from tkinter import *
import numpy as np
import random
import time

screen_width = 500
screen_height = 400

tk = Tk()
canvas = Canvas(tk, width=screen_width, height=screen_height)
tk.title("Test")
canvas.pack()

class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vspeed = 2
        self.direction = random.randrange(360)
        self.xspeed = self.vspeed * np.cos(self.direction * np.pi / 180)
        self.yspeed = -self.vspeed * np.sin(self.direction * np.pi / 180)

        self.shape = canvas.create_oval(self.x, self.y, self.x + 20, self.y + 20, fill=color)

    def move(self):
        self.x += self.xspeed
        self.y += self.yspeed
        canvas.move(self.shape, self.xspeed, self.yspeed)
        pos = canvas.coords(self.shape)
        if self.x > screen_width - 20:
            self.xspeed = -self.xspeed
            self.x = screen_width - 20
        if self.x < 0:
            self.xspeed = -self.xspeed
            self.x = 0
        if self.y > screen_height - 20:
            self.yspeed = -self.yspeed
            self.y = screen_height - 20
        if self.y < 0:
            self.yspeed = -self.yspeed
            self.y = 0

colors = ['red', 'green', 'blue', 'orange', 'yellow', 'cyan', 'magenta', 'dodgerblue', 'turquoise', 'grey', 'gold', 'pink']

balls = []
for i in range(100):
    balls.append(Ball(random.randrange(screen_width), random.randrange(screen_height), random.choice(colors)))


while True:

    for ball in balls:
        ball.move()

    tk.update()
    time.sleep(0.01)



canvas.mainloop()