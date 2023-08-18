import pygame
from settings import *

def animation_text_save(text):
        display_surface = pygame.display.get_surface()

        sceneExit = False
        time = 1500

        while not sceneExit:

            text_surf = pygame.font.Font('../font/LycheeSoda.ttf',30).render(text,False,'black')
            text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-20))
            pygame.draw.rect(display_surface, 'white', text_rect.inflate(10,10),0,2) #ultimos 2 argumentos se quiser bordas redondas pode-se adicionar estes argumentos
            display_surface.blit(text_surf, text_rect)

            pygame.display.update()

            passed_time = pygame.time.Clock().tick(60)
            time -= passed_time
            if time <= 0:
                sceneExit = True