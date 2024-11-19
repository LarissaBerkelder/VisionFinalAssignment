import board
import neopixel_spi

class led:

    def __init__(self):
        self.pixels = neopixel_spi.NeoPixel_SPI(board.SPI(), 6)
        self.mole_color = (255, 0, 0)

    def turn_off_led(self):
        self.pixels.fill((0, 0, 0))
        self.pixels.show()

    def turn_on_random_led(self, random_led):
        self.pixels[random_led] = self.mole_color
        self.pixels.show()   

    def turn_off_random_led(self, random_led):
        self.pixels[random_led] = (0, 0, 0)
        self.pixels.show()      