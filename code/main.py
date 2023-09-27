import pygame, sys
from settings import *
from level import Level
from intro import Intro
from save_load import *
from functions import animation_text_save
import os

class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Lab Hero')
		self.clock = pygame.time.Clock()
		self.intro = Intro()
		self.intro_run()


	def intro_run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit() 
				if pygame.key.get_pressed()[pygame.K_RETURN]:
					# load game if exists
					try:
						data = load_file('player_history/data')
						self.level = Level(data)
					except FileNotFoundError:
						# self.level = Level(DEFAULT_INVENTORY)
						self.level = Level(DEFAULT_INVENTORY_2)
					self.run()
				elif pygame.key.get_pressed()[pygame.K_SPACE]:
					self.level = Level(DEFAULT_INVENTORY_2)
					if os.path.exists("player_history/data.txt"):
						os.remove("player_history/data.txt")
					if os.path.exists("player_history/results.txt"):
						os.remove("player_history/results.txt")
					if os.path.exists("player_history/simulation_file.txt"):
						os.remove("player_history/simulation_file.txt")
					self.run()
  
			self.intro.run()
			pygame.display.update()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					animation_text_save('Saving Game', fullscreen=True)
					save_file([self.level.player.results, self.level.player.missions_activated, self.level.player.missions_completed])
					pygame.quit()
					sys.exit()
					
			dt = self.clock.tick() / 1000 
			self.level.run(dt)
			pygame.display.update()
		

if __name__ == '__main__':
	game = Game()
	game.run()
