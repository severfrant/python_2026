import tkinter
import random

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=800, height=800)
canvas.pack()
#tvůj kód odsud

canvas.create_oval(150, 150, 250, 250, fill="white")
canvas.create_oval(150, 250, 250, 350, fill="white")
canvas.create_oval(150, 350, 250, 450, fill="white")

while True:
    i = random.randint(2, 25)
    i *= 100

    if (i < 700):
        canvas.create_oval(150, 250, 250, 350, fill="yellow")
        print("YELLOW, delay:", i)
    elif (700 <= i <= 1500):        
        canvas.create_oval(150, 350, 250, 450, fill="green")
        print("GREEN, delay:", i)
    else:        
        canvas.create_oval(150, 150, 250, 250, fill="red")
        print("RED, delay:", i)

    #tvůj kód až sem
    root.update()
    root.after(i)
    
    canvas.create_oval(150, 150, 250, 250, fill="white")
    canvas.create_oval(150, 250, 250, 350, fill="white")
    canvas.create_oval(150, 350, 250, 450, fill="white")