from time import sleep

import usb_midi
import adafruit_midi
from adafruit_midi.note_off import NoteOff
from adafruit_midi.note_on import NoteOn

import board
import busio

from digitalio import DigitalInOut, Direction, Pull
from adafruit_neotrellis.neotrellis import NeoTrellis
from adafruit_neotrellis.multitrellis import MultiTrellis

i2c_bus = busio.I2C(board.SCL, board.SDA)

int_pin = DigitalInOut(board.D5)
int_pin.direction = Direction.INPUT
int_pin.pull = Pull.DOWN

trelli = [
    [NeoTrellis(i2c_bus, False, addr=0x2F),
     NeoTrellis(i2c_bus, False, addr=0x2e)],
    [NeoTrellis(i2c_bus, False, addr=0x32),
     NeoTrellis(i2c_bus, False, addr=0x30)]
]
trellis = MultiTrellis(trelli)

# light up all keys at start
for y in range(8):
	for x in range(8):
		trellis.color(y, x, 0x020202)
		sleep(0.01)

midi = adafruit_midi.MIDI(midi_out=usb_midi.ports[1], out_channel=0)


def XY(x, y, offset=-1):
    return ((y+offset)*8 + (x+offset))


OFF = (0,0,0)

RED     = (20,0,0) 
ORANGE  = (15,5,0) 
YELLOW  = (10,10,0)
GREEN   = (0,20,0) 
BLUE    = (0,0,20) 
PURPLE  = (10,0,20)
PINK    = (13,0,7) 

W25 = (5,5,5)
W50 = (15,15,15)
W75 = (25,25,25)
W100 = (35,35,35)

color = OFF

def momentary(color = OFF, off = -1, on = -1): #use to make key momentary
    if on == -1:
        on = color
    if off == -1:
        off = (round(on[0] / 5), round(on[1] / 5), round(on[2] / 5))
    return {'off': off, 'on': on, 'type': 'momentary'}

def latching(color = OFF, off = -1, on = -1): #use to make key latching
    if on == -1:
        on = color
    if off == -1:
        off = (round(on[0] / 5), round(on[1] / 5), round(on[2] / 5))
    #print('On: ', on, 'Off: ', off)
    return {'off': off, 'on': on, 'state': False, 'type': 'latching'}

# --------------------------------------------------------------------------------------

# BUTTONS  0 = button, 1 = pad data, 2 = midi data (need to change some code around to get this to work)

x = 0

BUTTONS = [
    [XY(1, 1), latching( RED    )],
    [XY(2, 1), latching( ORANGE )],
    [XY(3, 1), latching( YELLOW )],
    [XY(4, 1), latching( GREEN  )],
    [XY(5, 1), latching( BLUE   )],
    [XY(6, 1), latching( PURPLE )],
    [XY(7, 1), latching( PINK   )],

    [XY(1, 2), latching( OFF )],
    [XY(2, 2), latching( W25 )],
    [XY(3, 2), latching( W50 )],
    [XY(4, 2), latching( W75 )],
    [XY(5, 2), latching( W100 )],

    [XY(1, 3), latching( RED    )],
    [XY(2, 3), latching( ORANGE )],
    [XY(3, 3), latching( YELLOW )],
    [XY(4, 3), latching( GREEN  )],
    [XY(5, 3), latching( BLUE   )],
    [XY(6, 3), latching( PURPLE )],
    [XY(7, 3), latching( PINK   )],

    [XY(1, 4), latching( OFF )],
    [XY(2, 4), latching( W25 )],
    [XY(3, 4), latching( W50 )],
    [XY(4, 4), latching( W75 )],
    [XY(5, 4), latching( W100 )],

    [XY(1, 5), latching( OFF )],
    [XY(2, 5), latching( W25 )],
    [XY(3, 5), latching( W50 )],
    [XY(4, 5), latching( W75 )],
    [XY(5, 5), latching( W100 )],


    [XY(1, 7), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(2, 7), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(3, 7), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(4, 7), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(5, 7), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(6, 7), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(7, 7), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(8, 7), latching( off = (5,5,5), on = (5,2,2) )],

    [XY(1, 8), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(2, 8), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(3, 8), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(4, 8), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(5, 8), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(6, 8), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(7, 8), latching( off = (5,5,5), on = (5,2,2) )],
    [XY(8, 8), latching( off = (5,5,5), on = (5,2,2) )],
    
]

# --------------------------------------------------------------------------------------

buttonData = [{}, {}]  # [{key nums: data}, {key nums: midi data}]
keys = [] # [keynum] -> [1 = key data [momentary, latching]], [2 = midi data (int or tuple)]

for button in BUTTONS:
    buttonData[0].update({button[0]: button[1]})  # add key data
    #buttonData[1].update({button[0]: button[2]})  # add midi data

for keynum in range(0, 64):
    stuff = [
        keynum,
        buttonData[0].get(keynum, {'off': OFF, 'on': OFF, 'type': 'empty'}),
        buttonData[1].get(keynum, 0)
    ]

    keys.append(stuff)

# --------------------------------------------------------------------------------------

def blink(xcoord, ycoord, edge):
    padNum = XY(xcoord, ycoord, 0)

    if edge == NeoTrellis.EDGE_RISING:
        # print('key press! ', padNum)
        
        if keys[padNum][1]['type'] is 'momentary':
            print('momentary ', padNum, ' on')
            #midi.send(NoteOn(keys[padNum][2], 120))
            midi.send(NoteOn(padNum))

            color = keys[padNum][1]['on']
            trellis.color(xcoord, ycoord, color)

        elif keys[padNum][1]['type'] is 'latching':
            #midi.send(NoteOn(keys[padNum][2], 120))
            midi.send(NoteOn(padNum))

            if not keys[padNum][1]['state']:
                color = keys[padNum][1]['on']
                print('latching ', padNum, ' on ', keys[padNum])

            elif keys[padNum][1]['state']:
                color = keys[padNum][1]['off']
                print('latching ', padNum, ' off ', keys[padNum])

            trellis.color(xcoord, ycoord, color)
            keys[padNum][1]['state'] = not keys[padNum][1]['state']

        elif keys[padNum][1]['type'] is 'empty':
            print('Empty')

    elif edge == NeoTrellis.EDGE_FALLING:
        # print('key release! ', padNum)
        if keys[padNum][1]['type'] is 'momentary':
            print('momentary ', padNum, ' off')
            color = keys[padNum][1]['off']
            trellis.color(xcoord, ycoord, color)

# turn off all keys now. this way you can tell if anything errored between line 32 and here
for y in range(8):
    for x in range(8):
        trellis.color(x, y, keys[XY(x, y, 0)][1]['off'])
        trellis.activate_key(x, y, NeoTrellis.EDGE_RISING)
        trellis.activate_key(x, y, NeoTrellis.EDGE_FALLING)
        trellis.set_callback(x, y, blink)
        sleep(0.01)

while True:
    trellis.sync()
    sleep(0.01)
