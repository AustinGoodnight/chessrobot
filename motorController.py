
#import libraries
import time
from gpiozero import LED, Button
import numpy as np
#from pynput import keyboard
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



def binaryPlus(s):
    return '{:04b}'.format(1+ int(s,2))

def increment_4bit(bits):

    # convert bit array → int
    value = (bits[0] << 3) | (bits[1] << 2) | (bits[2] << 1) | bits[3]

    # increment mod 16
    value = (value + 1) & 0xF

    # write back into the same list
    bits[0] = (value >> 3) & 1
    bits[1] = (value >> 2) & 1
    bits[2] = (value >> 1) & 1
    bits[3] = value & 1

reed = np.zeros((8,8))

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
    mag.on()
    time.sleep(.5)
    motorController(-.5,'x') # back to edge
    motorController(-.5,'y') # back to edge
    motorController(x2-x1, 'x')
    motorController(y2-y1, 'y')
    motorController(.5,'x') # to center
    motorController(.5,'y') # to center
    mag.off()
    motorController((-x2),'x') # back to edge
    motorController((-y2),'y') # back to edge
    '''
    motorController((-x2)+1,'x')
    motorController((-y2)+1,'y')
    #motorController(-.5,'x') # to (0,0)
    motorController(-.5,'y') # to (0,0)
    '''

def locationOffEdge(x1,y1,x2,y2):
    motorController(x1,'x')
    motorController(y1,'y')
    mag.on()
    time.sleep(2)
    motorController(x2-x1, 'x')
    motorController(y2-y1, 'y')
    mag.off()
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

def translatey(y):
    #char input
    if y == 'a':
        yout = 1
    if y == 'b':
        yout = 2
    if y == 'c':
        yout = 3
    if y == 'd':
        yout = 4
    if y == 'e':
        yout = 5
    if y == 'f':
        yout = 6
    if y == 'g':
        yout = 7
    if y == 'h':
        yout = 8
    return yout

def translatex(x):
    return 9-x


while True:
    
    move = input("put next move (x,y) -> (x,y) as 'x,y,x,y'")
    moves = move.split(',')

    if moves[0] == 'e':
        quit()


    x1 = float(moves[1])
    y1 = translate(moves[0])
    x2 = float(moves[3])
    y2 = translate(moves[2])

    print("Moving from ", moves[0], moves[1], " to ", moves[2], moves[3])

    locationOnEdge(x1,y1,x2,y2)
    
