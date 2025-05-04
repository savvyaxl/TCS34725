print("Hello World!")
print("Hello World! 2")
import board
import digitalio
ledpin = digitalio.DigitalInOut(board.D3)
ledpin.direction = digitalio.Direction.OUTPUT
ledpin.value = True
ledpin1 = digitalio.DigitalInOut(board.D5)
ledpin1.direction = digitalio.Direction.OUTPUT
ledpin1.value = False
print(ledpin)
print(dir(board))
print("Hello World! 3")
