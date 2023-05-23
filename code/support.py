import pygame
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