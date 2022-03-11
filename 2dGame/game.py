import pygame
from sys import exit
from random import choice

# import Player class
from Player import Player

# import Obstacle class
from Obstacle import Obstacle

# import pause screen
from pause import Pause

# core function
def display_score():
    current_time = round((pygame.time.get_ticks()- stop_time) / 1000)
    score_surface = test_font.render(f'Score:{current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# collision function
def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        # delete enemys
        obstacle_group.empty()
        return False
    else: return True


# Creating a window
pygame.init()
width = 800
height = 400
screen = pygame.display.set_mode((width, height))
game_active = False

# music
music = pygame.mixer.Sound("audio/music.wav")
music.set_volume(0.05)

# title
pygame.display.set_caption("Runner")

# control the frame rate
clock = pygame.time.Clock()

# create text font
test_font = pygame.font.Font("font/Pixeltype.ttf", 50)

# create a surface
sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

# Groups
# Create Player and add him to a single Group
player = pygame.sprite.GroupSingle()
player.add(Player())
obstacle_group = pygame.sprite.Group()

pause = pygame.sprite.GroupSingle()
pause.add(Pause())

# time
stop_time = 0

# read in the highscore
with open("score.txt") as s:
    highscore = s.readline()

# set score as 0
score = 0

# Timer User event
obstacle_timer = pygame.USEREVENT + 1

# Trigger event (spawn enemys)
pygame.time.set_timer(obstacle_timer, 1500)

# so the display wont close
while True:
    # loop through the player input
    for event in pygame.event.get():
        # if close button is clicked
        if event.type == pygame.QUIT:
            pygame.quit()
            # close code
            exit()
        # restart the game
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

    if game_active:
        # play sound
        # music.play(loops=-1)
        # put surfaces on the display
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # show score
        score = display_score()

        # call the Player Sprite and methods
        player.draw(screen)
        player.update(score)

        # call the group (enemys) Sprite and methods
        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collision_sprite()

    # Start and end screen
    else:
        # set the stop timer
        stop_time = pygame.time.get_ticks()

        pause.draw(screen)
        hihgscore = pause.update(music, screen, score, highscore)


    # update the display
    pygame.display.update()

    # how many loop runs per second
    clock.tick(60)

