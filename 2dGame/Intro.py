import pygame

from sys import exit

from random import randint, choice

# Player as sprite Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # create the player surface and rectangle
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        #import sound
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.1)

    # player input
    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 and score != 0:
            self.gravity = -20
            self.jump_sound.play()
    def apply_gravity(self):
        # let the player jump
        if self.gravity < 22:
            self.gravity += 1
            self.rect.bottom += self.gravity
        # so the player does not fall through the ground
        if self.rect.bottom > 300:
            self.rect.bottom = 300
    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        if type == "fly":
            fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
            fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
            self.frames = [fly_frame_1, fly_frame_2]
            y_position = 210
        else:
            snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_frame_1, snail_frame_2]
            y_position = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_position))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index > len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

#score function
def display_score():
    current_time = round((pygame.time.get_ticks()- stop_time) / 1000)
    score_surface = test_font.render(f'Score:{current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

# obstacle function
def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= 4
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surf, obstacle_rect)
            else:
                screen.blit(fly_surf , obstacle_rect)
            # list comprehension of all obstacles still on the screen
            obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
    return obstacle_list

# collision function
def collisions(player_rect, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player_rect.colliderect(obstacle_rect): return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        # delete enemys
        obstacle_group.empty()
        return False
    else: return True


# player animation function
def player_animation():
    global player_surf, player_index
    if player_rect.bottom < 300:
        player_surf = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0
        player_surf = player_walk[int(player_index)]

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

# create an enemy (and remove the alpha values)
snail_frame_1= pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frames_index = 0
snail_surf = snail_frames[snail_frames_index]

fly_frame_1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frames_index = 0
fly_surf = fly_frames[fly_frames_index]

# obstacles
obstacle_rect_list = []

#create the player surface and rectangle
player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player_surf = player_walk[player_index]
player_rect = player_surf.get_rect(midbottom = (80, 300))

# end game player
player_stand = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

# end game surface
name_surf = test_font.render("Pixel Runner", False, (111, 196, 169)).convert_alpha()
name_rect = name_surf.get_rect(center = (400, 80))
# restart surface
res_surf = test_font.render("Press space to run", False,  (111, 196, 169)).convert_alpha()
res_rect = res_surf.get_rect(center = (400, 320))
# gravity
player_gravity = 0
#time
stop_time = 0
# score
score = 0
# Timer User event
obstacle_timer = pygame.USEREVENT + 1
# Trigger event
pygame.time.set_timer(obstacle_timer, 1500)

# enemy timer
snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 500)
# so the display wont close
while True:
    # loop through the player input
    for event in pygame.event.get():
        # if close button is clicked
        if event.type == pygame.QUIT:
            pygame.quit()
            # close code
            exit()
        if game_active:
            # make the player jump
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rect.bottom == 300:
                    player_gravity = -22
            if event.type == pygame.MOUSEBUTTONDOWN and player_rect.bottom == 300:
                if player_rect.collidepoint(event.pos):
                    player_gravity = -22
        # restart the game
        if not game_active:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))

                # list of enemys
                #if randint(0, 2):
                    #obstacle_rect_list.append(snail_surf.get_rect(midbottom = (randint(900, 1100), 300)))
                #else:
                    #obstacle_rect_list.append(fly_surf.get_rect(midbottom=(randint(900, 1100), 210)))
            # create obstacle surf 0 or 1
            if event.type == snail_animation_timer:
                if snail_frames_index == 0: snail_frames_index = 1
                else: snail_frames_index = 0
                snail_surf = snail_frames[snail_frames_index]
            elif event.type == fly_animation_timer:
                if fly_frames_index == 0: fly_frames_index = 1
                else: fly_frames_index = 0
                fly_surf = fly_frames[fly_frames_index]

    if game_active:
        # play sound
        # music.play(loops=-1)
        # put surfaces on the display
        screen.blit(sky_surface, (0, 0))
        screen.blit(ground_surface, (0, 300))
        # show score
        score = display_score()

        player.draw(screen)
        # update Sprites = call methods
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        #collision
        game_active = collision_sprite()

    else: # Start and end screen
        # set the stop timer
        stop_time = pygame.time.get_ticks()
        # stop the music
        music.stop()
        screen.fill((94, 129, 162))
        screen.blit(name_surf,name_rect)
        # empty the obstacle list, player position and player gravity
        obstacle_rect_list.clear()
        player_rect.midbottom = (80, 300)
        player_gravity = 0
        # Display score
        score_message = test_font.render(f'Score: {score}', False, (111, 196, 169))
        score_rect = score_message.get_rect(center = (400, 340))
        screen.blit(player_stand, player_stand_rect)
        # Only display score if score != 0
        if score == 0:
            screen.blit(res_surf, res_rect)
        else:
            screen.blit(score_message, score_rect)

    # update the display
    pygame.display.update()
    # how many loop runs per second
    clock.tick(60)
