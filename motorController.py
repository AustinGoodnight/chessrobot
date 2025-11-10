# lets have a grid that represents spots on the board

# this grid starts at the bottom left corner, closet to the mounted motor, looking towards the other side

# the bottom is (0,0)

# this area is for storage

#this lowkey might be wrong depedning on how the board works out, but lets find out first

#written by Austin Goodnight

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
from pynput import keyboard
'''
PIN LAYOUT
^ more pins
00 01
05 g
06 12 (Y Direction 1) [step dir]
13 g  [electromagnet control]
19 16 [xstep] [dir]
26 20 [xstep] [dir]
g  21
USB PORT SIDE
'''

#this assigns each motor to an output on the pi
#one is an alernating control that moves the motor once per HIGH/LOW
#the second changes the direction of this movement when HIGH
m1step = LED(20) #x
m1dir = LED(26)

m2step = LED(16) #y
m2dir = LED(19)


mag = LED(13)



'''
stepmode = 8 #inverse of step division // lower is faster but less precise
    #this is set on the board by default, has to match the physical board

squareSize = 58.7475 #size of squares

rotationLength = 54 #distance belt moves by one rotation

motorDelay = .05 #delay between motor pulses in microseconds // lower >> faster speed

halfPythagorean = 1/2 * squareSize * 1.41 #this is the distance to the center of any square from the corner

stepsPerRotation = 200 * stepmode #number of steps per rotation 
'''
# ^not using that anymore
# one rotation is 39mm
rotationLength = 39.0
stepsPerRotation = 3200
squareSize = 58.7475 #size of squares
halfPythagorean = 1/2 * squareSize * 1.41 #this is the distance to the center of any square from the corner
motorDelay = .05 #delay between motor pulses in microseconds // lower >> faster speed



def on_press(key):
    if ((key.char == ('w'))):
        m1dir.on()
        for i in range(300):
            
            m1step.on()
            time.sleep(motorDelay * .00005)
            m1step.off()
            time.sleep(motorDelay * .00005)
    if key.char == ('s'):
        m1dir.off()
        for i in range(300):
            m1step.on()
            time.sleep(motorDelay * .00005)
            m1step.off()
            time.sleep(motorDelay * .00005)

    if key.char == ('a'):
        m2dir.off()
        for i in range(300):
            
            m2step.on()
            time.sleep(motorDelay * .00005)
            m2step.off()
            time.sleep(motorDelay * .00005)

    if key.char == ('d'):
        m2dir.on()
        for i in range(300):
            m2step.on()
            time.sleep(motorDelay * .00005)
            m2step.off()
            time.sleep(motorDelay * .00005)

def on_release(key):
    print('release')
    held = False

def startKB():
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()


def motorController(distance, axis):

    if distance < 0: #if distance is negative, set direction to HIGH 
        m1dir.off()
        m2dir.off()
        dist = -distance
    else:
        dist = distance
        m1dir.on()
        m2dir.on()

    #calculate steps based on factors
    steps = int(((dist * squareSize) / rotationLength) * stepsPerRotation)

    if axis == 'x': #for x axis, control two x axis motors
        for i in range(steps):
            m1step.on()
            time.sleep(motorDelay * .00005)
            m1step.off()
            time.sleep(motorDelay * .00005)

    else: # for y axis, control the y axis motor (m2)
        for i in range(steps):
            m2step.on()
            time.sleep(motorDelay * .00005)
            m2step.off()
            time.sleep(motorDelay * .00005)

    #ensure motor direction is set to LOW
    m1dir.off()
    m2dir.off()


def toCenter():

    #moves piece from corner to center

    steps = (halfPythagorean / rotationLength) * stepsPerRotation #calc steps

    #move to center

    for i in steps:

    #output to pin (m1)

    #output to pin (m2)

        time.sleep(motorDelay * .0001)


def toCorner():

    steps = (halfPythagorean / rotationLength) * stepsPerRotation #calc steps

    for i in steps:

    #direction pin active

    #output to pin (m1)

    #output to pin (m2)

        time.sleep(motorDelay * .0001)


#directly addressing these is probably better
#originally I thought there might be more coding needed
def magOn():
    mag.on()

def magOff():
    mag.off()

'''
while True:
    #script that allows for continual manual entering of moves for testing

    move = input("put next move (x,y)")
    if move == 'k':
        startKB()
    while():
        m1dir.off()
        m1step.on()
        time.sleep(motorDelay * .00005)
        m1step.off()
        time.sleep(motorDelay * .00005)
    while():
        m1dir.on()
        m1step.on()
        time.sleep(motorDelay * .00005)
        m1step.off()
        time.sleep(motorDelay * .00005)

    moves = move.split(',')

    x = int(moves[0])
    y = int(moves[1])

    motorController(x, 'x')
    motorController(y, 'y')
'''

def location(x1,y1,x2,y2):
    motorController(x1,'x')
    motorController(y1,'y')
    magOn()
    time.sleep(2)
    motorController(x2-x1, 'x')
    motorController(y2-y1, 'y')
    magOff()
    motorController(-x2,'x')
    motorController(-y2,'y')


while True:
    mag.off()
    move = input("put next move (x,y) -> (x,y) as 'x,y,x,y'")
    moves = move.split(',')

    x1 = int(moves[0])
    y1 = int(moves[1])
    x2 = int(moves[2])
    y2 = int(moves[3])

    location(x1,y1,x2,y2)




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