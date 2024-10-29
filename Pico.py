import time
from machine import ADC, Pin, UART
from BLE_CEEO import Yell

# MIDI commands
NoteOn = 0x90
NoteOff = 0x80
velocity = {'off': 0, 'f': 80}

# Initialize BLE connection
p = Yell('Medha', verbose=True, type='midi')
p.connect_up()

# Set up ADC pins for piezo sensors and digital pins
piezo_pin1 = ADC(Pin(26))
piezo_pin2 = ADC(Pin(27))
digital_pin1 = Pin(14, Pin.IN)
digital_pin2 = Pin(15, Pin.IN)

# Thresholds for triggering notes
threshold1 = 10000
threshold2 = 500
threshold3 = 5000
threshold4 = 10000

# MIDI note settings for single notes
channel = 0
notes = {
    "C": 60,  # C note
    "G": 67,  # G note
    "E": 64,  # E note
    "D": 62   # D note
}

# UART setup for communication with the Dahal board
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Helper function to send MIDI notes
def send_midi(cmd, note, velocity_level):
    timestamp_ms = time.ticks_ms()
    tsM = (timestamp_ms >> 7 & 0b111111) | 0x80
    tsL = 0x80 | (timestamp_ms & 0b1111111)
    c = cmd | (0x0F & channel)
    payload = bytes([tsM, tsL, c, note, velocity[velocity_level]])
    p.send(payload)

# Helper function to send note info over UART
def send_note_to_lcd(note_name):
    uart.write(f"Note: {note_name}\n")

# Main loop to read sensors and play notes
try:
    while True:
        # Read sensor values
        sensor1_value = piezo_pin1.read_u16()
        sensor2_value = piezo_pin2.read_u16()
        sensor3_value = digital_pin1.value()
        sensor4_value = digital_pin2.value()

        # C note (sensor 1)
        if sensor1_value > threshold1:
            send_midi(NoteOn, notes["C"], 'f')
            send_note_to_lcd("C")
        else:
            send_midi(NoteOff, notes["C"], 'off')

        # G note (sensor 2)
        if sensor2_value > threshold2:
            send_midi(NoteOn, notes["G"], 'f')
            send_note_to_lcd("G")
        else:
            send_midi(NoteOff, notes["G"], 'off')

        # E note (sensor 3)
        if sensor3_value > threshold3:
            send_midi(NoteOn, notes["E"], 'f')
            send_note_to_lcd("E")
        else:
            send_midi(NoteOff, notes["E"], 'off')

        # D note (sensor 4)
        if sensor4_value > threshold4:
            send_midi(NoteOn, notes["D"], 'f')
            send_note_to_lcd("D")
        else:
            send_midi(NoteOff, notes["D"], 'off')

        time.sleep(0.1)

finally:
    p.disconnect()
