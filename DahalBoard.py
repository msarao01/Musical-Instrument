from machine import Pin, SoftI2C, UART
import ssd1306

# I2C setup for SSD1306 display
i2c = SoftI2C(scl=Pin(7), sda=Pin(6))
screen = ssd1306.SSD1306_I2C(128, 64, i2c)

# UART setup to receive messages from Raspberry Pi Pico
uart = UART(1, baudrate=9600, tx=Pin(4), rx=Pin(5))

# Function to display note on LCD
def display_note_on_lcd(note):
    screen.fill(0)  # Clear the screen
    screen.text(f'Note: {note}', 0, 0, 1)  # Display note text
    screen.show()

# Main loop to receive UART messages and display them
while True:
    if uart.any():
        note_data = uart.read().decode('utf-8').strip()  # Read and decode message
        if "Note:" in note_data:
            note = note_data.split(":")[1].strip()
            display_note_on_lcd(note)
