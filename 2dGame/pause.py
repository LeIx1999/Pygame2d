import pygame

# score
score = 0

class Pause(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # end game player
        self.image = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
        self.image = pygame.transform.rotozoom(self.image, 0, 2)
        self.rect = self.image.get_rect(center=(400, 200))

    def draw(self, music, screen):
        # paint the screen blue
        screen.fill((94, 129, 162))

        # create text font
        test_font = pygame.font.Font("font/Pixeltype.ttf", 50)
        # end game surface
        name_surf = test_font.render("Pixel Runner", False, (111, 196, 169)).convert_alpha()
        self.name_rect = name_surf.get_rect(center=(400, 80))

        # restart surface
        res_surf = test_font.render("Press space to run", False, (111, 196, 169)).convert_alpha()
        self.res_rect = res_surf.get_rect(center=(400, 320))

        # blit the player_stand
        screen.blit(self.image, self.rect)

        # stop the music
        music.stop()

        screen.blit(name_surf, self.name_rect)

        # empty the player gravity
        player_gravity = 0

        # Display score
        score_message = test_font.render(f'Score: {score}', False, (111, 196, 169))
        score_rect = score_message.get_rect(center=(400, 340))

        # Display highsore
        self.highscore_message = test_font.render(f'Highscore: {score}', False, (111, 196, 169))
        self.highscore_rect = score_message.get_rect(center=(650, 25))
        screen.blit(self.highscore_message, self.highscore_rect)

        # Only display score if score != 0
        if score == 0:
            screen.blit(res_surf, self. res_rect)
        else:
            screen.blit(score_message, score_rect)

    def highscore(self, score, highscore_old):
        if score > int(highscore_old):
            with open("score.txt", mode = "w") as c:
                c.write(str(score))


    def update(self, music, screen, score, highscore_old):
        self.draw(music, screen)
        self.highscore(score, highscore_old)