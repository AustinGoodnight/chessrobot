






def location(x1,y1,x2,y2):
    # go from current position (corner?) to x1,y1, turn mag on and go to x2,y2, then go back to corner

    motorController(x1, x)
    motorController(y1, y)
    magOn()
    motorController(x2-x1, x)
    motorController(y2-y1, y)
    magOff()
    motorController(-x2,x)
    motorController(-y2,y)