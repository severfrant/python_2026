import tkinter
import random

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=800, height=800, bg="navy")
canvas.pack()

while True:
    barva = random.choice(["yellow", "orange", "aqua", "salmon", "gold", "green yellow", "white"])
    random_x = random.randint(1, 799)
    random_y = random.randint(1, 799)
    
    canvas.create_rectangle(random_x - 1, random_y - 1, random_x + 1, random_y + 1, fill=barva, outline=barva)
    print("New star: [x:", str(random_x) + ", y:", str(random_y) + "]")
    
    root.update()
    root.after(50)