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



def drawText(surface, text, color, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break

        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if we've wrapped the text, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and blit it to the surface
        if bkg:
            image = font.render(text[:i], 1, color, bkg)
            image.set_colorkey(bkg)
        else:
            image = font.render(text[:i], aa, color)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text we just blitted
        text = text[i:]

    return text