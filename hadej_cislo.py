import random

fin = random.randint(1, 5)
print("Hadej cislo od 1 do 5... \n")

def zkus(cislo):
    if (cislo == fin):
        print("Pecka, uhádl jsi.")
    else:
        print("Nee, zkus znovu!")