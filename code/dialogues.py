import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from button import Button
from utils import *

class Dialogues: 
    def __init__(self,toggle_menu, player) -> None: # add variable name character to change message and id
        #general setup 
        self.player = player
        self.character = None

        self.toggle_menu = toggle_menu

        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path,30)
        self.font_nome = pygame.font.Font(font_path,24)
        self.screen = pygame.display.get_surface() 
        self.timer = Timer(200)
        self.imagem_path = None
        self.nome = None



    def choosing_character(self, character):
        self.character = character
        if self.character == 'Sequeira':    
            self.message = [
            "Hey there, jolly chap! I am Dr. João Sequeira, and my line of research is meta-omics,",
            "which means I study complex microbial communities through their collective DNA, RNA",
             "and proteins!",
             " ",
            "Now go on, and be the best pokemon master you can be! Gotta catchem' all!"
        ]
            self.imagem_path = get_resource_path('graphics/dialogues/Sequeira.jpg')
            self.nome = self.font_nome.render('Dr. Sequeira', True, 'black')
            
        elif self.character == 'Nuno':    
            self.message = [
            "Hello! My name is Dr. Nuno Alves!",
            " ",
            "I'm currently doing my PhD where I'm trying to use Artificial Intelligence",
            "to find novel antibiotics for Mycobacterium tuberculosis."
        ]
            self.imagem_path = get_resource_path('graphics/dialogues/Nuno.jpg')
            self.nome = self.font_nome.render('Dr. Alves', True, 'black')
        elif self.character == 'Pacheco':
            self.message = [
            "Oh hello, fellow student! My name is Dr. Miguel Pacheco and I'm trying to improve the",
            "production of bacterial cellulose. For that, I'm building a Genome-Scale Metabolic Model,",
            "as well as, conducting experiments in laboratory to confirm that I'm being successful",
            "in my quest! Let's both try our best!"
            ]
            self.imagem_path = get_resource_path('graphics/dialogues/Pacheco.jpg')
            self.nome = self.font_nome.render('Dr. Pacheco', True, 'black')

        elif self.character == 'Marta':
            self.message = [
            "I'm Marta!"
            ]
            self.imagem_path = get_resource_path('graphics/dialogues/martinez.jpg')
            self.nome = self.font_nome.render('Dra. Marta', True, 'black')
        
        elif self.character == 'Capela':
            self.message = [
            "I'm Capela!"
            ]
            self.imagem_path = get_resource_path('graphics/dialogues/silva.jpg')
            self.nome = self.font_nome.render('Dr. Capela', True, 'black')

        elif self.character == 'Fernanda':
            self.message = [
            "Hey there! I am Dr. Fernanda Vieira and my research focuses on phage therapy.",
            "This means I explore the intricate world of viral communities, specifically phages,",
            "by studying their interactions with the host organisms.",
            "Interesting, right?"
            ]
            self.imagem_path = get_resource_path('graphics/dialogues/martinez.jpg')
            self.nome = self.font_nome.render('Dra. Vieira', True, 'black')

        elif self.character == 'Alexandre':
            self.message = [
            "Hello there! My name is Dr. Alexandre Oliveira, and I am studying the metabolic",
            "interactions between SARS-CoV-2 and various human tissues using genome-scale",
            "metabolic models.",
            "SARS-COV-2 is a strain of coronavirus that causes COVID-19!"
            ]
            self.imagem_path = get_resource_path('graphics/dialogues/silva.jpg')
            self.nome = self.font_nome.render('Dr. Oliveira', True, 'black')

        elif self.character == 'Emanuel':
            self.message = [
            "Hey there! I am Dr. Emanuel Cunha, and my line of research is systems biology.",
            "Currently, I'm studying pigment and lipid production by microalgae using",
            "genome-scale metabolic models.",
            "Do you already know what GEMs are?"
            ]
            self.imagem_path = get_resource_path('graphics/dialogues/silva.jpg')
            self.nome = self.font_nome.render('Dr. Cunha', True, 'black')

        else:
            self.message = ['Hello there! Are you enjoying LabHero so far?']
            self.imagem_path = get_resource_path('graphics/dialogues/carter.jpg')
            self.nome = self.font_nome.render('Dr.', True, 'black')


    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()

    def update(self):
        self.input()
        self.menu_message(self.message, buttons=False)


    def menu_message(self, message, buttons = False):

        menu_border = pygame.draw.rect(self.screen, (255,215,0), [0,500,1280,220], width=5)
        menu_bg = pygame.draw.rect(self.screen, (186,214,177), [5,505,1270,210])

        imagem = pygame.image.load(self.imagem_path).convert()
        
        x = 25; # x coordnate of image
        y = 520; # y coordinate of image
        self.screen.blit(imagem, ( x,y))

        cientista_rect = pygame.draw.rect(self.screen, 'white', [25,675,150,25])

        # nome = self.font_nome.render('Dr. Sequeira', True, 'black')
        self.screen.blit(self.nome,(40,677))

        for line, msg in enumerate(message):
            surf = self.font.render(msg, True, 'black')
            self.screen.blit(surf,(200,525+(line*20)+(15*line)))

        if buttons:
            botao_teste = Button(200,650,150,50,self.screen, 'Yes', self.menu.update)
            botao_teste_2 = Button(370,650,220,50,self.screen, 'Not now', self.toggle_menu)
            botao_teste.process()
            botao_teste_2.process()

        

        pygame.display.flip()

