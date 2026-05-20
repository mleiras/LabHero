import sys

import pygame_menu

from utils import *


mytheme = pygame_menu.themes.THEME_GREEN.copy()
font = pygame_menu.font.FONT_MUNRO
mytheme.widget_font = font
mytheme.title_font = font
mytheme.title_font_size = 50
mytheme.title_bar_style = pygame_menu.widgets.MENUBAR_STYLE_SIMPLE
mytheme.title_offset = (20, 4)
mytheme.widget_margin = (10, 10)
mytheme.widget_font_color = 'black'

tutorial_theme = mytheme.copy()
tutorial_theme.background_color = (255, 215, 0, 255)


model_path = get_resource_path('data/models/e_coli_core.xml.gz')


class _IndexableList:
    def __init__(self, items):
        self._items = list(items)

    def __len__(self):
        return len(self._items)

    def __getitem__(self, i):
        return self._items[i]

    def __iter__(self):
        return iter(self._items)


class _Series(_IndexableList):
    @property
    def iloc(self):
        return self


class _DF:
    def __init__(self, index, name=None, lb=None, ub=None):
        self.index = _IndexableList(index)
        self.name = _Series(name if name is not None else index)
        self.lb = _Series(lb) if lb is not None else None
        self.ub = _Series(ub) if ub is not None else None

    def __len__(self):
        return len(self.index)


if sys.platform == 'emscripten':
    import json
    with open(get_resource_path('data/models/e_coli_core_meta.json'), encoding='utf-8') as f:
        _meta = json.load(f)
    model = None
    simul = None
    objective = _meta['objective']
    REACTIONS = _DF(
        index=_meta['reactions_ex']['index'],
        name=_meta['reactions_ex']['name'],
        lb=_meta['reactions_ex']['lb'],
        ub=_meta['reactions_ex']['ub'],
    )
    REACTIONS_v0 = _DF(index=_meta['reactions_all']['index'])
    GENES_v0 = None
    GENES = list(_meta['genes'])
else:
    import mewpy
    from mewpy.simulation import get_simulator
    from cobra.io import read_sbml_model

    model = read_sbml_model(model_path)
    simul = get_simulator(model)
    objective = list(simul.objective.keys())[0]
    REACTIONS_v0 = simul.find_reactions()
    REACTIONS = simul.find_reactions('EX')
    GENES_v0 = simul.find_genes().name
    GENES = [name for (name, _) in GENES_v0.items()]


if __name__ == '__main__':
    print(GENES)
    print(REACTIONS_v0)
