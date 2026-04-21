import tkinter
import random

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=800, height=800)
canvas.pack()

def ob(sirka, vyska, barva):
    x = random.randint(0, 600)
    y = random.randint(0, 600)
    canvas.create_rectangle(x, y, x + sirka, y + vyska, fill=barva)
    root.update()