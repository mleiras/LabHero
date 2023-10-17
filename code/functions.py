import pygame
from settings import *
from os import walk

def import_folder(path):
    surface_list = []

    for _,__,img_files in walk(path):
        for img_file in sorted(img_files):
            full_path = path + "/" + img_file
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)


    return surface_list


def import_folder_dict(path):
    surface_dict = {}

    for _,__,img_files in walk(path):
        for img_file in sorted(img_files):
            full_path = path + "/" + img_file
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_dict[img_file.split('.')[0]] = image_surf

    return surface_dict
    

def animation_text_save(text, time=1200, fullscreen=False):
        display_surface = pygame.display.get_surface()

        if fullscreen:
            time = 1000
            display_surface.fill('gold')
            title = pygame.font.Font('../font/LycheeSoda.ttf',100).render('Lab Hero', False, 'black')
            title_rect = title.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            display_surface.blit(title, title_rect)

        sceneExit = False
        # time = 1500

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


