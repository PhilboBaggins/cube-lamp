from machine import Pin, PWM
import time
import math

PIN_NUM_RED_1 = 17
PIN_NUM_RED_2 = 15
PIN_NUM_RED_3 = 26
PIN_NUM_RED_4 = 7

PIN_NUM_GRN_1 = 16
PIN_NUM_GRN_2 = 14
PIN_NUM_GRN_3 = 27
PIN_NUM_GRN_4 = 6

PIN_NUM_BLU_1 = 18
PIN_NUM_BLU_2 = 13
PIN_NUM_BLU_3 = 28
PIN_NUM_BLU_4 = 5

PIN_NUM_ALL_RED = [PIN_NUM_RED_1, PIN_NUM_RED_2, PIN_NUM_RED_3, PIN_NUM_RED_4]
PIN_NUM_ALL_GRN = [PIN_NUM_GRN_1, PIN_NUM_GRN_2, PIN_NUM_GRN_3, PIN_NUM_GRN_4]
PIN_NUM_ALL_BLU = [PIN_NUM_BLU_1, PIN_NUM_BLU_2, PIN_NUM_BLU_3, PIN_NUM_BLU_4]

DEFAULT_FREQ = 1000
DEFAULT_ITERATE_COLOUR_DELAY_MS = 5

def iterateColour(start, stop, step, delay):
    for i in range(int(start), int(stop), int(step)):
        #print(hex(i))
        yield i * i
        time.sleep_ms(delay)

def iterateColourUp(delay=DEFAULT_ITERATE_COLOUR_DELAY_MS):
        yield from iterateColour(0x0000, math.sqrt(0xFFFF), 1, delay)

def iterateColourDown(delay=DEFAULT_ITERATE_COLOUR_DELAY_MS):
        yield from iterateColour(math.sqrt(0xFFFF), 0x0000, -1, delay)

class CubeBoard:
    def __init__(self):
        self.ledRed = list(map(lambda p: PWM(Pin(p)), PIN_NUM_ALL_RED))
        self.ledGrn = list(map(lambda p: PWM(Pin(p)), PIN_NUM_ALL_GRN))
        self.ledBlu = list(map(lambda p: PWM(Pin(p)), PIN_NUM_ALL_BLU))

        for led in self.ledRed:
            led.freq(DEFAULT_FREQ)
        for led in self.ledGrn:
            led.freq(DEFAULT_FREQ)
        for led in self.ledBlu:
            led.freq(DEFAULT_FREQ)

    def setRed(self, duty):
        duty = int(duty)
        for led in self.ledRed:
            led.duty_u16(duty)

    def setGrn(self, duty):
        duty = int(duty)
        for led in self.ledGrn:
            led.duty_u16(duty)

    def setBlu(self, duty):
        duty = int(duty)
        for led in self.ledBlu:
            led.duty_u16(duty)

    def set(self, r, g, b):
        self.setRed(r)
        self.setGrn(g)
        self.setBlu(b)

    def off(self):
        self.set(0, 0, 0)

    def onFull(self):
        self.set(0xFFFF, 0xFFFF, 0xFFFF)

    def iterateColour(self, rangeGenerator, r, g, b, delay):
        for i in rangeGenerator(delay):
            rr = i if r else 0
            gg = i if g else 0
            bb = i if b else 0
            cubeBoard.set(rr, gg, bb)

    def iterateColourUp(self, r=False, g=False, b=False, delay=DEFAULT_ITERATE_COLOUR_DELAY_MS):
        self.iterateColour(iterateColourUp, r, g, b, delay)

    def iterateColourDown(self, r=False, g=False, b=False, delay=DEFAULT_ITERATE_COLOUR_DELAY_MS):
        self.iterateColour(iterateColourDown, r, g, b, delay)

cubeBoard = CubeBoard()
cubeBoard.off()

# # Cycle through colours
# cubeBoard.set(0xFFFF, 0x0000, 0x0000)  # Just red
# time.sleep(1.0)
# cubeBoard.set(0x0000, 0xFFFF, 0x0000)  # Just green
# time.sleep(1.0)
# cubeBoard.set(0x0000, 0x0000, 0xFFFF)  # Just blue
# time.sleep(1.0)

while True:
    # Red
    cubeBoard.iterateColourUp(True, False, False, 1)
    cubeBoard.iterateColourDown(True, False, False, 5)

    # Green
    cubeBoard.iterateColourUp(False, True, False, 1)
    cubeBoard.iterateColourDown(False, True, False, 5)

    # Blue
    cubeBoard.iterateColourUp(False, False, True, 1)
    cubeBoard.iterateColourDown(False, False, True, 5)

#cubeBoard.off()
