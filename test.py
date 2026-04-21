def nasobky_x(x, min, max):
    for i in range(min, max + 1):
        if (i % x == 0):
            print(i, end=" ")
            
nasobky_x(2, 1, 15)