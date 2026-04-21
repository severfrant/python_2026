import tkinter
import random

root = tkinter.Tk()
canvas = tkinter.Canvas(root, width=400, height=400)
canvas.pack()

def francie():
    canvas.create_rectangle(50, 50, 150, 250, fill="blue")
    canvas.create_rectangle(250, 50, 350, 250, fill="red")
    return "francie"
    
def svedsko():
    canvas.create_rectangle(50, 50, 350, 250, fill="navy")
    canvas.create_rectangle(50, 130, 350, 170, fill="gold")
    canvas.create_rectangle(140, 50, 180, 250, fill="gold")
    return "svedsko"
    
def polsko():    
    canvas.create_rectangle(50, 150, 350, 250, fill="red")
    return "polsko"
    
def irsko():
    canvas.create_rectangle(50, 50, 150, 250, fill="green")
    canvas.create_rectangle(250, 50, 350, 250, fill="orange")
    return "irsko"
    
def italie():
    canvas.create_rectangle(50, 50, 150, 250, fill="green")
    canvas.create_rectangle(250, 50, 350, 250, fill="red")
    return "italie"
    
def spanelsko():
    canvas.create_rectangle(50, 50, 350, 110, fill="red")
    canvas.create_rectangle(50, 110, 350, 190, fill="yellow")
    canvas.create_rectangle(50, 190, 350, 250, fill="red")
    canvas.create_oval(80, 130, 120, 170, fill="red")
    return "spanelsko"
    
def ukrajina():
    canvas.create_rectangle(50, 50, 350, 250, fill="DodgerBlue2")
    canvas.create_rectangle(50, 150, 350, 250, fill="yellow")
    return "ukrajina"
    
def vycisti():    
    #nakresli bílý obdelnik na souřadnicích (50, 50) a (350, 250)
    canvas.create_rectangle(50, 50, 350, 250, fill="white")
    return ""
   
   
#KOD CO JE TADY DAL NEMUSITE RESIT => IT JUST WORKS 
odpoved = input("Start? (ano/ne)\n")
print("==================================")
if (odpoved == "ano"):   
    skore = 0
    pocet = 0
    while (odpoved == "ano"):
        vycisti()
        root.update()
        
        flags = [francie, svedsko, polsko, irsko, italie, spanelsko, ukrajina]
        volba = random.choice(flags)
        spravne = volba()
        root.update()
        pocet += 1
        
        hadej = input("Jakého státu to je vlajka?\n")
        if (hadej == spravne):
            print("==================================")
            print("Správně!")
            skore += 1
            
        print("==================================")
        print("Současné skóre:", str(skore) + "/" + str(pocet))
        print("Úspěšnost:", str(round(skore/pocet*100, 2)) + "%")
        print("==================================")
        odpoved = input("Pokračovat? (ano/ne)\n")
        print("==================================")
        
    print("Finální skóre:", str(skore) + "/" + str(pocet))    
    print("Úspěšnost kvízu:", str(round(skore/pocet*100, 2)) + "%")