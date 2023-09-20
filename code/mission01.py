import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from functions import animation_text_save
import textwrap


#############################################

class Mission01: # alterar nome classe no caso de usar para todas
    def __init__(self, toggle_menu) -> None:
        self.toggle_menu = toggle_menu

        self.font = pygame.font.Font('../font/LycheeSoda.ttf',24)
        self.screen = pygame.display.get_surface() ### set_mode([1280,720])
        self.timer = Timer(200)

        # pygame.draw.rect(self.screen, 'black', [0,520,1280,200])

        self.mission01 = """Lorem ipsum dolor sit amet, consectetur adipiscing elit"""

        self.mission01_list = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit",
                          "Teste 2",
                          "Testeeeeeee 3"]
        self.done = False

    

    def update(self):
        # mission = self.mission01
        message = self.mission01
        # active_message = 0
        # message = mission[active_message]
        # snip = self.font.render('', True, 'white')
        counter = 0
        message_counter = 0
        speed = 100
        pygame.draw.rect(self.screen, 'black', [0,520,1280,200])

        while message_counter < len(self.mission01_list)-1 and not self.done:

        # while not self.done:
            if counter < (speed*len(message)):
                counter += 1
            elif counter >= speed * len(message):
                self.done = True

            # for event in pygame.event.get():
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_RETURN and done and active_message < len(message)-1:
            #             active_message += 1
            #             done = False
            #             message = mission[active_message]
            #             counter = 0
            
            # print(int(counter//(1/speed)))

            line_height = 530

            for m in self.mission01_list:
                
                snip = self.font.render(m[0:(counter//speed)], True, 'white')
                self.screen.blit(snip, (10, line_height))
                line_height += 20
                # message_counter += 1

            pygame.display.flip()

        if self.done:
            snip = self.font.render(message, True, 'white')
            self.screen.blit(snip, (10, 530))

            pygame.display.flip()


        


    # def update(self):
    #     self.dialogue()
        



if __name__ == '__main__':
    m1 = Mission01
    m1.update()









# import pygame
# pygame.init()
# font = pygame.font.Font('../font/LycheeSoda.ttf',24)
# screen = pygame.display.set_mode([1280,720])
# timer = pygame.time.Clock()
# messages = ['This is a message. \n Please enter ENTER to continue the dialogue. This is a message. This is a message. \n Please enter ENTER to continue the dialogue.',
#             'Another one.',
#             'This is a test for LabHero!']
# active_message = 0
# message = messages[active_message]
# snip = font.render('', True, 'white')
# counter = 0
# speed = 3
# done = False

# run = True
# while run:
#     screen.fill('yellow')
#     timer.tick(60)
#     pygame.draw.rect(screen, 'black', [0,520,1280,200])
#     if counter < speed * len(message):
#         counter += 1
#     elif counter >= speed * len(message):
#         done = True

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_RETURN and done and active_message < len(messages)-1:
#                 active_message += 1
#                 done = False
#                 message = messages[active_message]
#                 counter = 0
    

#     snip = font.render(message[0:counter//speed], True, 'white')
#     screen.blit(snip, (10, 530))

#     pygame.display.flip()

# pygame.quit()







# class Mission01:
#     def __init__(self, toggle_menu):
#         self.toggle_menu = toggle_menu
#         self.display_surface = pygame.display.get_surface()
#         self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)

#         options
#         self.width = 400
#         self.space = 10
#         self.padding = 8

#         self.setup()
        
#         self.index = 0
#         self.timer = Timer(200)

#         self.mission01 = False # mudar com o load game

#     def setup(self):
#         self.text_surfs = []
#         self.total_height = 400
#         for item in self.options:
#             text_surf = self.font.render(item, False, 'black') # render(string, AA, color)
#             self.text_surfs.append(text_surf)
#             self.total_height += text_surf.get_height() + (self.padding*2)
#         self.total_height += (len(self.text_surfs) - 1) * self.space
#         self.menu_top = SCREEN_HEIGHT / 2 # - self.total_height / 2 # meio da janela prinicpal - meio da altura do menu (assim o menu fica centrado verticalmente)
#         self.menu_width = SCREEN_WIDTH / 2 # - self.width / 2 # meio da janela prinicpal - meio da largura do menu (assim o menu fica centrado horizontalmente)
#         self.main_rect = pygame.Rect(self.menu_width, self.menu_top, self.width, self.total_height) # left, top, width and height
        


#     def display_text(self):
#         text_surf = self.font.render('Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
#             'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
#             'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea ',
#             False,'black')
#         text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

#         pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(10,10),0,2) #ultimos 2 argumentos se quiser bordas redondas pode-se adicionar estes argumentos
#         self.display_surface.blit(text_surf, text_rect)



#     def input(self):
#         keys = pygame.key.get_pressed()
#         self.timer.update()

#         if keys[pygame.K_ESCAPE]:
#             self.toggle_menu()
        
#         if not self.timer.active:
#             if keys[pygame.K_UP]:
#                 self.index -= 1
#                 self.timer.activate()
#             if keys[pygame.K_DOWN]:
#                 self.index += 1
#                 self.timer.activate()


#     def update(self):
#         self.input()
#         self.display_text()






# class Mission01:
#     def __init__(self, toggle_menu) -> None:

#         # general setup
#         self.toggle_menu = toggle_menu
#         self.display_surface = pygame.display.get_surface()
#         self.font = pygame.font.Font('../font/LycheeSoda.ttf',30)
        
#         self.index = 0
#         self.timer = Timer(200)

#         self.mission01 = False # mudar com o load game



#     def setup(self):
        
#         menu = pygame_menu.Menu(
#             height=720,
#             onclose=self.toggle_menu,
#             theme=mytheme,
#             title='Mission 1',
#             width=1280,
#         )

#         menu_text = pygame_menu.Menu(
#             height=720,
#             onclose=self.toggle_menu,
#             theme=mytheme,
#             title='About Mission 01',
#             width=1280
#         )


#         menu_text.add.label(
#             'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
#             'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
#             'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
#             'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
#             'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
#             'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
#             'id est laborum.'
#             'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
#             'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
#             'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
#             'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
#             'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
#             'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
#             'id est laborum.'
#             'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
#             'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
#             'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
#             'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
#             'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
#             'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
#             'id est laborum.'
#             'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
#             'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
#             'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
#             'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
#             'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
#             'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
#             'id est laborum.'
#             'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
#             'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim '
#             'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea '
#             'commodo consequat. Duis aute irure dolor in reprehenderit in voluptate '
#             'velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat '
#             'cupidatat non proident, sunt in culpa qui officia deserunt mollit anim '
#             'id est laborum.',
#             max_char=33,
#             wordwrap=True
#         )
#         menu_text.add.button('Back', pygame_menu.events.BACK, background_color=(70, 70, 70))

        


#         image_path = '../graphics/objects/merchant.png'
#         menu.add.image(image_path, scale=(2,2))
#         menu.add.label(
#             'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod '
#             'tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim.'

#             'veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea ',
#             wordwrap=True,
#             align=pygame_menu.locals.ALIGN_CENTER,
#             font_size=30)
#         menu.add.button('More Info', menu_text)
#         menu.add.vertical_margin(50)  
#         if self.mission01:
#             menu.add.label('Mission Activated', font_color=(150, 150, 150))
#             menu.add.vertical_margin(20)  
#             menu.add.button('Deliver Results', action=None, background_color=(50,100,100)) ## TASK: ADICIONAR FUNÇÃO ENTREGAR RESULTADOS  
#         else:
#             menu.add.button('Activate Mission', action=self.activate_mission01, background_color=(50,100,100))        
#         menu.add.vertical_margin(20)  

#         menu.mainloop(self.display_surface)

        


#     def toggle_menu(self):
#         self.toggle_shop = not self.toggle_shop

#     def activate_mission01(self):
#         self.mission01 = True
#         animation_text_save('Mission 01 Activated')



#     def input(self):
#         keys = pygame.key.get_pressed()
#         self.timer.update()

#         if keys[pygame.K_ESCAPE]:
#             pygame_menu.events.BACK
            

#     def update(self):
#         self.input()
#         self.setup()
        


