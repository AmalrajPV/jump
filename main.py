import os
import time

import pygame
from pygame import mixer

#   game variables
height, width = 600, 900
blue = (135, 206, 250)
black = (0, 0, 0)
x1, x2 = 0, 900
increment = 0
fps = 60
index = 0
speed = 5
count = 0
player_y = 325
sun_x = 800
color = blue
player_size = (60, 140)
jump = False
vel = 20
obs1_width = 50
obst1_height = 50
obs2_width = 90
obst2_height = 90
obst1_y = 410
obst1_x = 900
counter = 0

#   images
man = [pygame.transform.scale(pygame.image.load(os.path.join('assets', 'guy1.png')), player_size),
       pygame.transform.scale(pygame.image.load(os.path.join('assets', 'guy2.png')), player_size),
       pygame.transform.scale(pygame.image.load(os.path.join('assets', 'guy3.png')), player_size),
       pygame.transform.scale(pygame.image.load(os.path.join('assets', 'guy4.png')), player_size)]

obstacle1 = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'obst2.png')), (obst1_height, obs1_width))
bg1 = pygame.image.load(os.path.join('assets', 'background1.png'))
bg2 = pygame.image.load(os.path.join('assets', 'background2.png'))
sun = pygame.image.load(os.path.join('assets', 'sun.png'))

pygame.init()
window = pygame.display.set_mode((width, height))
mixer.init()
jump_sound = pygame.mixer.Sound(os.path.join('assets', 'img_jump.wav'))
running = True


def fill(x_1, x_2):
    window.fill(blue)
    window.blit(sun, (sun_x, 50))
    window.blit(bg1, (x_1, 0))
    window.blit(bg2, (x_2, 0))
    # pygame.draw.rect(window, (255, 255, 255), player_rect)


def player(y):
    global count
    if count >= 60:
        count = 0
    window.blit(man[count // 15], (100, y))


def obst1(x):
    window.blit(obstacle1, (x, obst1_y))


def p_jump(rect):
    global jump, vel
    key = pygame.key.get_pressed()
    if jump is False and key[pygame.K_SPACE]:
        jump = True
        mixer.Sound.play(jump_sound)

    # jump physics
    if jump is True:
        rect.y -= vel
        vel -= 1
        if vel < -20:
            jump = False
            vel = 20


#   main game loop
def main():
    global running, x1, x2, index, player_y, count, sun_x, color, obst1_height, \
        obst1_y, obst1_x, speed, increment, counter
    fail = pygame.mixer.Sound(os.path.join('assets', 'fail.wav'))

    point = 0

    player_rect = pygame.Rect(100, player_y, player_size[0]-10, player_size[1])
    obst_rect = pygame.Rect(900, obst1_y, obs1_width - 2, obst1_height - 2)

    font = pygame.font.Font('freesansbold.ttf', 30)

    clock = pygame.time.Clock()

    while running:
        clock.tick(fps)
        # counter += 1
        # if counter == 60:
        #     seconds += 1
        #     counter = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        obst_rect.x -= speed
        if obst_rect.x < -70:
            obst_rect.x = 900

        if obst_rect.x == player_rect.x-50:
            point += 1

        text = font.render(f'points : {point}', True, black)
        txt = text.get_rect()
        txt.center = (100, 50)

        x1 -= speed
        x2 -= speed
        if x1 <= -900:
            x1 = 900
        if x2 <= -900:
            x2 = 900
        fill(x1, x2)
        window.blit(text, txt)

        p_jump(player_rect)
        obst1(obst_rect.x)

        if player_rect.colliderect(obst_rect):
            mixer.Sound.play(fail)
            time.sleep(1)
            running = False

        count += 1
        player(player_rect.y)
        index += 1
        if index == 4:
            index = 0

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
