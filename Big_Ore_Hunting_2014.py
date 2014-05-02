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
CLOCK = pygame.time.Clock()


class WorldContainer(pygame.Surface):
    def __init__(self, width, height, pos=(0, 0)):
        pygame.Surface.__init__(self, (width, height))
        self.width = width
        self.height = height
        self.pos = pos
        self.rect = pygame.Rect(self.pos, (self.width, self.height))

        self.objects = {}


# Everything that can be mined in the underworld
class GroundChunk(pygame.sprite.Sprite):
    def __init__(self, pos, color=(0, 0, 0)):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.color = color
        self.image = pygame.Surface((50, 50))
        self.image.fill(self.color)

        self.rect = pygame.Rect(self.pos, self.image.get_size())

    def update(self, player, keys, amount=1):

        if keys[pygame.K_w]:
            self.rect.y += amount
        elif keys[pygame.K_a]:
            self.rect.x += amount
        elif keys[pygame.K_s]:
            self.rect.y -= amount
        elif keys[pygame.K_d]:
            self.rect.x -= amount
        if self.rect.colliderect(player.rect):
            self.kill()


# Player class
class Digger():
    def __init__(self):
        self.image = pygame.Surface((50, 50))
        self.image.fill(WHITE)
        self.global_x = 0
        self.global_y = 0
        self.rect = pygame.Rect((640-(self.image.get_width()/2),
                                 400-(self.image.get_height()/2)), self.image.get_size())

        self.inventory = []
        self.speed = 1
        self.health = 100
        self.max_health = 100
        
        self.energy = 1000
        self.max_energy = 1000
        
        self.heat = 0
        self.max_heat = 100

    def update(self, keys):
        pass


# Used to create bases at the surface
class Outpost():
    def __init__(self, name, pos):
        self.name = name
        self.pos = pos


# Creates spooky monsters
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
        self.ground_chunks_rects = [x.rect for x in self.ground_chunks]

        self.bg_color = (135, 206, 250)
        self.player = Digger()
        self.font = pygame.font.Font(None, 30)
        self.playing = True

        self.gen_ground_chunks()
        self.game_loop()

    # Main game loop
    def game_loop(self):
        pygame.key.set_repeat(10, 10)
        is_space = False
        while self.playing:
            self.ground_chunks_rects = [x.rect for x in self.ground_chunks]

            # Main event loop
            # Turn on the drill
            if pygame.event.get(pygame.QUIT):
                self.playing = False
                pygame.quit()
                break
            pygame.event.pump()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_SPACE]:
                is_space = True
            else:
                is_space = False

            if keys[pygame.K_p]:
                self.player.speed += 1
            if keys[pygame.K_o] and self.player.speed > 1:
                self.player.speed -= 1
            if keys[pygame.K_l]:
                self.player.speed = 1

            if any(keys):
                # Create a copy of the rectangle for collision testing
                temp_rect = self.player.rect.copy()
                move = True
                # Move the rectangle and check for collisions
                if keys[pygame.K_w]:
                    temp_rect.move_ip(0, -self.player.speed)
                elif keys[pygame.K_a]:
                    temp_rect.move_ip(-self.player.speed, 0)
                elif keys[pygame.K_s]:
                    temp_rect.move_ip(0, self.player.speed)
                elif keys[pygame.K_d]:
                    temp_rect.move_ip(self.player.speed, 0)
                else:
                    move = False

                if move:
                    # If the drill is activated and there's a block in the way
                    if temp_rect.collidelist(self.ground_chunks_rects) != -1 and is_space:
                        self.ground_chunks.update(self.player, keys, self.player.speed)

                    # If there is nothing in the way
                    elif temp_rect.collidelist(self.ground_chunks_rects) == -1:
                        self.ground_chunks.update(self.player, keys, self.player.speed)

                    # If the drill is not activated, and there is a block in the way
                    else:
                        self.ground_chunks.update(self.player, keys, self.max_move(keys))

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
            CLOCK.tick(60)

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

    # Calculates the maximum distance the player can move without colliding with something
    def max_move(self, keys):
        for value in reversed(range(self.player.speed)):
            temp_rect = self.player.rect.copy()

            if keys[pygame.K_w]:
                temp_rect.move_ip(0, -value)
            elif keys[pygame.K_a]:
                temp_rect.move_ip(-value, 0)
            elif keys[pygame.K_s]:
                temp_rect.move_ip(0, value)
            elif keys[pygame.K_d]:
                temp_rect.move_ip(value, 0)

            if temp_rect.collidelist(self.ground_chunks_rects) == -1:
                return value
        return 1

    @staticmethod
    def clip_amount(axis_pos):
        remainder = axis_pos % 50

        if remainder == 0:
            return 0
        elif remainder not in range(16, 34):
            return (round(float(axis_pos)/50)*50) - axis_pos
        else:
            return 0

if __name__ == "__main__":
    Game()
