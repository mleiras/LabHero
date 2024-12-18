import pygame
from settings import *
from random import randint, choice
from timers import Timer
from utils import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups, z = LAYERS['main']):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width*0.5, -self.rect.height*0.75) 

class Interaction(Generic):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size)
        super().__init__(pos, surf, groups)
        self.name = name
        
class Water(Generic):
    def __init__(self, pos, frames, groups):

        # animation setup
        self.frames = frames
        self.frame_index = 0

        # sprite setup
        super().__init__(
            pos = pos,
            surf = self.frames[self.frame_index],
            groups = groups,
            z = LAYERS['water'])
    
    def animate(self, dt):
        self.frame_index += 3 * dt
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        self.image = self.frames[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class WildFlower(Generic):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups)
        self.hitbox = self.rect.copy().inflate(-20,-self.rect.height*0.9)

class Tree(Generic):
    def __init__(self, pos, surf, groups, name, player_add):
        super().__init__(pos, surf, groups)

        
        # apples
        apples_path = get_resource_path('graphics/fruit/apple.png')
        self.apples_surf = pygame.image.load(apples_path)
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

        self.player_add = player_add


    def create_fruit(self):
        for pos in self.apple_pos: # posição relativa à imagem da arvore, não do mapa
            if randint(0,10) < 2:
                x = pos[0] + self.rect.left
                y = pos[1] + self.rect.top
                Generic(
                    pos = (x,y), 
                    surf = self.apples_surf, 
                    groups = [self.apple_sprites, self.groups()[0]],
                    z = LAYERS['fruit']) # como não há acesso direto ao grupo all_sprites, consegue-se aceder a todos os grupos da classe Tree (level.py) e escolhe-se o grupo pela ordem que aparece 

    def damage(self):
        #remove an apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(
                pos = random_apple.rect.topleft,
                surf = random_apple.image,
                groups =  self.groups()[0],
                z = LAYERS['fruit'])
            self.player_add('apple')
            random_apple.kill()


    def update(self, dt):
        pass
       


class Particle(Generic):
    def __init__(self, pos, surf, groups, z, duration = 200):
        super().__init__(pos, surf, groups, z)
        self.duration = duration
        self.start_time = pygame.time.get_ticks()

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0)) # black colour
        self.image = new_surf

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()