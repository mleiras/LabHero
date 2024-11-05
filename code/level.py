import pygame 
from settings import *
from player import Player
from sprites import *
import pytmx
from pytmx.util_pygame import load_pygame # pytmx map loader
from soil import *
# from menu import *
from menu_2 import *
from window import Window
from books import Books
from ecoli import Ecoli
from mission01 import Mission01
from mission02 import Mission02
from mission03 import Mission03
from dialogues import Dialogues
from save_load import save_file
from functions import *
from utils import *

class Level:
	def __init__(self, load_game):

		# get the display surface
		self.display_surface = pygame.display.get_surface()

		# load the game
		self.load_game = load_game

		# sprite groups
		self.all_sprites = CameraGroup()
		self.collision_sprites = pygame.sprite.Group()
		self.tree_sprites = pygame.sprite.Group()
		self.interaction_sprites = pygame.sprite.Group()

		self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
		self.setup()

		# MENUS
		self.menu_active = False
		self.desk_active = False
		self.books_active = False
		self.ecoli_active = False
		self.talk_1_active = False
		self.talk_1 = Mission01(self.toggle_talk_1, self.player)
		self.talk_2_active = False
		self.talk_2 = Mission02(self.toggle_talk_2, self.player)
		self.talk_3_active = False
		self.talk_3 = Mission03(self.toggle_talk_3, self.player)
		self.menu = Menu(self.player, self.toggle_shop)
		self.window = Window(self.desk_menu, self.player)
		self.books = Books(self.read_books)
		self.ecoli = Ecoli(self.see_ecoli)
		self.dialogues = Dialogues(self.toggle_dialogue, self.player)
		self.dialogues_active = False

		# sounds
		success_path = get_resource_path('audio/success.wav')
		self.success = pygame.mixer.Sound(success_path) 
		self.success.set_volume(0.1)

		# music
		# self.music_bg = pygame.mixer.Sound(MUSIC_NAME)
		# self.music_bg.set_volume(0.07)
		# self.music_bg.play(loops = -1)

	def setup(self):
		
		map_path = get_resource_path('data/map_lb.tmx')
		tmx_data = load_pygame(map_path)
		surf_path = get_resource_path('graphics/world/ground_lb.png')

		# house
		for layer in ['HouseFloor', 'HouseFurnitureBottom']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles(): # 'HouseFurnitureBottom' mesmo nome que layers no programa Tiled
				Generic((x* TILE_SIZE, y* TILE_SIZE), surf, self.all_sprites, LAYERS['house bottom'])

		for layer in ['HouseWalls', 'HouseFurnitureMiddle', 'HouseFurnitureTop']:
			for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
				Generic((x* TILE_SIZE, y* TILE_SIZE), surf, self.all_sprites, LAYERS['main'])

		# Fence
		for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
			Generic((x* TILE_SIZE, y* TILE_SIZE), surf, [self.all_sprites, self.collision_sprites], LAYERS['main'])

		# Water
		water_frames_path = get_resource_path('graphics/water')
		water_frames = import_folder(water_frames_path)
		for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
			Water((x* TILE_SIZE, y* TILE_SIZE), water_frames, self.all_sprites)


		# Trees
		for obj in tmx_data.get_layer_by_name('Trees'):
			Tree(
				pos = (obj.x, obj.y),
				surf = obj.image,
				groups = [self.all_sprites, self.collision_sprites, self.tree_sprites],
				name = obj.name,
				player_add = self.player_add)

		# Wildflowers
		for obj in tmx_data.get_layer_by_name('Decoration'):
			WildFlower((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

		# collision tiles 
		for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles(): # no mapa tem tiles definidos como collision (como water, house, etc.)
			Generic((x * TILE_SIZE, y * TILE_SIZE), pygame.Surface((TILE_SIZE, TILE_SIZE)), self.collision_sprites) # apenas neste grupo porque não queremos mostrar estes tiles, apenas colidir

		# Player
		for obj in tmx_data.get_layer_by_name('Player'):
			if obj.name == 'Start':
				self.player = Player(
					pos = (obj.x,obj.y),
					group = self.all_sprites,
					collision_sprites = self.collision_sprites,
					tree_sprites = self.tree_sprites,
					interaction = self.interaction_sprites,
					soil_layer = self.soil_layer,
					toggle_shop = self.toggle_shop,
					desk_menu = self.desk_menu,
					books = self.read_books,
					ecoli = self.see_ecoli,
					# inventory = self.load_game,
					inventory2 = self.load_game,
					talk_1 = self.toggle_talk_1,
					talk_2 = self.toggle_talk_2,
					talk_3 = self.toggle_talk_3,
					dialogues = self.toggle_dialogue
					# music = self.music_bg
					)
			
			if obj.name == 'Mission01':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
			
			if obj.name == 'Mission02':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Mission03':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
			
			if obj.name == 'Desk':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
			
			if obj.name == 'Books':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			if obj.name == 'Ecoli':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)	

			if obj.name == 'Sequeira' or 'Pacheco' or 'Nuno' or 'Fernanda' or 'Emanuel' or 'Alexandre' or 'Capela' or 'Marta' :
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			# if obj.name == 'Oscar':
			# 	Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)

			# if obj.name == 'Vitor':
			# 	Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
				
			if obj.name == 'Coffee':
				Interaction((obj.x, obj.y), (obj.width, obj.height), self.interaction_sprites, obj.name)
			

		Generic(
			pos = (0,0),
			surf = pygame.image.load(surf_path).convert_alpha(),
			groups = self.all_sprites,
			z = LAYERS['ground'])

	def player_add(self, item):
		self.player.item_inventory[item] += 1
		self.success.play()

	def toggle_shop(self):
		self.menu_active = not self.menu_active

	def toggle_talk_1(self):
		self.talk_1_active = not self.talk_1_active

	def toggle_talk_2(self):
		self.talk_2_active = not self.talk_2_active
	
	def toggle_talk_3(self):
		self.talk_3_active = not self.talk_3_active

	def toggle_dialogue(self):
		self.dialogues_active = not self.dialogues_active

	def desk_menu(self):
		self.desk_active = not self.desk_active

	def read_books(self):
		self.books_active = not self.books_active

	def see_ecoli(self):
		self.ecoli_active = not self.ecoli_active

	def plant_collision(self):
		if self.soil_layer.plant_sprites: # se houver plantas
			for plant in self.soil_layer.plant_sprites.sprites():
				if plant.harvestable and plant.rect.colliderect(self.player.hitbox): # se colidir com o player
					self.player_add(plant.plant_type)
					plant.kill()
					Particle(
						pos = plant.rect.topleft,
						surf = plant.image,
						groups = self.all_sprites,
						z = LAYERS['main']
					)
					x = plant.rect.centerx // TILE_SIZE
					y = plant.rect.centery // TILE_SIZE
					self.soil_layer.grid[y][x].remove('P')

	def reset(self):
		#save game
		save_file([self.player.player_name, self.player.results, self.player.missions_activated, self.player.missions_completed])

		# plants
		self.soil_layer.update_plants()

		# trees
		for tree in self.tree_sprites.sprites():
			for apple in tree.apple_sprites.sprites():
				apple.kill()
			tree.create_fruit()


	def run(self,dt): #delta time

		# drawing logic
		self.display_surface.fill('black')
		self.all_sprites.custom_draw(self.player)

		#updates
		if self.menu_active:
			# self.menu.update()
			self.menu.update()

		elif self.talk_1_active:
			self.talk_1.update()

		elif self.talk_2_active:
			self.talk_2.update()

		elif self.talk_3_active:
			self.talk_3.update()

		elif self.desk_active:
			self.window.update()

		elif self.books_active:
			self.books.update()

		elif self.ecoli_active:
			self.ecoli.update()

		elif self.dialogues_active:
			self.dialogues.choosing_character(self.player.character)
			self.dialogues.update()
			
		else:
			self.all_sprites.update(dt)
			self.plant_collision()

		


class CameraGroup(pygame.sprite.Group):
	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()

	def custom_draw(self, player):
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		for layer in LAYERS.values(): # ordem dos sprites (eixo z)
			for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery): # para ordenar os sprites (pelo y) para estar atrás/à frente dos objetos
				if sprite.z == layer:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)


					# # analytics (só para visualizar melhor)
					# if sprite == player:
					# 	pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
					# 	hitbox_rect = player.hitbox.copy()
					# 	hitbox_rect.center = offset_rect.center
					# 	pygame.draw.rect(self.display_surface, 'green', hitbox_rect, 5)
					# 	target_pos = offset_rect.center + PLAYER_TOOL_OFFSET[player.status.split('_')[0]]
					# 	pygame.draw.circle(self.display_surface, 'blue', target_pos, 5)