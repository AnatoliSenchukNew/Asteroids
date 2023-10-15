from typing import Any
from pygame import*
from random import*

w, h = 700, 500
window = display.set_mode((w, h))
display.set_caption("Asteroids")

game = True
finish = False
clock = time.Clock()
FPS = 60
background = transform.scale(image.load("galaxy.jpg"), (w, h))
class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        super().__init__()
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx-7, self.rect.top, 15,30,15)
        bullets.add(bullet)

ship = Player("gogo.png",10, h-100,65,95,4)

lost = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        global hearts
        if self.rect.y > h:
            try:
                hearts.pop(0)
            except:
                pass
            
            self.rect.y = 0
            self.rect.x = randint(0,w-50)
            lost = lost + 1

asteroids = sprite.Group()

for i in range(6):
        pics = ["gigi.png", "papa.png"]
        asteroid = Enemy(choice(pics), randint(0, w-50), -40, 50, 50, 1)
        asteroids.add(asteroid)     

score = 0




class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()



bullets = sprite.Group()
mixer.init()
mixer.music.load("hightweight.mp3")
mixer.music.play() 

fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.2)

font.init()
mainfount = font.Font("HFHourglass.ttf",40)



from time import time as timer
reload_time = False
num_fire = 0

hearts = []
lives = 10
hX = 300
for i in range(lives):
    heart = GameSprite("HEART.png",hX,10,40,37,0)
    hearts.append(heart)
    hX += 40 

restart = (GameSprite("RESTART.png", 655, 50 ,40,37,100))
vuxid = (GameSprite("exit.png", 650, 450, 40, 40, 37))


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and reload_time == False:
                    ship.fire()
                    fire_sound.play()
                    num_fire += 1
                if num_fire >= 10 and reload_time == False:
                    reload_time = True
                    reload_start = timer()
            if e.key == K_r and finish:
                num_fire = 0
                for a in asteroids:
                    a.rect.y = -100
                    a.rect.x = randint(0, w-100)
                score, lost , finish = 0,0,0
                hearts = []
                lives = 10
                hX = 300
                for i in range(lives):
                    heart = GameSprite("HEART.png", hX,10,40,37,0)
                    hearts.append(heart)
                    hX += 40
        if e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                x,y = e.pos
                if restart.rect.collidepoint(x,y) and finish:
                    num_fire = 0
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    score, lost , finish = 0,0,0
                    hearts = []
                    lives = 10
                    hX = 300
                    for i in range(lives):
                        heart = GameSprite("HEART.png", hX,10,40,37,0)
                        hearts.append(heart)
                        hX += 40
                if vuxid.rect.collidepoint(x,y):
                    game = False




    if not finish:
        
        window.blit(background,(0,0))
        score_text = mainfount.render("Killed: "+str(score), True,(0,255,0))
        lost_text = mainfount.render("Missed: "+str(lost), True,(0,255,0))
        window.blit(score_text, (5,10))
        window.blit(lost_text,(5,50))
         
        vuxid.draw()
        asteroids.update()
        asteroids.draw(window)
        ship.draw()
        ship.update()
        bullets.update()
        bullets.draw(window)
        restart.draw()
        for heart in hearts:
            heart.draw()


        if sprite.spritecollide(ship, asteroids, False):
            lose_text = mainfount.render("YOU LOSE", True, (0,255,0))
            window.blit(lose_text, (200, 200))
            finish = True

        collide = sprite.groupcollide(bullets,asteroids,True,True)
        for c in collide:
            score += 1
            pics = ["gigi.png", "papa.png"]
            asteroid = Enemy(choice(pics), randint(0, w-50), -40, 50, 50, 1)
            asteroids.add(asteroid)
        
        if reload_time:
            reload_end = timer()
            if reload_end - reload_start < 3:
                reload = mainfount.render("RELOADING...", True, (0,255,0))
                window.blit(reload, (200, 200))
            else:
                num_fire = 0
                reload_time = False
        
        if len(hearts) <= 0:
            lose_text = mainfount.render("YOU LOSE", True , (0,255,0))
            window.blit(lose_text,(200,200))
            finish = True

    display.update()
    clock.tick(60)


















