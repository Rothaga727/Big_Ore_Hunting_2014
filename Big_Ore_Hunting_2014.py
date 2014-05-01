#######################
# Big Ore Hunter 2014 #
# Brandon Sturgeon    #
#######################

import random
import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
class WorldContainer(pygame.Surface):
    def __init__(self, width, height, pos=(0, 0)):
        pygame.Surface.__init__(self, (width, height))
        self.width = width
        self.height = height
        self.pos = pos
        self.rect = pygame.Rect(self.pos, (self.width, self.height))

        self.objects = {}


class GroundChunk(pygame.sprite.Sprite):
    def __init__(self, pos, color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.color = color
        self.image = pygame.Surface((50, 50))
        self.image.fill(self.color)

        self.rect = pygame.Rect(self.pos, self.image.get_size())

    def update(self, key, player):
        if key == pygame.K_w:
            self.rect.y += 50
        if key == pygame.K_a:
            self.rect.x += 50
        if key == pygame.K_s:
            self.rect.y -= 50
        if key == pygame.K_d:
            self.rect.x -= 50

        if self.rect.colliderect(player.rect):
            print "COLLIDING"
            self.kill()


class Digger():
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 0, 0))
        self.global_x = 0
        self.global_y = 0
        self.rect = pygame.Rect((640-(self.image.get_width()/2),
                                 400-(self.image.get_height()/2)), self.image.get_size())

        self.inventory = []
        
        self.health = 100
        self.max_health = 100
        
        self.energy = 1000
        self.max_energy = 1000
        
        self.heat = 0
        self.max_heat = 100

    def update(self, keys):
        pass


class Outpost():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos


class Monster():
    def __init__(self):
        pass


class Game():
    def __init__(self):
        self.game_window = pygame.display.set_mode((1280, 800))
        self.above_world = WorldContainer(width=6400, height=400, pos=(-3200, 0))
        self.below_world = WorldContainer(width=6400, height=2400, pos=(-3200, 400))
        self.world_rects = (self.above_world.rect, self.below_world.rect)
        self.ground_chunks = pygame.sprite.Group()

        self.bg_color = (135, 206, 250)
        self.player = Digger()
        self.font = pygame.font.Font(None, 30)
        self.playing = True

        self.gen_ground_chunks()
        self.game_loop()

    def game_loop(self):
        pygame.key.set_repeat(10, 10)
        while self.playing:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.playing = False
                    break

                if event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_s:
                        if self.player.global_y*5 < 2350:
                            self.player.global_y += 1
                            self.ground_chunks.update(event.key, self.player)
                            for world in self.world_rects:
                                world.y -= 50
                    elif event.key == pygame.K_w:
                        if self.player.global_y*5 > -50:
                            self.player.global_y -= 1
                            self.ground_chunks.update(event.key, self.player)
                            for world in self.world_rects:
                                world.y += 50
                    elif event.key == pygame.K_a:
                        if self.player.global_x*5 > -3200:
                            self.player.global_x -= 1
                            self.ground_chunks.update(event.key, self.player)
                            for world in self.world_rects:
                                world.x += 50
                    elif event.key == pygame.K_d:
                        if self.player.global_x*5 < 3200:
                            self.player.global_x += 1
                            self.ground_chunks.update(event.key, self.player)
                            for world in self.world_rects:
                                world.x -= 50

            self.game_window.fill(WHITE)
            self.above_world.fill(self.bg_color)
            self.below_world.fill(BLACK)
            
            self.game_window.blit(self.above_world, (self.above_world.rect.x, self.above_world.rect.y))
            self.game_window.blit(self.below_world, (self.below_world.rect.x, self.below_world.rect.y))
            self.ground_chunks.draw(self.game_window)
            self.game_window.blit(self.player.image, (640-(self.player.image.get_width()/2),
                                                      400-(self.player.image.get_height()/2)))
            self.game_window.blit(self.font.render("("+str(self.player.global_x)+"," +
                                                   str(self.player.global_y)+")", 1, (0, 255, 0)), (400, 10))
            pygame.display.flip()

        pygame.quit()

    def gen_ground_chunks(self):

        print "Generating Chunks"
        y_counter = 0
        for y in range(int(2400/50)):
            x_counter = -3200
            y_counter += 50
            for x in range(int(6400/50)):
                rand_color = random.choice((RED, GREEN, BLUE))
                self.ground_chunks.add(GroundChunk(color=rand_color, pos=(x_counter+15, y_counter+25)))
                x_counter += 50



if __name__ == "__main__":
    Game()
