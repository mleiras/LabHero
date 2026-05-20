import asyncio
import sys

import pygame

from functions import drain_animations


async def run_menu(menu, surface, on_update=None):
    """Async replacement for pygame_menu.Menu.mainloop.

    Yields to the event loop every frame so pygbag/wasm can pump browser events.
    Drains any queued animation_text_save overlays between menu update and next frame.
    on_update: optional callable invoked each frame before menu.update (e.g. ESC handling).
    """
    while menu.is_enabled():
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if on_update is not None:
            on_update()

        if menu.is_enabled():
            menu.update(events)
        if menu.is_enabled():
            menu.draw(surface)

        pygame.display.update()
        await drain_animations()
        await asyncio.sleep(0)
