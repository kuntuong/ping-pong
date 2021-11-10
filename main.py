from pygame import *

window = display.set_mode((700, 500))
display.set_caption("Ping Pong")

# initialize the font class
font.init()

# initialize the clock class
clock = time.Clock()

# transform.scale the background to the program
background = transform.scale(image.load("background.jpg"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def blit_image(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ball(GameSprite):
    def update():
        pass

class Paddle(GameSprite):
    def update():
        pass

ball = Ball("ball.png", 330, 230, 40, 40, 5)

player_1 = Ball("paddle.png", -10, 10, 150, 180, 5)
player_2 = Ball("paddle.png", 555, 310, 150, 180, 5)

game = True
while game:
    # call the keys pressed and FPS times
    keys_pressed = key.get_pressed()
    clock.tick(60)

    for e in event.get():
        # gives the player option to 
        # quit the game
        if e.type == QUIT:
            game = False

    # render the background
    window.blit(background, (0, 0))

    # render the sprites
    ball.blit_image()

    player_1.blit_image()
    player_2.blit_image()

    # always update the screen
    display.update()