# lets have a grid that represents spots on the board

# this grid starts at the bottom left corner, closet to the mounted motor, looking towards the other side

# the bottom is (0,0)

# this area is for storage

#this lowkey might be wrong depedning on how the board works out, but lets find out first



'''
MOTOR TESTING

MOTOR I
with real driver:
    single power source, worked currently once currend was adjusted
with real driver in assembly
with fake driver:
    single power soruce, could not get work work (motor vibrated), possibly because current struggled to be adjusted
    (trying on broken motor just in case)

MOTOR II
with real driver:
    single power source, gets stuck and varies speed even with current adjustmnet
with fake driver:

MOTOR III
with real driver:
    not tested but seems to work flawlessy
with fake driver:









'''

'''

8

7

6

5

4

3

2

1

0 1 2 3 4 5 6 7 8


0 = storage

'''


import time
from gpiozero import LED
'''
PIN LAYOUT
^ more pins
x  x
x  x
35 36
37 38
g  x
USB PORT SIDE
'''
m1step = LED(26)
m1dir = LED(20)

m2step = LED(19)
m2dir = LED(16)


stepmode = 4 #inverse of step division // lower is faster but less precise

squareSize = 58.7475 #size of squares

rotationLength = 54 #distance belt moves by one rotation

motorDelay = .1 #delay between motor pulses in microseconds // lower >> faster speed

halfPythagorean = 1/2 * squareSize * 1.41

stepsPerRotation = 200 * stepmode #number of steps per rotation 


def motorController(distance, axis):

    if distance < 0:
        m1dir.on()
        m2dir.on()
        dist = -distance
    else:
        dist = distance

    steps = int(((dist * squareSize) / rotationLength) * stepsPerRotation)

    if axis == 'x':
        for i in range(steps):

        #output to pin (selected by motor)
            m1step.on()
            time.sleep(motorDelay * .00005)
            m1step.off()
            time.sleep(motorDelay * .00005)


    else:

        #set pin for y axis

        print("code this dumbass")

        for i in range(steps):

            m2step.on()
            time.sleep(motorDelay * .00005)
            m2step.off()
            time.sleep(motorDelay * .00005)

    m2dir.off()
    #calculate steps




def toCenter():

    #moves piece from corner to center

    steps = (halfPythagorean / rotationLength) * stepsPerRotation

    #move to center

    for i in steps:

    #output to pin (m1)

    #output to pin (m2)

        time.sleep(motorDelay * .0001)


def toCorner():

    steps = (halfPythagorean / rotationLength) * stepsPerRotation

    for i in steps:

    #direction pin active

    #output to pin (m1)

    #output to pin (m2)

        time.sleep(motorDelay * .0001)


def magOn():

    #turn electromagnet on

    print("code this dumbass")


def magOff():

    #turn electromagnet off

    print("code this dumbass")


while True:

    move = input("put next move (x,y)")

    moves = move.split(',')


    x = int(moves[0])

    y = int(moves[1])


    motorController(x, 'x')

    motorController(y, 'y')


'''

code example


motorcontroller(5,x)

motorctronoller(3,y)

# goes to (5,3)


toCenter()

magOn() # grabs piece

toCorner()


motorcontroller(2,x)

motorcontroller(1,y)

#moves it +2x +1y, this would need to be calulated


magOff()


#after should probably go to corner to recalibrate, etc. 


'''