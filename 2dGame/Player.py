# Class Player
import pygame

# Player as sprite Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # create the player surface and rectangle
        player_walk_1 = pygame.image.load("graphics/player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/player/player_walk_2.png").convert_alpha()

        # list of animation images
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0

        # image for a jump
        self.player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
        self.image = self.player_walk[self.player_index]

        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

        #import sound
        self.jump_sound = pygame.mixer.Sound("audio/jump.mp3")
        self.jump_sound.set_volume(0.1)

    # player input
    def player_input(self, score):
        # jump on space
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300 and score != 0:
            self.gravity = -20
            self.jump_sound.play()

    def update(self, score):
        self.player_input(score)
        self.apply_gravity()
        self.animation_state()

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