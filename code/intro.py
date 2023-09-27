import pygame 
from settings import *
from timers import Timer
from button import Button


class Intro:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.font = pygame.font.Font('../font/LycheeSoda.ttf',100)
		self.font_text = pygame.font.Font('../font/LycheeSoda.ttf',30)
		self.width = 400
		self.space = 10
		self.padding = 8

		
	def run(self):
		self.display_surface.fill('gold')
		self.title = self.font.render('Lab Hero', False, 'black') # render(string, AA, color)
		self.title_rect = self.title.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
		self.display_surface.blit(self.title, self.title_rect)
		self.text = self.font_text.render('press ENTER to continue', False, 'red') # render(string, AA, color)
		self.text2 = self.font_text.render('or press SPACE to new game', False, (60,150,140)) # render(string, AA, color)
		self.text_rect = self.text.get_rect(center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+75))
		self.text_rect2 = self.text2.get_rect(center = (SCREEN_WIDTH/2, (SCREEN_HEIGHT/2)+120))
		self.display_surface.blit(self.text, self.text_rect)
		self.display_surface.blit(self.text2, self.text_rect2)


		
		

