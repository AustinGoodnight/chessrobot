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
