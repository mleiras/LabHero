import asyncio
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


_animation_queue = []


def animation_text_save(text, time=1200, fullscreen=False):
    """Queue a text overlay to be drawn for ~time ms. Drained by the async game/menu loop."""
    _animation_queue.append((text, time, fullscreen))


async def drain_animations():
    """Play any queued animations one at a time. Called each frame by the async loops."""
    while _animation_queue:
        text, time_ms, fullscreen = _animation_queue.pop(0)
        await _play_animation(text, time_ms, fullscreen)


async def _play_animation(text, time, fullscreen):
    display_surface = pygame.display.get_surface()
    font_path = get_resource_path('font/LycheeSoda.ttf')

    if fullscreen:
        time = 1000
        display_surface.fill('gold')
        title = pygame.font.Font(font_path,100).render('Lab Hero', False, 'black')
        title_rect = title.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        display_surface.blit(title, title_rect)

    clock = pygame.time.Clock()
    elapsed = 0
    while elapsed < time:
        text_surf = pygame.font.Font(font_path, 30).render(text,False,'black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT-20))
        pygame.draw.rect(display_surface, 'white', text_rect.inflate(10,10),0,2)
        display_surface.blit(text_surf, text_rect)
        pygame.display.update()
        passed = clock.tick(60)
        elapsed += passed
        await asyncio.sleep(0)
