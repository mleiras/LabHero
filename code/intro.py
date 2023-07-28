import pygame 
from settings import *
from timers import Timer


class Intro:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font('../font/LycheeSoda.ttf',100)
		self.font_text = pygame.font.Font('../font/LycheeSoda.ttf',30)
		self.width = 400
		self.space = 10
		self.padding = 8
		
	def run(self):
		self.total_height = 0
		self.display_surface.fill('gold')
		self.title = self.font.render('Lab Hero', False, 'black') # render(string, AA, color)
		self.title_rect = self.title.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		self.display_surface.blit(self.title, self.title_rect)
		self.text = self.font_text.render('press any key to start', False, 'red') # render(string, AA, color)
		self.text_rect = self.text.get_rect(center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+75))
		self.display_surface.blit(self.text, self.text_rect)


		
		

