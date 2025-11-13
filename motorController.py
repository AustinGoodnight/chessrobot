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







#import libraries
import time
from gpiozero import LED, Button
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


#x-direction
m1step = LED(20) 
m1dir = LED(26)

#y-direction
m2step = LED(16)
m2dir = LED(19)

#magnet on/off on = on. off = off.
mag = LED(6)

S = [0,0,0,0]
S0 = LED(17)
S1 = LED(27)
S2 = LED(22)
S3 = LED(23)

mux1 = Button(5, pull_up=True)
mux2 = Button(12, pull_up=True)
mux3 = Button(24, pull_up=True)
mux4 = Button(25, pull_up=True)



rotationLength = 39.0
stepsPerRotation = 3200
squareSize = 58.7475 #size of squares -> real size is 55, meaning there's a mismatch between this value and rotationLength
                    # for the time being, it works and I don't think it would make much sense to change it
halfPythagorean = 1/2 * squareSize * 1.41 #this is the distance to the center of any square from the corner // NOT USED
motorDelay = .05 #delay between motor pulses in microseconds // lower >> faster speed





def reedSensors():
    S1.off()
    S0.off()
    S2.off()
    S3.off()
    if Button.is_pressed:
        print('active')
    else:
        print('inactive')



#this allows for keyboard control of gantry
#normally not used, mainly for testing
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

def locationOnEdge(x1,y1,x2,y2):
    #goes from 0,0 to x1,y1
    #grabs piece then goes to x2,y2
    #then goes back to 0,0
    #all along the edges
    motorController(.5,'x') # to edge
    motorController(.5,'y') # to edge
    motorController(x1-1,'x')
    motorController(y1-1,'y')
    motorController(.5,'x') # to center
    motorController(.5,'y') # to center
    magOn()
    time.sleep(.5)
    motorController(-.5,'x') # back to edge
    motorController(-.5,'y') # back to edge
    motorController(x2-x1, 'x')
    motorController(y2-y1, 'y')
    motorController(.5,'x') # to center
    motorController(.5,'y') # to center
    magOff()
    motorController(-.5+(-x2)+1,'x') # back to edge
    motorController(-.5+(-y2)-.5,'y') # back to edge
    '''
    motorController((-x2)+1,'x')
    motorController((-y2)+1,'y')
    #motorController(-.5,'x') # to (0,0)
    motorController(-.5,'y') # to (0,0)
    '''

def locationOffEdge(x1,y1,x2,y2):
    motorController(x1,'x')
    motorController(y1,'y')
    magOn()
    time.sleep(2)
    motorController(x2-x1, 'x')
    motorController(y2-y1, 'y')
    magOff()
    motorController(-x2,'x')
    motorController(-y2,'y')


def edgeTraceX():
    mag.on()
    motorController(1.5,'y')
    motorController(8, 'x')

    time.sleep(5)
    motorController(-8,'x')
    motorController(-1.5,'y')
    mag.off()

def edgeTraceY():
    mag.on()
    motorController(1.5,'x')
    motorController(8, 'y')

    time.sleep(5)
    motorController(-8,'y')
    motorController(-1.5,'x')
    mag.off()

def spaceTest():
    mag.on()
    motorController(9,'y')
    for i in range(8):
        motorController(1, 'x')
        time.sleep(2)

    motorController(-8,'x')
    motorController(-9,'y')

while True:
    reedSensors()
    time.sleep(2)
    '''
    move = input("put next move (x,y) -> (x,y) as 'x,y,x,y'")
    moves = move.split(',')

    x1 = float(moves[0])
    y1 = float(moves[1])
    x2 = float(moves[2])
    y2 = float(moves[3])

    locationOffEdge(x1,y1,x2,y2)
    '''




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