#######################
# Big Ore Hunter 2014 #
# Brandon Sturgeon    #
#######################

import pygame
pygame.init()


class Digger():
    def __init__(self):
        self.image = pygame.Surface((100, 100))
        self.image.fill((255, 0, 0))
        self.global_x = 0
        self.global_y = 0

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
        self.above_world = pygame.Surface((6400, 400))
        self.above_world_rect = pygame.Rect((-3200, 0), self.above_world.get_size())
        self.below_world = pygame.Surface((6400, 2400))
        self.below_world_rect = pygame.Rect((-3200, 400), self.below_world.get_size())
        self.world_rects = (self.above_world_rect, self.below_world_rect)
        
        self.bg_color = (135, 206, 250)
        self.player = Digger()
        self.font = pygame.font.Font(None, 30)
        
        self.game_loop()

    def game_loop(self):
        while True:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        self.player.global_y += 1
                        for world in self.world_rects:
                            world.y -= 5
                    if event.key == pygame.K_w:
                        self.player.global_y -= 1
                        for world in self.world_rects:
                            world.y += 5
                    if event.key == pygame.K_a:
                        self.player.global_x -= 1
                        for world in self.world_rects:
                            world.x += 5
                    if event.key == pygame.K_d:
                        self.player.global_x += 1
                        for world in self.world_rects:
                            world.x -= 5

            self.above_world.fill(self.bg_color)
            self.below_world.fill((0, 0, 0))
            
            self.game_window.blit(self.above_world, (self.above_world_rect.x, self.above_world_rect.y))
            self.game_window.blit(self.below_world, (self.below_world_rect.x, self.below_world_rect.y))
            self.game_window.blit(self.player.image, (640-(self.player.image.get_width()/2),
                                                      400-(self.player.image.get_height()/2)))
            self.game_window.blit(self.font.render("("+str(self.player.global_x)+"," +
                                                   str(self.player.global_y)+")", 1, (0, 255, 0)), (400, 10))
            pygame.display.flip()


if __name__ == "__main__":
    Game()
