from pygame import *

# initialize the font class
font.init()

# initialize the clock class
clock = time.Clock()

game = True
while game:
    # call the keys pressed and FPS times
    keys_pressed = key.get_pressed()
    clock.tick(60)
    print("hello")
    for e in event.get():
        # gives the player option to 
        # quit the game
        if e.type == QUIT:
            game = False

    # always update the screen
    display.update()