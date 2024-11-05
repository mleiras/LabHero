import pygame
from settings import *
from functions import *
from timers import Timer
import time
from utils import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, desk_menu, books, ecoli, inventory2, talk_1, talk_2, talk_3, dialogues):
        super().__init__(group)

        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        #general setup
        self.image = self.animations[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['main']

        # movement 
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

        # collision
        self.hitbox = self.rect.copy().inflate((-126,-70)) # tuplo w,h
        self.collision_sprites = collision_sprites

        # Área de interação independente da hitbox
        self.interaction_area = pygame.Rect(25,25, 50, 50)  # Tamanho pequeno para detectar objetos próximos

        # timers
        self.timers = {
            'tool_use': Timer(350, self.use_tool)
        }

        self.item_inventory = DEFAULT_INVENTORY[0]

        self.player_name, self.results, self.missions_activated, self.missions_completed = inventory2

        # interaction
        self.toggle_shop = toggle_shop
        self.talk_1 = talk_1
        self.talk_2 = talk_2
        self.talk_3 = talk_3
        self.desk_menu = desk_menu
        self.books = books
        self.ecoli = ecoli
        self.dialogues = dialogues
        self.character = None
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.soil_layer = soil_layer

        	
        # music

        self.music_bg = pygame.mixer.Sound(MUSIC_NAME)
        self.music_bg.set_volume(0.07)
        # self.music_bg.set_volume(0)
        self.music_bg.play(loops = -1)

    def use_tool(self):
        for tree in self.tree_sprites.sprites():
            if tree.rect.collidepoint(self.target_pos):
                tree.damage()
       

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]] # status[0] (direção do jogador) para identificar o a posição da ferramenta no dict

    
        
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': []}
        
        for animation in self.animations.keys():
            path_1 = get_resource_path('graphics/character/')
            full_path = path_1 + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def update_interaction_area(self):
        # Posiciona a área de interação ligeiramente à frente do jogador com base na direção
        if self.status.startswith('up'):
            self.interaction_area.midbottom = self.hitbox.midtop
        elif self.status.startswith('down'):
            self.interaction_area.midtop = self.hitbox.midbottom
        elif self.status.startswith('left'):
            self.interaction_area.midright = self.hitbox.midleft
        elif self.status.startswith('right'):
            self.interaction_area.midleft = self.hitbox.midright

    def input(self):

        self.update_interaction_area()

        keys = pygame.key.get_pressed()

        if not self.timers['tool_use'].active:
            
            # directions
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'

            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'

            elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            
            if keys[pygame.K_m]:
                self.toggle_shop()

            # MENUS (ATALHOS PARA TESTES)

            # if keys[pygame.K_k]:
            #     self.desk_menu()
            
            # if keys[pygame.K_b]:
            #     self.books()

            # if keys[pygame.K_t]:
            #     self.talk_2()


            # interaction
            if keys[pygame.K_RETURN] or keys[pygame.K_KP_ENTER]:
                # timer for tool use
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

                # collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False) # spritecollide(sprite, group, dokill)
                # if collided_interaction_sprite:

                # Deteta colisão apenas com objetos dentro da área de interação
                for sprite in self.interaction:
                    if self.interaction_area.colliderect(sprite.hitbox):

                        if sprite.name == 'Mission01':
                            self.talk_1()

                        elif sprite.name == 'Mission02':
                            self.talk_2()

                        elif sprite.name == 'Mission03':
                            self.talk_3()
                        
                        elif sprite.name == 'Desk':
                            # print(time.time())
                            animation_text_save('... please wait ...', time = 100) #, time=500)
                            self.desk_menu()

                        elif sprite.name == 'Books':
                            self.books()
                        
                        elif sprite.name == 'Ecoli':
                            self.ecoli()

                        elif sprite.name == 'Sequeira' or 'Pacheco' or 'Marta' or 'Nuno' or 'Fernanda' or 'Emanuel' or 'Alexandre' or 'Capela':
                            self.character = sprite.name
                            self.dialogues() # add variable with name character to change message and id
                            
            
    def get_status(self):
        # if player not moving add idle
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'

        # tool use
        if self.timers['tool_use'].active:
            self.status = self.status.split('_')[0] # + '_' + self.selected_tool

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
        
    def move(self, dt):
        # normalize vector (diagonal speed same as horizontal/vertical speed)
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize() 
        
        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        self.collision('horizontal')

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        self.collision('vertical')

    def collision(self, direction):
        for sprite in self.collision_sprites.sprites():
            if hasattr(sprite, 'hitbox'):
                if sprite.hitbox.colliderect(self.hitbox):
                    if direction == 'horizontal':
                        if self.direction.x > 0: #moving right
                            self.hitbox.right = sprite.hitbox.left
                        if self.direction.x < 0: #moving left
                            self.hitbox.left = sprite.hitbox.right
                        self.rect.centerx = self.hitbox.centerx
                        self.pos.x = self.hitbox.centerx

                    if direction == 'vertical':
                        if self.direction.y > 0: #moving down
                            self.hitbox.bottom = sprite.hitbox.top
                        if self.direction.y < 0: #moving up
                            self.hitbox.top = sprite.hitbox.bottom
                        self.rect.centery = self.hitbox.centery
                        self.pos.y = self.hitbox.centery

    def update(self, dt):
        self.input()
        self.get_status()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)

