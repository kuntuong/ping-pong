from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption("Ping Pong")

mixer.init()

# initialize the font class
font.init()

font_1 = font.Font("font.ttf", 80)
font_2 = font.Font("font.ttf", 50)
font_3 = font.Font("font.ttf", 65)
font_4 = font.Font("font.ttf", 45)

# initialize the clock class
clock = time.Clock()

# transform.scale the background to the program
background = transform.scale(image.load("background.jpg"), (700, 500))
black_background = transform.scale(image.load("black_background.jpg"), (700, 500))

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(img), (width, height))
        ran1 = randint(1, 2)
        ran2 = randint(1, 2)
        self.ball_speed = 4
        if ran1 == 1:
            self.speedx = self.ball_speed
        else:
            self.speedx = -self.ball_speed
        
        if ran2 == 1:
            self.speedy = self.ball_speed
        else:
            self.speedy = -self.ball_speed
        
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

        wall_hit = mixer.Sound("sounds/wall_hit.wav")
        if self.rect.y < 1:
            self.speedy *= -1
            mixer.Sound.play(wall_hit)
        elif self.rect.y > 480:
            self.speedy *= -1
            mixer.Sound.play(wall_hit)

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

class Bot(GameSprite):
    def update(self):
        pass

ball = Ball("ball.png", 330, 230, 40, 40, 5)

player_1 = Player1("paddle.png", 30, randint(10, 350), 50, 150, 7)
player_2 = Player2("paddle.png", 620, randint(10, 350), 50, 150, 7)

player1_score = 0
player2_score = 0

state = "start"

paddle_hit = mixer.Sound("sounds/paddle_hit.wav")
score = mixer.Sound("sounds/score.wav")

singleplayer_point = 0
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
        if e.type == KEYDOWN:
            if e.key == K_ESCAPE:
                game = False
            
    if state == "start":
        window.blit(black_background, (0, 0))
        start_txt = font_1.render("Ping Pong", 1, (255, 255, 255))
        window.blit(start_txt, (170, 130))

        multi_txt = font_4.render("Press A for Multiplayer", 1, (255, 255, 255))
        window.blit(multi_txt, (27, 230))

        multi_txt = font_4.render("Press SPACE for Singleplayer", 1, (255, 255, 255))
        window.blit(multi_txt, (15, 300))

        if keys_pressed[K_a]:
            state = "multiplayer"

            ball = Ball("ball.png", 330, 230, 40, 40, 5)

            player_1 = Player1("paddle.png", 30, randint(10, 350), 50, 150, 7)
            player_2 = Player2("paddle.png", 620, randint(10, 350), 50, 150, 7)
        elif keys_pressed[K_SPACE]:
            state = "singleplayer"

            ball = Ball("ball.png", 330, 230, 40, 40, 5)

            player_bot = Bot("paddle.png", 30, randint(10, 350), 50, 150, 7)
            player_2 = Player2("paddle.png", 620, randint(10, 350), 50, 150, 7)

    elif state == "multiplayer":
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

        # detect the collision between the paddles and the ball
        if sprite.collide_rect(player_1, ball) or sprite.collide_rect(player_2, ball):
            ball.speedx *= -1
            mixer.Sound.play(paddle_hit)

        if ball.rect.x < 1:   
            won = 2
            mixer.Sound.play(score)
            state = "gameover"
        elif ball.rect.x > 660:
            won = 1
            mixer.Sound.play(score)
            state = "gameover"
    
    elif state == "singleplayer":
        # render the background
        window.blit(background, (0, 0))

        # render the sprites
        ball.blit_image()

        player_bot.blit_image()
        player_2.blit_image()

        # update the sprites
        player_bot.update()
        player_2.update()
    
        ball.update()

        player_bot.rect.y = ball.rect.y - 70

        # detect the collision between the paddles and the ball
        if sprite.collide_rect(player_bot, ball):
            ball.speedx *= -1
            mixer.Sound.play(paddle_hit)
            singleplayer_point += 1
        if sprite.collide_rect(player_2, ball):
            ball.speedx *= -1
            mixer.Sound.play(paddle_hit)

        if ball.rect.x < 1:   
            won = 4
            mixer.Sound.play(score)
            state = "gameover"
        elif ball.rect.x > 660:
            won = 3
            mixer.Sound.play(score)
            state = "gameover"

    elif state == "gameover":
        window.blit(black_background, (0, 0))

        if won == 1:
            player1_wins = font_1.render("Player 1 Wins", 1, (255, 255, 255))
            window.blit(player1_wins, (90, 180))
        elif won == 2:
            player2_wins = font_1.render("Player 2 Wins", 1, (255, 255, 255))
            window.blit(player2_wins, (90, 180))
        elif won == 3:
            player2_wins = font_1.render("Game Over", 1, (255, 255, 255))
            window.blit(player2_wins, (150, 120))

            player2_wins = font_1.render("Score: " + str(singleplayer_point), 1, (255, 255, 255))
            window.blit(player2_wins, (180, 190))
        elif won == 4:
            player2_wins = font_1.render("You Won!", 1, (255, 255, 255))
            window.blit(player2_wins, (180, 180))

        press_enter = font_1.render("Press Enter", 1, (255, 255, 255))
        window.blit(press_enter, (115, 270))
        
        if keys_pressed[K_RETURN]:
            state = "start"


    # always update the screen
    display.update()