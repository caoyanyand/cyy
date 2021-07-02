# plane07.py 检测我方飞机是否被撞 重生时无敌状态
import pygame
import sys
import traceback
import myplane
import enemy
import bullet
import supply

from pygame.locals import *
from random import *


def add_small_enemies(group1, group2, num):
    for i in range(num):
        e1 = enemy.SmallEnemy(bg_size)
        group1.add(e1)
        group2.add(e1)


def draw_score_bombs_lifes():
    # 绘制全屏炸弹数量
    bomb_text = bomb_font.render("× %d" % bomb_num, True, WHITE)
    text_rect = bomb_text.get_rect()
    screen.blit(bomb_image, (10, height - 10 - bomb_rect.height))
    screen.blit(bomb_text, (20 + bomb_rect.width, height - 5 - text_rect.height))

    # 绘制剩余生命数量
    if life_num:
        for i in range(life_num):
            screen.blit(life_image, \
                        (width - 10 - (i + 1) * life_rect.width, \
                         height - 10 - life_rect.height))

    # 绘制得分
    score_text = score_font.render("Score : %s" % str(score), True, WHITE)
    screen.blit(score_text, (10, 5))


def draw_me():
    global me_destroy_index, life_num
    if me.active:
        if switch_image:
            screen.blit(me.image1, me.rect)
        else:
            screen.blit(me.image2, me.rect)
    else:
        # 毁灭
        if not (delay % 3):
            if me_destroy_index == 0:
                me_down_sound.play()
            screen.blit(me.destroy_images[me_destroy_index], me.rect)
            me_destroy_index = (me_destroy_index + 1) % 4
            if me_destroy_index == 0:
                life_num -= 1
                me.reset()
                pygame.time.set_timer(INVINCIBLE_TIME, 3 * 1000)


def draw_small():
    global e1_destroy_index, score
    for each in small_enemies:
        if each.active:
            each.move()
            screen.blit(each.image, each.rect)
        # 毁灭
        elif not (delay % 3):
            if e1_destroy_index == 0:
                enemy1_down_sound.play()
            screen.blit(each.destroy_images[e1_destroy_index], each.rect)
            e1_destroy_index = (e1_destroy_index + 1) % 4
            if e1_destroy_index == 0:
                score += 1000
                each.reset()


pygame.init()
pygame.mixer.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("2021雷霆出击 V1.0 明德学院信息系计科18 碧空战将")

background = pygame.image.load("images/background.png").convert()
bg1_top = 0
bg2_top = -700

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 载入游戏音乐
pygame.mixer.music.load("sound/game_music.ogg")
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(-1)
bullet_sound = pygame.mixer.Sound("sound/bullet.wav")
bullet_sound.set_volume(0.2)
bomb_sound = pygame.mixer.Sound("sound/use_bomb.wav")
bomb_sound.set_volume(0.2)
supply_sound = pygame.mixer.Sound("sound/supply.wav")
supply_sound.set_volume(0.2)
get_bomb_sound = pygame.mixer.Sound("sound/get_bomb.wav")
get_bomb_sound.set_volume(0.2)
get_bullet_sound = pygame.mixer.Sound("sound/get_bullet.wav")
get_bullet_sound.set_volume(0.2)
upgrade_sound = pygame.mixer.Sound("sound/upgrade.wav")
upgrade_sound.set_volume(0.2)
enemy3_fly_sound = pygame.mixer.Sound("sound/enemy3_flying.wav")
enemy3_fly_sound.set_volume(0.2)
enemy1_down_sound = pygame.mixer.Sound("sound/enemy1_down.wav")
enemy1_down_sound.set_volume(0.2)
enemy2_down_sound = pygame.mixer.Sound("sound/enemy2_down.wav")
enemy2_down_sound.set_volume(0.2)
enemy3_down_sound = pygame.mixer.Sound("sound/enemy3_down.wav")
enemy3_down_sound.set_volume(0.5)
me_down_sound = pygame.mixer.Sound("sound/me_down.wav")
me_down_sound.set_volume(0.2)

# 统计得分
score = 0
score_font = pygame.font.Font("font/font.ttf", 36)

# 标志是否暂停游戏
paused = False

# 设置难度级别
level = 1

# 全屏炸弹
bomb_image = pygame.image.load("images/bomb.png").convert_alpha()
bomb_rect = bomb_image.get_rect()
bomb_font = pygame.font.Font("font/font.ttf", 48)
bomb_num = 3

# 生命数量
life_image = pygame.image.load("images/life.png").convert_alpha()
life_rect = life_image.get_rect()
life_num = 3

## 生成我方飞机
me = myplane.MyPlane(bg_size)

enemies = pygame.sprite.Group()

# 生成敌方小型飞机
small_enemies = pygame.sprite.Group()
add_small_enemies(small_enemies, enemies, 15)

# 生成普通子弹
bullet1 = []
bullet1_index = 0
BULLET1_NUM = 4
for i in range(BULLET1_NUM):
    bullet1.append(bullet.Bullet1(me.rect.midtop))

# 生成超级子弹
bullet2 = []
bullet2_index = 0
BULLET2_NUM = 12
for i in range(BULLET2_NUM // 3):
    bullet2.append(bullet.Bullet2((me.rect.centerx - 33, me.rect.centery)))
    bullet2.append(bullet.Bullet2((me.rect.centerx + 30, me.rect.centery)))
    bullet2.append(bullet.Bullet2((me.rect.centerx - 1, me.rect.centery)))

# 用于延迟
delay = 100

# 标志是否使用超级子弹
is_double_bullet = False
is_Triple_Tap = False

# 解除我方无敌状态定时器
INVINCIBLE_TIME = USEREVENT + 2

# 用于切换图片
switch_image = True

clock = pygame.time.Clock()

# 中弹图片索引
e1_destroy_index = 0
e2_destroy_index = 0
e3_destroy_index = 0
me_destroy_index = 0


def main():
    global bullet1_index, bullet2_index, delay, bg1_top, bg2_top

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == INVINCIBLE_TIME:
                me.invincible = False
                pygame.time.set_timer(INVINCIBLE_TIME, 0)

        bg1_top = (bg1_top + 1) if bg1_top <= 700 else -700
        bg2_top = (bg2_top + 1) if bg2_top <= 700 else -700
        screen.blit(background, (0, bg1_top))
        screen.blit(background, (0, bg2_top))

        if life_num and not paused:
            # 检测用户的键盘操作
            key_pressed = pygame.key.get_pressed()

            if key_pressed[K_w] or key_pressed[K_UP]:
                me.moveUp()
            if key_pressed[K_s] or key_pressed[K_DOWN]:
                me.moveDown()
            if key_pressed[K_a] or key_pressed[K_LEFT]:
                me.moveLeft()
            if key_pressed[K_d] or key_pressed[K_RIGHT]:
                me.moveRight()

            # 发射子弹
            if not (delay % 10):
                bullet_sound.play()
                if is_double_bullet:
                    bullets = bullet2
                    bullets[bullet2_index].reset((me.rect.centerx - 33, me.rect.centery))
                    bullets[bullet2_index + 1].reset((me.rect.centerx + 30, me.rect.centery))
                    if is_Triple_Tap:
                        bullets[bullet2_index + 2].reset((me.rect.centerx - 1, me.rect.centery))
                    bullet2_index = (bullet2_index + 3) % BULLET2_NUM
                else:
                    bullets = bullet1
                    bullets[bullet1_index].reset(me.rect.midtop)
                    bullet1_index = (bullet1_index + 1) % BULLET1_NUM

            # 检测子弹是否击中敌机
            for b in bullets:
                if b.active:
                    b.move()
                    screen.blit(b.image, b.rect)
                    enemy_hit = pygame.sprite.spritecollide(b, enemies, False, pygame.sprite.collide_mask)
                    if enemy_hit:
                        b.active = False
                        for e in enemy_hit:
                            e.active = False
            draw_small()

            # 检测我方飞机是否被撞
            enemies_down = pygame.sprite.spritecollide(me, enemies, False, pygame.sprite.collide_mask)
            if enemies_down and not me.invincible:
                me.active = False
                for e in enemies_down:
                    e.active = False
            draw_me()

        draw_score_bombs_lifes()

        delay = (delay - 1) if delay else 100

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
