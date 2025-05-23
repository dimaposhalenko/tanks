from pygame import *
from random import randint
from time import time as timer

# фонова музика
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
 
goal = 50


# шрифти і написи
font.init()
font1 = font.Font(None, 40)
font2 = font.Font(None, 36)
win = font1.render('ТИ КЛУТОЙ ПЕПСИКОЛЬНИЙ!', True, (255, 180, 51))
lose = font1.render('ТИ ОБОБА БАРАБУЛЬКА', True, (180, 0, 0))
font2 = font.Font(None, 36)


# нам потрібні такі картинки:
img_back = "galaxy.jpg"  # фон гри
img_hero = "rocket.png"  # герой
img_bullet = "bullet.png" # куля
img_enemy = "ufo.png"  # ворог
img_ast = "asteroid.png"



score = 0  # збито кораблів
lost = 0  # пропущено кораблів
max_lost = 3 # програли, якщо пропустили стільки
# клас-батько для інших спрайтів
class GameSprite(sprite.Sprite):
    # конструктор класу
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # викликаємо конструктор класу (Sprite):
        sprite.Sprite.__init__(self)
 
        # кожен спрайт повинен зберігати властивість image - зображення
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed
 
        # кожен спрайт повинен зберігати властивість rect - прямокутник, в який він вписаний
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
    # метод, що малює героя у вікні
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
# клас головного гравця
class Player(GameSprite):
    # метод для керування спрайтом стрілками клавіатури
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
 




    def fire (self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -35)
        bullets.add(bullet)  



# клас спрайта-ворога
class Enemy(GameSprite):
    # рух ворога
    def update(self):
        self.rect.y += self.speed
        global lost
        # зникає, якщо дійде до краю екрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()



# створюємо віконце
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# створюємо спрайти
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10)
 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster)












asteroids = sprite.Group()
for i in range(1, 6):
    asteroid = Enemy(img_ast, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    asteroids.add(asteroid)







bullets = sprite.Group()


# змінна "гра закінчилася": як тільки вона стає True, в основному циклі перестають працювати спрайти
finish = False
# Основний цикл гри:
run = True  # прапорець скидається кнопкою закриття вікна
 
num_fire = 0

rel_time = False

while run:
    # подія натискання на кнопку Закрити
    for e in event.get():
        if e.type == QUIT:
            run = False

        elif e.type == KEYDOWN:
            if e.key   == K_SPACE:
                if num_fire < 20 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()


                if num_fire >= 20 and rel_time == False:
                    last_time = timer()
                    rel_time = True

    if not finish:
        # оновлюємо фон
        window.blit(background, (0, 0))
 
        # пишемо текст на екрані
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
 
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        # рухи спрайтів
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()



        # оновлюємо їх у новому місці при кожній ітерації циклу
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)



        if rel_time:
            now_time = timer()



            if now_time - last_time < 3:
                reload = font2.render("ПЕРЕЗАРЯДКА ", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else: 
                num_fire = 0
                rel_time = False




 











        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)



        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))

        if score >= goal:
            finish = True
            window.blit(win, (200, 200))


        display.update()
    # цикл спрацьовує кожні 0.05 секунд
    time.delay(45)
