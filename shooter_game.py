#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

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
        if keys[K_RIGHT] and self.rect.x < win_widht - 80:
            self.rect.x += self.speed
    def fire(self):
        pass

        

class Enemy(GameSprite):
    def update(self):
        global lost         
        global schot
        if self.rect.y <= win_heidht - 65:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(0, win_widht - 65)
            lost += 1
            schot += 1

class Bullet(GameSprite):
    def update(self):      
        global schot
        if self.rect.y >= 0:
            self.rect.y -= self.speed
        else:
            self.kill()

# class Wall(sprite.Sprite):
#     def __init__(self, color_1, color_2, color_3, wall_x, wall_y ,wall_width, wall_height):
#         super().__init__()
#         self.color_1 = color_1
#         self.color_2 = color_2
#         self.color_3 = color_3
#         self.width = wall_width
#         self.height = wall_height
#         self.image = Surface((self.width, self.height))
#         self.image.fill((color_1, color_2, color_3))
#         self.rect = self.image.get_rect()
#         self.rect.x = wall_x
#         self.rect.y = wall_y
#     def draw_wall(self):
#         window.blit(self.image, (self.rect.x, self.rect.y))

finish = False
win_widht = 700
win_heidht = 500
FPS = 60
schotchik = 0  

window = display.set_mode((win_widht, win_heidht))
display.set_caption('Догонялки')
background = transform.scale(image.load('galaxy.jpg'), (win_widht, win_heidht))

mixer.init() # подключение возможности использовать Mixer
mixer.music.load('space.ogg') # загрузить музык. файл для фона
mixer.music.play() # включить музыку для фона
music = mixer.Sound('fire.ogg')

font.init() # подключение возможности использовать Font

font = font.SysFont('Areal', 40) 

lost = 0
schot = 0
num_fire = 0
rel_time = False

# создать видимую надпись "YOU WIN" желтого цвета
# lose = font.render('YOU LOSE!', True, (255, 0, 0)) 

rocket = Player('rocket.png', 300, 400, 60, 80, 5)
asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy('asteroid.png', randint(0, win_widht - 65), 0, 80, 60, 1.5)
    asteroids.add(asteroid)


# группа инопланетян
monsters = sprite.Group()
for i in range(5):
    foe2 = Enemy('ufo.png', randint(0, win_widht - 65), 0, 80, 60, 1.5)
    monsters.add(foe2)

# группа пуль
bullets = sprite.Group()

game = True
clock = time.Clock()
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False

        if e.type == KEYDOWN:
            if e.key == K_SPACE: # нажатие 
                music.play()
                rocket.fire()
                if num_fire < 5:
                    weapon = Bullet('bullet.png', rocket.rect.centerx-7, rocket.rect.top, 15, 20, 15)
                    bullets.add(weapon)
                    num_fire += 1
                else:
                    last_time = timer()
                    rel_time = True

    if finish != True:
        window.blit(background, (0, 0))
        rocket.update()
        rocket.reset()
        asteroid.update()
        asteroid.reset()

        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()

        if rel_time == True:
            now_time = timer()

            if now_time - last_time < 3:
                reloud = font.render('Идет перезарядка, подождите ...', 1, (150, 0, 0))
                window.blit(reloud, (200, 400))
            else:
                num_fire = 0
                rel_time = True

        text_lose = font.render('Пропущено: ' + str(lost), 1, (255, 215, 255)) 
        text_schot = font.render('Счет: ' + str(schotchik), 1, (255, 215, 255))
        window.blit(text_schot, (20, 30))
        window.blit(text_lose, (20, 60))
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        if sprite_list != {}:
            schotchik += 1
            foe2 = Enemy('ufo.png', randint(0, win_widht - 65), 0, 80, 60, 1.5)
            monsters.add(foe2)

        sprite_list2 = sprite.spritecollide(rocket, monsters, False)

        sprite_list3 = sprite.spritecollide(rocket, asteroids, False)

        if lost >= 3 or sprite_list2 != []:
            finish = True
        if lost >= 3 or sprite_list3 != []:
            finish = True
            loser = font.render('Проигрыш', True, (255, 215, 255))
            window.blit(loser,(win_widht/2,win_heidht/2))
        if schotchik >= 10:
            finish = True
            win = font.render('Выиграл', True, (255, 215, 255))
            window.blit(win,(win_widht/2,win_heidht/2)) 

    display.update()
    clock.tick(FPS)

    