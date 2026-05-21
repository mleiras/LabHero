import sys
import os
import asyncio

sys.path.append(os.path.join(os.path.dirname(__file__), 'code'))

import pygame

from settings import *
from level import Level
from intro import Intro
from save_load import *
from functions import animation_text_save, drain_animations
from utils import *


class Game:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_icon(pygame.image.load(get_resource_path('LabHero-icon.png')))
		pygame.display.set_caption('Lab Hero')
		self.clock = pygame.time.Clock()
		self.intro = Intro()


	async def intro_run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

				if pygame.key.get_pressed()[pygame.K_RETURN]:
					try:
						data = load_file(get_save_path('data'))
						self.level = Level(data)
					except FileNotFoundError:
						self.level = Level(DEFAULT_INVENTORY_2)
					await self.run()
				elif pygame.key.get_pressed()[pygame.K_SPACE]:
					self.level = Level(DEFAULT_INVENTORY_2)
					if os.path.exists(get_save_path("data.txt")):
						os.remove(get_save_path("data.txt"))
					if os.path.exists(get_save_path("results.txt")):
						os.remove(get_save_path("results.txt"))
					if os.path.exists(get_save_path("simulation_file.txt")):
						os.remove(get_save_path("simulation_file.txt"))
					await self.run()

			self.intro.run()
			if self.intro.pending is not None:
				coro_factory = self.intro.pending
				self.intro.pending = None
				await coro_factory()
			pygame.display.update()
			await drain_animations()
			await asyncio.sleep(0)


	async def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					animation_text_save('Saving Game', fullscreen=True)
					await drain_animations()
					save_file([self.level.player.player_name, self.level.player.results, self.level.player.missions_activated, self.level.player.missions_completed])
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000
			await self.level.run(dt)
			pygame.display.update()
			await drain_animations()
			await asyncio.sleep(0)


async def main():
	game = Game()
	await game.intro_run()


if __name__ == '__main__':
	asyncio.run(main())
