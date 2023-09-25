import pygame
from settings import *
from support import *
from functions import *
from timers import Timer
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group, collision_sprites, tree_sprites, interaction, soil_layer, toggle_shop, desk_menu, books, inventory2):
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

        # timers
        self.timers = {
            'tool_use': Timer(350, self.use_tool)
        }
        #     'tool_switch': Timer(200),
        #     'seed_use': Timer(350, self.use_seed),
        #     'seed_switch': Timer(200)
        # }

        # tools
        # self.tools = ['axe', 'hoe', 'water']
        # self.tool_index = 0
        # self.selected_tool = self.tools[self.tool_index]

        # seeds
        # self.seeds = ['corn', 'tomato']
        # self.seed_index = 0
        # self.selected_seed = self.seeds[self.seed_index]

        # inventory
        # self.item_inventory, self.seed_inventory, self.money = inventory[:3]

        self.item_inventory = DEFAULT_INVENTORY[0]

        self.results, self.missions_activated, self.missions_completed = inventory2[:3]

        # interaction
        self.toggle_shop = toggle_shop
        self.desk_menu = desk_menu
        self.books = books
        self.tree_sprites = tree_sprites
        self.interaction = interaction
        self.soil_layer = soil_layer

        # sound
        # self.watering = pygame.mixer.Sound('../audio/water.mp3')
        # self.watering.set_volume(0.2)

    def use_tool(self):
        for tree in self.tree_sprites.sprites():
            if tree.rect.collidepoint(self.target_pos):
                tree.damage()
        # if self.selected_tool == 'hoe':
        #     self.soil_layer.get_hit(self.target_pos)
        # if self.selected_tool == 'water':
        #     self.soil_layer.water(self.target_pos)
        #     self.watering.play()

    def get_target_pos(self):
        self.target_pos = self.rect.center + PLAYER_TOOL_OFFSET[self.status.split('_')[0]] # status[0] (direção do jogador) para identificar o a posição da ferramenta no dict

    # def use_seed(self):
    #     if self.seed_inventory[self.selected_seed] > 0:
    #         self.soil_layer.plant_seed(self.target_pos, self.selected_seed)
    #         self.seed_inventory[self.selected_seed] -= 1
        
    def import_assets(self):
        self.animations = {'up': [], 'down': [], 'left': [], 'right': [],
                           'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
                           'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
                           'right_axe': [], 'left_axe': [], 'up_axe': [], 'down_axe': [],
                           'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []}
        
        for animation in self.animations.keys():
            full_path = '../graphics/character/' + animation
            self.animations[animation] = import_folder(full_path)
    
    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animations[self.status]):
            self.frame_index = 0
        self.image = self.animations[self.status][int(self.frame_index)]

    def input(self):

        keys = pygame.key.get_pressed()

        if not self.timers['tool_use'].active:
            
            # directions
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'

            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
            
            # MENU test
            if keys[pygame.K_m]:
                self.toggle_shop()

            if keys[pygame.K_k]:
                self.desk_menu()
            
            if keys[pygame.K_b]:
                self.books()


            # tools use
            if keys[pygame.K_SPACE]:
                # timer for tool use
                self.timers['tool_use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0
            
            #change tool
            # if keys[pygame.K_q] and not self.timers['tool_switch'].active:
            #     self.timers['tool_switch'].activate()
            #     self.tool_index += 1
            #     if self.tool_index >= len(self.tools): self.tool_index = 0
            #     self.selected_tool = self.tools[self.tool_index]

            # seed use
            # if keys[pygame.K_LCTRL]:
            #     # timer for tool use
            #     self.timers['seed_use'].activate()
            #     self.direction = pygame.math.Vector2()
            #     self.frame_index = 0
            #     # print('use seed')

            #change seed
            # if keys[pygame.K_e] and not self.timers['seed_switch'].active:
            #     self.timers['seed_switch'].activate()
            #     self.seed_index += 1
            #     if self.seed_index >= len(self.seeds): self.seed_index = 0
            #     self.selected_seed = self.seeds[self.seed_index]
            #     # print(self.selected_seed)

            # interaction
            if keys[pygame.K_RETURN]:
                collided_interaction_sprite = pygame.sprite.spritecollide(self, self.interaction, False) # spritecollide(sprite, group, dokill)
                if collided_interaction_sprite:
                    if collided_interaction_sprite[0].name == 'Trader':
                        self.toggle_shop()

                    elif collided_interaction_sprite[0].name == 'Desk':
                        # print(time.time())
                        animation_text_save('... please wait ...', time = 100) #, time=500)
                        self.desk_menu()

                    elif collided_interaction_sprite[0].name == 'Books':
                        self.books()
                        
            
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

