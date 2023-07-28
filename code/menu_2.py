import pygame
import pygame_menu
from settings import *
from timers import Timer

class Menu:
    def __init__(self) -> None:
        surface = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

        # movement
        self.index = 0
        self.timer = Timer(200)

        menu = pygame_menu.Menu('Lab Hero Settings', 400, 300,
                        onclose=pygame_menu.events.CLOSE,
                        theme=pygame_menu.themes.THEME_BLUE)

        menu.add.text_input('Name :', default='Monica')
        menu.add.selector('Difficulty :', [('Easy', 1), ('Hard', 2)], onchange=self.set_difficulty)
        menu.add.button('Play', pygame_menu.events.CLOSE)
        menu.add.button('Quit', pygame_menu.events.EXIT)
        menu.mainloop(surface)



    def set_difficulty(value, difficulty):
        # Do the job here !
        pass

    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.menu.CLOSE()
        
        # if not self.timer.active:
        #     if keys[pygame.K_UP]:
        #         self.index -= 1
        #         self.timer.activate()
        #     if keys[pygame.K_DOWN]:
        #         self.index += 1
        #         self.timer.activate()

        #     if keys[pygame.K_SPACE]:
        #         self.timer.activate()
        #         # get item
        #         current_item = self.options[self.index]

        #         # sell
        #         if self.index <= self.sell_border:
        #             if self.player.item_inventory[current_item] > 0:
        #                 self.player.item_inventory[current_item] -= 1
        #                 self.player.money += SALE_PRICES[current_item]
        #         # buy
        #         else:
        #             seed_price = PURCHASE_PRICES[current_item]
        #             if self.player.money >= seed_price:
        #                 self.player.seed_inventory[current_item] += 1
        #                 self.player.money -= seed_price
                
        # # values
        # if self.index < 0:
        #     self.index = len(self.options) -1
        # if self.index > len(self.options)-1:
        #     self.index = 0

    def update(self):
        self.input()
        



    

