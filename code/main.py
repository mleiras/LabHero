import pygame, sys
from settings import *
from level import Level
from intro import Intro
from save_load import *
import pygame_menu

# from scrollbar import *

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Lab Hero') 
		self.clock = pygame.time.Clock()
		self.intro = Intro()
		
		# load game if exists
		try:
			name, *data = load_file('data')
			print('continue game')
			self.level = Level(data)
		# if not, default values 
		except:
			self.level = Level(DEFAULT_INVENTORY)

		self.intro_run()

	def intro_run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit() 
				if pygame.key.get_pressed()[pygame.K_RETURN]:
					self.run()
				# if event.type == pygame.KEYDOWN:
					# self.run()
  
			self.intro.run()
			pygame.display.update()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					save_file([self.level.player.item_inventory, self.level.player.seed_inventory, self.level.player.money])
					pygame.quit()
					sys.exit()
					
  
			dt = self.clock.tick() / 1000 # retirar o 30 depois
			self.level.run(dt)
			pygame.display.update()
		

# class GameState():
# 	def __init__(self):
# 		self.state = 'main_game'

# 		for event in pygame.event.get():
# 			if event.type == pygame.QUIT:
# 				save_file([self.level.player.item_inventory, self.level.player.seed_inventory, self.level.player.money])
# 				pygame.quit()
# 				sys.exit()
  
# 		dt = self.clock.tick() / 1000 # retirar o 30 depois
# 		self.level.run(dt)
# 		pygame.display.update()



if __name__ == '__main__':
	game = Game()
	game.run()
