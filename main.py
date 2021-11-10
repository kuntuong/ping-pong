from pygame import *
from random import randint

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
        self.speedx = 2
        self.speedy = 2
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.way_ball = randint(1, 4) 
    def blit_image(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ball(GameSprite):
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.y < 1:
            self.speedy *= -1
        elif self.rect.y > 480:
            self.speedy *= -1
class Player1(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys_pressed[K_s] and self.rect.y < 320:
            self.rect.y += self.speed

class Player2(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys_pressed[K_DOWN] and self.rect.y < 320:
            self.rect.y += self.speed

ball = Ball("ball.png", 330, 230, 40, 40, 5)

player_1 = Player1("paddle.png", -10, 10, 150, 180, 7)
player_2 = Player2("paddle.png", 555, 310, 150, 180, 7)

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

    # update the sprites
    player_1.update()
    player_2.update()
    
    ball.update()

    if sprite.collide_rect(player_1, ball) or sprite.collide_rect(player_2, ball):
        ball.speedx *= -1

    # always update the screen
    display.update()