import pygame as p
import time
import threading

class Cat(p.sprite.Sprite, threading.Thread):
    def __init__(self):
        super(Cat, self).__init__()
        threading.Thread.__init__(self)
        self.x = 50
        self.y = HEIGHT / 2
        self.vel = 4
        self.width = 65
        self.height = 65
        
        p.init()
        self.est1 = p.image.load('./Img/est1.png')
        self.est2 = p.image.load('./Img/est2.png')
        self.est3 = p.image.load('./Img/est3.png')
        self.est4 = p.image.load('./Img/est4.png')
        self.est1 = p.transform.scale(self.est1, (self.width, self.height))
        self.est2 = p.transform.scale(self.est2, (self.width, self.height))
        self.est3 = p.transform.scale(self.est3, (self.width, self.height))
        self.est4 = p.transform.scale(self.est4, (self.width, self.height))

        self.image = self.est1
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.movement()
        self.correction()
        self.checkCollision()
        self.rect.center = (self.x, self.y)

    def movement(self):
        keys = p.key.get_pressed()
        if keys[p.K_LEFT]:
            self.x -= self.vel
            self.image = self.est2

        elif keys[p.K_RIGHT]:
            self.x += self.vel
            self.image = self.est1

        if keys[p.K_UP]:
            self.y -= self.vel
            self.image = self.est4

        elif keys[p.K_DOWN]:
            self.y += self.vel
            self.image = self.est3

    def correction(self):
        if self.x - self.width / 2 < 0:
            self.x = self.width / 2

        elif self.x + self.width / 2 > WIDTH:
            self.x = WIDTH - self.width / 2

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2

    def checkCollision(self):
        car_check = p.sprite.spritecollide(self, car_group, False, p.sprite.collide_mask)
        if car_check:
            explosion.explode(self.x, self.y)
        



class Car(p.sprite.Sprite, threading.Thread):
    def __init__(self, number):
        super(Car, self).__init__()
        threading.Thread.__init__(self)
        if number == 1:
            self.x = 190
            self.image = p.image.load('./Img/Slow Car.png')
            self.vel = -4

        else:
            self.x = 460
            self.image = p.image.load('./Img/Fast Car.png')
            self.vel = 5

        self.y = HEIGHT / 2
        self.width = 100
        self.height = 150
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        self.movement()
        self.rect.center = (self.x, self.y)

    def movement(self):
        self.y += self.vel

        if self.y - self.height / 2 < 0:
            self.y = self.height / 2
            self.vel *= -1

        elif self.y + self.height / 2 > HEIGHT:
            self.y = HEIGHT - self.height / 2
            self.vel *= -1


class Screen(p.sprite.Sprite, threading.Thread):
    def __init__(self):
        super().__init__()
        threading.Thread.__init__(self)
        self.img1 = p.image.load('./Img/Scene.png')
        self.img2 = p.image.load('./Img/You Win.png')
        self.img3 = p.image.load('./Img/You lose.png')

        self.img1 = p.transform.scale(self.img1, (WIDTH, HEIGHT))
        self.img2 = p.transform.scale(self.img2, (WIDTH, HEIGHT))
        self.img3 = p.transform.scale(self.img3, (WIDTH, HEIGHT))

        self.image = self.img1
        self.x = 0
        self.y = 0

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.topleft = (self.x, self.y)


class Flag(p.sprite.Sprite, threading.Thread):
    def __init__(self, number):
        super().__init__()
        threading.Thread.__init__(self)
        self.number = number

        if self.number == 1:
            self.image = p.image.load('./Img/qr.png')
            self.visible = False
            self.x = 50

        else:
            self.image = p.image.load('./Img/quesadilla.png')
            self.visible = True
            self.x = 580

        self.y = HEIGHT / 2
        self.image = p.transform.scale2x(self.image)
        self.rect = self.image.get_rect()
        self.mask = p.mask.from_surface(self.image)

    def update(self):
        if self.visible:
            self.collision()
            self.collision()
            self.rect.center = (self.x, self.y)

    def collision(self):
        global SCORE, cat
        
        flag_hit = p.sprite.spritecollide(self, cat_group, False, p.sprite.collide_mask)
        if flag_hit:
            self.visible = False

            if self.number == 1:
                white_flag.visible = True
                if SCORE < 10:
                    SwitchLevel()

                else:
                    cat_group.empty()
                    DeleteOtherItems()

                    EndScreen(1)

            else:
                green_flag.visible = True

class Explosion(object):
    def __init__(self):
        self.costume = 1
        self.width = 140
        self.height = 140
        self.image = p.image.load('./Img/explosion' + str(self.costume) + '.png')
        self.image = p.transform.scale(self.image, (self.width, self.height))

    def explode(self, x, y):
        x = x - self.width / 2
        y = y - self.height / 2
        DeleteCat()

        while self.costume < 9:
            self.image = p.image.load('./Img/explosion' + str(self.costume) + '.png')
            self.image = p.transform.scale(self.image, (self.width, self.height))
            win.blit(self.image, (x, y))
            p.display.update()

            self.costume += 1
            time.sleep(0.1)

        DeleteOtherItems()
        EndScreen(0)


def ScoreDisplay():
    global gameOn

    if gameOn:
        score_text = score_font.render('  '+str(SCORE), True, (0, 0, 0))
        win.blit(score_text, (255, 10))


def checkFlags():
    for flag in flags:
        if not flag.visible:
            flag.kill()

        else:
            if not flag.alive():
                flag_group.add(flag)


def SwitchLevel():
    global SCORE

    if slow_car.vel < 0:
        slow_car.vel -= 1

    else:
        slow_car.vel += 1

    if fast_car.vel < 0:
        fast_car.vel -= 1

    else:
        fast_car.vel += 1

    SCORE += 1


def DeleteCat():
    global cat

    cat.kill()

    screen_group.draw(win)
    car_group.draw(win)
    flag_group.draw(win)

    screen_group.update()
    car_group.update()
    flag_group.update()

    p.display.update()


def DeleteOtherItems():
    car_group.empty()
    flag_group.empty()
    flags.clear()

def EndScreen(n):
    global gameOn

    gameOn = False

    if n == 0:
        bg.image = bg.img3

    elif n == 1:
        bg.image = bg.img2

WIDTH = 640
HEIGHT = 480

def main():
    
    arreglo = []
    for i in range(1):
        arreglo.append(Cat())
        i+1

    for t in arreglo:
        t.start()
        print('Thread iniciado')
main()

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('UPChiapas')
clock = p.time.Clock()

SCORE = 0
score_font = p.font.SysFont('sans-serif', 80)

bg = Screen()
screen_group = p.sprite.Group()
screen_group.add(bg)

cat = Cat()
cat_group = p.sprite.Group()
cat_group.add(cat)

slow_car = Car(1)
fast_car = Car(2)
car_group = p.sprite.Group()
car_group.add(slow_car, fast_car)

green_flag = Flag(1)
white_flag = Flag(2)
flag_group = p.sprite.Group()
flag_group.add(green_flag, white_flag)
flags = [green_flag, white_flag]

explosion = Explosion()

gameOn = True
run = True
while run:
    clock.tick(60)
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False   
    screen_group.draw(win)

    ScoreDisplay()
    checkFlags()

    car_group.draw(win)
    cat_group.draw(win)
    flag_group.draw(win)

    car_group.update()
    cat_group.update()
    flag_group.update()

    screen_group.update()

    p.display.update()