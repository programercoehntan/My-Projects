#Create your own shooter
from random import randint
from pygame import *
#classes
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global missed
        #if reach edges of window, enemies disappear
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            missed = missed + 1
class Obstacle(GameSprite):
    def update (self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width -80)
            



            
class Bullet (GameSprite):
    def update(self):
        self.rect.y += self.speed
        #dissapear when touch edge
        if self.rect.y < 0:
            self.kill() 
#variables
score = 0 #ships destroyed 
missed = 0 #ships failed to destroy
goal = 40
max_lost = 5

#fonts and captions goal
font.init()
displayText = font.Font('Minecraft.ttf', 20)

endText = font.Font('Minecraft.ttf', 36)
WIN = endText.render("You win!", True, (52, 235, 52))
LOSE = endText.render("You lose!", True, (217, 9, 9))

img_bg = "galaxy.png"
img_hero = "rocket.png"
img_asteroid = "asteroid.png"
img_bullet = "bullet.png"
 
#backgroudm music goal  Shooter game
mixer.init()
mixer.music.load("space.mp3")
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")#bullet sound goal
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Space Shooter-Shoot the aliens!!")
background = transform.scale(image.load(img_bg), (win_width, win_width))



#create sprite 35
ship = Player(img_hero, 5, win_height - 50, 40, 50, 8)
UFOs = sprite.Group()
for i in range(1, 6):
    img = randint(1,7)
    if img == 1 or img == 4 or img == 6 or img == 7:
        img_enemy = "ufo.png"
        ufo = Enemy(img_enemy, randint(80, win_width -80),-40, 60, 53, randint(2,4))
        UFOs.add(ufo)
    elif img == 2 :
        img_enemy = "ufo2.png"
        ufo = Enemy(img_enemy, randint(80, win_width -80),-40, 90, 70, randint(1,2))
        UFOs.add(ufo)
        
    else:
        img_enemy = "ufo3.png"
        ufo = Enemy(img_enemy, randint(80, win_width -80),-40, 55, 55, randint(4,5))
        UFOs.add(ufo)
    
asteroids = sprite.Group()
for i in range(1, 2):
    
    asteroid = Obstacle(img_asteroid, randint(80, win_width - 80), -40, 30, 52, randint(1, 2))
    asteroids.add(asteroid)
 


bullets = sprite.Group()

#whilw game font

game = True
finish = False
FPS = 60
clock = time.Clock()

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()

    if not finish:
        window.blit(background, (0,0))
        bullets.update()
        ship.update()
        ship.reset()
        UFOs.update()
        UFOs.draw(window)
        asteroids.update()
        asteroids.draw(window)
        bullets.draw(window)



        collides = sprite.groupcollide(UFOs, bullets, True, True)
        for c in collides:
            score += 1
            img = randint(1,7)
            if img == 1 or img == 4 or img == 6 or img == 7:
                img_enemy = "ufo.png"
                ufo = Enemy(img_enemy, randint(80, win_width -80),-40, 60, 53, randint(2,4))
                UFOs.add(ufo)
            elif img == 2:
                img_enemy = "ufo2.png"
                ufo = Enemy(img_enemy, randint(80, win_width -80),-40, 90, 70, randint(1,2))
                UFOs.add(ufo)
                
            else:
                img_enemy = "ufo3.png"
                ufo = Enemy(img_enemy, randint(80, win_width -80),-40, 55, 55, randint(4,5))
                UFOs.add(ufo)

        collides = sprite.groupcollide(UFOs, bullets, True, True)
        
            

        if missed >= max_lost or sprite.spritecollide(ship, asteroids, False):
            finish = True
            window.blit(LOSE, (300,200))

        if score >= goal:
            finish = True
            window.blit(WIN, (300,200))  

        SCORE =  displayText.render("SCORE: " + str(score), 1, (255,255,255))
        window.blit(SCORE, (10, 20))

        MISSED =  displayText.render("MISSED: "+ str(missed), 1, (255,255,255))
        window.blit(MISSED, (10, 50))
        display.update()
        clock.tick(FPS)



