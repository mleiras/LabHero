import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from button import Button


class Dialogues: 
    def __init__(self, toggle_menu, player) -> None:
        #general setup 
        self.player = player

        self.toggle_menu = toggle_menu

        self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        self.font_nome = pygame.font.Font('../font/LycheeSoda.ttf',24)
        self.screen = pygame.display.get_surface() 
        self.timer = Timer(200)

    
    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
        self.m01_step1 = [
            "Hey there, jolly chap! I am Dr. João Sequeira, and my line of research is meta-omics,",
            "which means I study complex microbial communities through their collective DNA, RNA",
             "and proteins!",
             " ",
            "Now go on, and be the best pokemon master you can be! Gotta catchem' all!"
        ]
           
        self.input()

        self.menu_message(self.m01_step1, buttons=False)


       

    def menu_message(self, message, buttons = False):

        menu_border = pygame.draw.rect(self.screen, (255,215,0), [0,500,1280,220], width=5)
        menu_bg = pygame.draw.rect(self.screen, (186,214,177), [5,505,1270,210])

        # pygame.display.set_caption('Cientista')
        imagem = pygame.image.load("../graphics/dialogues/Sequeira.jpg").convert()
        
        x = 25; # x coordnate of image
        y = 520; # y coordinate of image
        self.screen.blit(imagem, ( x,y))

        cientista_rect = pygame.draw.rect(self.screen, 'white', [25,675,150,25])

        nome = self.font_nome.render('Dr. Sequeira', True, 'black')
        self.screen.blit(nome,(40,677))

        for line, msg in enumerate(message):
            surf = self.font.render(msg, True, 'black')
            self.screen.blit(surf,(200,525+(line*20)+(15*line)))

        if buttons:
            botao_teste = Button(200,650,150,50,self.screen, 'Yes', self.menu.update)
            botao_teste_2 = Button(370,650,220,50,self.screen, 'Not now', self.toggle_menu)
            botao_teste.process()
            botao_teste_2.process()

        pygame.display.flip()

