from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption("Ping Pong")

# initialize the font class
font.init()

font_1 = font.Font(None, 80)
font_2 = font.Font(None, 50)
font_3 = font.Font(None, 65)

# initialize the clock class
clock = time.Clock()

# transform.scale the background to the program
background = transform.scale(image.load("background.jpg"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        ran1 = randint(1, 2)
        ran2 = randint(1, 2)
        if ran1 == 1:
            self.speedx = 2
        else:
            self.speedx = -2
        
        if ran2 == 1:
            self.speedy = 2
        else:
            self.speedy = -2
        
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
        elif keys_pressed[K_s] and self.rect.y < 350:
            self.rect.y += self.speed

class Player2(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys_pressed[K_DOWN] and self.rect.y < 350:
            self.rect.y += self.speed

ball = Ball("ball.png", 330, 230, 40, 40, 5)

player_1 = Player1("paddle.png", 30, randint(10, 350), 50, 150, 7)
player_2 = Player2("paddle.png", 620, randint(10, 350), 50, 150, 7)

player1_score = 0
player2_score = 0

state = "start"

# finish = False
won = 1
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
            
    if state == "start":
        window.blit(background, (0, 0))
        start_txt = font_1.render("Ping Pong", 1, (255, 255, 255))
        window.blit(start_txt, (220, 130))

        multi_txt = font_3.render("Press ENTER for Multiplayer", 1, (255, 255, 255))
        window.blit(multi_txt, (45, 225))

        multi_txt = font_3.render("Press SPACE for Singleplayer", 1, (255, 255, 255))
        window.blit(multi_txt, (35, 310))

        if keys_pressed[K_SPACE]:
            state = "singleplayer"

            ball = Ball("ball.png", 330, 230, 40, 40, 5)

            player_1 = Player1("paddle.png", 30, randint(10, 350), 50, 150, 7)
            player_2 = Player2("paddle.png", 620, randint(10, 350), 50, 150, 7)

    elif state == "singleplayer":
        # render the background
        window.blit(background, (0, 0))

        # render the sprites
        ball.blit_image()

        player_1.blit_image()
        player_2.blit_image()

        player1_scoretxt = font_2.render("" + str(player1_score), 1, (255, 255, 255))
        player2_scoretxt = font_2.render("" + str(player2_score), 1, (255, 255, 255))

        window.blit(player1_scoretxt, (290, 80))
        window.blit(player2_scoretxt, (390, 80))
        # update the sprites
        player_1.update()
        player_2.update()
    
        ball.update()

        # detect the collision between the paddles and the ball
        if sprite.collide_rect(player_1, ball) or sprite.collide_rect(player_2, ball):
            ball.speedx *= -1

        if ball.rect.x < 1: 
            won = 2

            state = "gameover"
        elif ball.rect.x > 660:
            won = 1

            state = "gameover"
    
    elif state == "gameover":
        window.blit(background, (0, 0))

        if won == 1:
            player1_wins = font_1.render("Player 1 Wins", 1, (255, 255, 255))
            window.blit(player1_wins, (170, 180))
        elif won == 2:
            player2_wins = font_1.render("Player 2 Wins", 1, (255, 255, 255))
            window.blit(player2_wins, (170, 180))

        press_enter = font_1.render("Press Enter", 1, (255, 255, 255))
        window.blit(press_enter, (200, 270))
        
        if keys_pressed[K_RETURN]:
            state = "start"


    # always update the screen
    display.update()