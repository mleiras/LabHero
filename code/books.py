import pygame
import pygame_menu
from settings import *
from save_load import *
from timers import Timer
from options_values import *
from async_menu import run_menu


class Books:
    def __init__(self, toggle_menu) -> None:

        # general setup
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        font_path = get_resource_path('font/LycheeSoda.ttf')
        self.font = pygame.font.Font(font_path, 30)

        # movement
        self.index = 0
        self.timer = Timer(200)

        # lazy book state
        self._pending_book = None
        self._top_menu = None


    def _on_book_click(self, book_id):
        def handler():
            self._pending_book = book_id
            if self._top_menu is not None:
                self._top_menu.disable()
        return handler


    def _build_top_menu(self):
        menu = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Books',
            width=1280
        )
        menu.add.label(
            'Books Available:',
            align=pygame_menu.locals.ALIGN_CENTER,
            font_size=50,
            font_color=(70,70,70))
        menu.add.vertical_margin(15)
        menu.add.button('How to Play', self._on_book_click('how_to_play'), background_color = (255,215,0, 255))
        menu.add.button('How to Simulate', self._on_book_click('how_to_simulate'), background_color = 'royalblue')
        menu.add.button('A Brief History of Microorganisms', self._on_book_click('brief_history'), background_color = 'green')
        menu.add.button('Intro to Modelling', self._on_book_click('intro_modelling'), background_color = 'orange')
        menu.add.button('E. coli Basics', self._on_book_click('ecoli'), background_color = 'violet')
        menu.add.button('Eat, Breathe and Love', self._on_book_click('eat_breathe_love'), background_color = 'red')
        return menu


    def _build_book(self, book_id):
        builders = {
            'how_to_play': self._build_how_to_play,
            'how_to_simulate': self._build_how_to_simulate,
            'brief_history': self._build_brief_history,
            'intro_modelling': self._build_intro_modelling,
            'ecoli': self._build_ecoli,
            'eat_breathe_love': self._build_eat_breathe_love,
        }
        return builders[book_id]()


    def _close_back(self, menu):
        def handler():
            menu.disable()
        return handler


    def _build_brief_history(self):
        book_brief_history = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='A Brief History of Microorganisms',
            width=1280,
            column_max_width=1280
        )

        book_brief_history.add.label(
            """
            This book is your guide to the incredible world of microorganisms. You'll learn how these tiny beings are everywhere around us, how they help or sometimes harm us, and how science and technology have helped us understand and live safely with them. Enjoy your journey into the microscopic world!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_brief_history.add.label(
            """
            Chapter 1: Microscopic Marvels
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkgreen',
            font_size = 35
        )
        book_brief_history.add.label(
            """
            Meet the Microorganisms
            Microorganisms are tiny living beings that are so small you can't see them without a special tool called a microscope. What makes them special is their small size and simple structure. Most of them are made up of just one cell!

            Where Do They Live?
            Microorganisms live everywhere, from the deepest parts of the ocean to hot springs and even inside your own body. They're like nature's little helpers, always there to do important jobs.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_brief_history.add.label(
            """
            Chapter 2: Microbes: Team Players
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkgreen',
            font_size = 35
        )
        book_brief_history.add.label(
            """
            We Depend on Each Other
            All living things, including us and microorganisms, rely on each other to survive. It's like a big team where everyone has a job to do. Microbes are like the superheroes of this team because they help keep the world in balance.

            Growing and Changing
            Microbes can reproduce really quickly, and sometimes their babies look just like them. But other times, they change a bit because of their environment. This is like a superpower that helps them adapt to different places.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_brief_history.add.label(
            """
            Chapter 3: Breathing and Living
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkgreen',
            font_size = 35
        )
        book_brief_history.add.label(
            """
            Breathing: Inside and Outside
            Just like we need to breathe, microorganisms do too. They have two ways of doing it. One way is by taking in air from their environment (external respiration), and the other is by using nutrients and oxygen to make energy (cellular respiration).

            Where They Live Matters
            Where microorganisms make their home affects how they get the air they need to breathe. Think of it like this: different places require different tools for breathing.

            Water World: Imagine tiny microorganisms living in water, like fish in a pond. They don't have gills, but it's as if they have their own secret ways to breathe underwater.
            Land Life: Now, picture other microorganisms living on land, just like we do. They don't have lungs, but they've found clever ways to breathe the air around them.

            So, even though they don't have gills or lungs like fish or humans, microorganisms have special adaptations to survive in their unique homes. It's all about using the right tools for the right job in their tiny worlds.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_brief_history.add.label(
            """
            Chapter 4: Microscopes: Windows to the Tiny World
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkgreen',
            font_size = 35
        )
        book_brief_history.add.label(
            """
            The Power of Microscopes
            Have you ever wondered how we discovered microorganisms? It's all thanks to super cool tools called microscopes. These amazing devices let scientists see things that are too small for our eyes.

            Microbe Detectives
            With microscopes, scientists became detectives, finding and studying microorganisms. It's like discovering a whole new world right under our noses!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_brief_history.add.label(
            """
            Chapter 5: Good Guys and Bad Guys
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkgreen',
            font_size = 35
        )
        book_brief_history.add.label(
            """
            Different Types of Microbes
            Microbes come in different types. Some are friendly and help us, like the ones in our gut that help with digestion. Others can be harmful, causing diseases. It's important to know the difference.

            Keeping Food Safe
            Microbes can make food go bad. But we've figured out ways to stop them, like refrigerating food or cooking it. This keeps us healthy by preventing food based illnesses.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_brief_history.add.label(
            """
            Chapter 6: Staying Healthy
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkgreen',
            font_size = 35
        )
        book_brief_history.add.label(
            """
            Vaccines: Our Super Shields
            Vaccines are like shields that protect us from harmful microorganisms. They train our bodies to fight off bad guys, so we don't get sick. It's like having a superhero army inside us!

            Using Medicine Wisely
            When we do get sick, doctors might give us medicine like antibiotics. These medicines are like superheroes that battle harmful microbes. But it's important to use them wisely and only when needed."
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_brief_history.add.button('Back', self._close_back(book_brief_history), background_color=(70, 70, 70))
        book_brief_history.add.vertical_margin(20)
        return book_brief_history


    def _build_intro_modelling(self):
        book_intro_modelling = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Intro to Modelling',
            width=1280,
            column_max_width=1280
        )

        book_intro_modelling.add.label(
            """
            This book takes you on a journey into the fascinating world of metabolic modeling, using E. coli as a guide.
            It shows how understanding metabolism is a key to solving real-world challenges and encourages young minds to explore the incredible possibilities of science.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_intro_modelling.add.label(
            """
            Chapter 1: The Secret Life of Cells
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkorange',
            font_size = 35
        )
        book_intro_modelling.add.label(
            """
            Meet the Tiny World Inside Cells
            Did you know that every living thing, including you, is made up of millions of tiny building blocks called cells? These cells are like little factories, working day and night to keep you alive. But there's a secret world inside them that's even more amazing!

            What's Metabolism?
            Cells need energy to do their jobs, just like we need food to have energy. Metabolism is like the recipe book that cells use to turn food into energy. It's a super important job!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_intro_modelling.add.label(
            """
            Chapter 2: Meet E. coli
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkorange',
            font_size = 35
        )
        book_intro_modelling.add.label(
            """
            Hello, E. coli!
            Imagine a tiny bacterium called E. coli. It's so small you can't see it without a microscope. E. coli is like a tiny superhero because it helps scientists learn about metabolism.

            Why E. coli?
            Scientists love using E. coli because it's a bit like a laboratory assistant. It's simple to study, and what we learn from it can help us understand the metabolism of other living things, including humans.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_intro_modelling.add.label(
            """
            Chapter 3: The Puzzle of Metabolic Models
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkorange',
            font_size = 35
        )
        book_intro_modelling.add.label(
            """
            What Are Metabolic Models?
            Metabolic models are like jigsaw puzzles. Scientists use them to figure out how cells work. These models are full of tiny pieces, just like a puzzle.

            Why Do We Need Metabolic Models?
            Imagine you're solving a big puzzle. You can't just put pieces together randomly; you need a plan. Metabolic models help scientists plan how cells use their energy and make things they need.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_intro_modelling.add.label(
            """
            Chapter 4: The Power of Investigation
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkorange',
            font_size = 35
        )
        book_intro_modelling.add.label(
            """
            Unlocking Mysteries
            Investigating metabolic models is like being a detective. Scientists study E. coli's metabolism to understand how it grows, how it uses food, and how it stays healthy.

            Why It Matters
            Understanding metabolism isn't just for fun; it's super important for our world! It can help us make medicines, create biofuels to save our planet, and even find ways to feed more people.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_intro_modelling.add.label(
            """
            Chapter 5: Join the Adventure!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkorange',
            font_size = 35
        )
        book_intro_modelling.add.label(
            """
            Be a Young Scientist
            You can be a scientist too! Learn about E. coli and metabolism. You might discover something amazing that can help the world.

            Our Metabolic Future
            As you grow, you'll see how important metabolic models are in solving big problems like making clean energy and finding new cures for diseases. You could be the scientist who changes the world!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_intro_modelling.add.button('Back', self._close_back(book_intro_modelling), background_color=(70, 70, 70))
        book_intro_modelling.add.vertical_margin(20)
        return book_intro_modelling


    def _build_how_to_simulate(self):
        book_how_to_simulate = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='How to Simulate',
            width=1280,
            column_max_width=1280
        )

        book_how_to_simulate.add.label(
            """
            This book provides beginners with a fun and easy-to-understand introduction to metabolic simulations, making complex scientific concepts accessible and exciting. Happy exploring!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_how_to_simulate.add.label(
            """
            Chapter 1: Change Simulation Options
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkblue',
            font_size = 35
        )
        book_how_to_simulate.add.vertical_margin(20)
        book_how_to_simulate.add.label(
            """Simulation Method""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = 'darkblue',
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        book_how_to_simulate.add.label(
            """
            FBA: calculates how microorganisms balance their food intake to maximize their growth.

            pFBA: This method is all about being efficient. It helps you find the most economical way for organisms to use nutrients.

            lMOMA: like a flexible thinker. It helps you see how organisms adapt when conditions change.  lMOMA shows how microorganisms change their metabolic plans when the environment shifts.

            ROOM: the optimal explorer! It helps you understand how organisms make choices, turning some genes on and others off. ROOM reveals how microorganisms regulate their genes to optimize their metabolism.

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_how_to_simulate.add.vertical_margin(20)

        book_how_to_simulate.add.label(
            """Objective""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = 'darkblue',
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        book_how_to_simulate.add.label(
            """
            Biomass is a good objective because it reflects how well E. coli is thriving in the given environment.

            The more biomass, the healthier and more productive the cell is.

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_how_to_simulate.add.vertical_margin(20)

        book_how_to_simulate.add.label(
            """Genes""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = 'darkblue',
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        book_how_to_simulate.add.label(
            """
            Knocking out ("turning off") essential genes can stop E. coli from growing, but knocking out non-essential genes may change its metabolism without harming its survival.

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_how_to_simulate.add.vertical_margin(20)

        book_how_to_simulate.add.label(
            """Environmental Conditions""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = 'darkblue',
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        book_how_to_simulate.add.label(
            """
            Adjust the bounds to control what resources E. coli consumes and how much it produces.

            A small lower bound limits intake, while a large upper bound accelerates production.

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_how_to_simulate.add.vertical_margin(40)

        book_how_to_simulate.add.label(
            """
            Chapter 2: Results
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkblue',
            font_size = 35
        )
        book_how_to_simulate.add.vertical_margin(20)

        book_how_to_simulate.add.label(
            """Biomass""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = 'darkblue',
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        book_how_to_simulate.add.vertical_margin(20)
        book_how_to_simulate.add.label(
            """ When running a simulation, the key result is usually the objective value.

            For example, if you're optimizing for biomass, a higher value means E. coli is growing well.

            If it's low, check your inputs or try different knock-outs and reaction limits because it means E. coli is not growing well.

            If it's null, well, I don't know another way to say this but ... it's dead. YOU KILLED HER!

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_how_to_simulate.add.vertical_margin(20)

        book_how_to_simulate.add.label(
            """Energy Source""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = 'darkblue',
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        book_how_to_simulate.add.vertical_margin(20)
        book_how_to_simulate.add.label(
            """ Energy sources are essential for E. coli to carry out its metabolic processes, powering growth and survival.

            If you remove the glucose bound (set the lower bound to 0), E. coli won't be able to take in glucose, which is its main energy source.

            Without glucose, the cell won't have enough fuel to grow, leading to a drop in biomass. This means that the cell might not survive, as glucose is crucial for many of its metabolic processes.

            So, watch the biomass value after removing glucose—it should decrease significantly!

            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_how_to_simulate.add.vertical_margin(20)
        book_how_to_simulate.add.button('Back', self._close_back(book_how_to_simulate), background_color=(70, 70, 70))
        book_how_to_simulate.add.vertical_margin(20)
        return book_how_to_simulate


    def _build_ecoli(self):
        book_ecoli = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='E. coli Basics',
            width=1280,
            column_max_width=1280
        )

        book_ecoli.add.label(
            """
            This book provides a deep dive into the world of E. coli, focusing on its metabolic model and its importance in scientific research and various industries.
            It's an exploration of a tiny microbe with big contributions to our understanding of life.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_ecoli.add.label(
            """
            Chapter 1: Meet E. coli
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkviolet',
            font_size = 35
        )
        book_ecoli.add.label(
            """
            Introducing Our Tiny Hero

            Meet Escherichia coli, or E. coli for short. It's a microscopic superstar! This tiny bacterium might look simple, but it holds the secrets to understanding how life works at its core.


            E. coli's Microscopic Machinery

            E. coli is like a well-oiled machine, with tiny parts that work together flawlessly. Inside, it has a metabolic model — a set of instructions that tells it how to grow, eat, and survive. Think of it as E. coli's rulebook for life.


            Feeding the Beast

            Just like us, E. coli needs to eat. But instead of burgers and fries, its favorite meal is glucose. It knows how to transform this sugar into energy, fueling its daily activities and growth.


            Breathing Lessons for Microbes

            E. coli has its own way of breathing. Some breathe with oxygen, just like we do. Others are like tiny rebels, thriving without oxygen. It's all part of their amazing adaptability.


            Reproduction, E. coli Style

            E. coli might not have families like we do, but it knows how to make baby E. coli. When conditions are perfect, it multiplies rapidly, filling its world with new generations.


            Beyond the Microscope

            E. coli isn't just a fascinating microbe; it's also a superstar in science and industry. Scientists use it to study life's mysteries, and it plays a vital role in creating medicines, biofuels, and more.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_ecoli.add.label(
            """
            Chapter 2: Metabolic Model
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'darkviolet',
            font_size = 35
        )
        book_ecoli.add.label(
            """
            Core Metabolism of E. coli

            E. coli's core metabolism includes essential biochemical pathways that are crucial for its growth and survival.

            You can see a visual map of these pathways in this link:
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )

        book_ecoli.add.url('https://escher.github.io/#/app?map=e_coli_core.Core%20metabolism&tool=Viewer', 'Escher Map')
        book_ecoli.add.label(
            """
            Escher is an open-source web application that allows you to interactively explore and visualize metabolic maps, which are representations of the biochemical pathways within an organism's metabolism.
            Escher maps like this one are valuable tools for researchers studying the metabolism of microorganisms like E. coli.
            They help visualize complex metabolic networks and gain insights into how genes, enzymes, and metabolites interact to support cellular functions.
            This understanding has applications in various fields, including biotechnology, systems biology, and metabolic engineering.


            Key Features:

            Interactive Exploration: Escher maps are highly interactive. You can zoom in and out, pan across the map, and click on individual metabolites and reactions to view detailed information.

            Pathway Representation: The map displays key metabolic pathways, such as glycolysis, the TCA (tricarboxylic acid) cycle, and the pentose phosphate pathway. These pathways are essential for energy production and biosynthesis.

            Metabolite and Reaction Details: Clicking on a metabolite or reaction node provides information about its name, abbreviation, and associated genes and enzymes. You can also see reaction reversibility and flux values.

            Color Coding: Metabolites and reactions may be color-coded to indicate various properties or conditions, such as metabolite concentration or reaction directionality.

            Search Function: Escher allows you to search for specific metabolites or reactions within the map, making it easy to find and focus on particular components of the metabolic network.

            Export Options: You can export the map for use in presentations or publications, which can be particularly useful for researchers and educators.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_ecoli.add.button('Back', self._close_back(book_ecoli), background_color=(70, 70, 70))
        book_ecoli.add.vertical_margin(20)
        return book_ecoli


    def _build_eat_breathe_love(self):
        book_eat_breathe_love = pygame_menu.Menu(
            height=720,
            onclose=self.toggle_menu,
            theme=mytheme,
            title='Eat, Breathe and Love',
            width=1280,
            column_max_width=1280
        )

        book_eat_breathe_love.add.label(
            """
            This book takes you on a fun and educational journey focusing on how microorganisms eat, breathe, and multiply, highlighting their adaptability and unique characteristics.
            E. coli serves as a friendly example to help kids understand these tiny but fascinating creatures that are all around us.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_eat_breathe_love.add.label(
            """
            Chapter 1: Eat
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'firebrick',
            font_size = 35
        )
        book_eat_breathe_love.add.label(
            """
            What's on the Menu for Microbes?
            Meet our tiny friend, E. coli! Just like you enjoy your favorite foods, microorganisms have their own favorites too. They love to munch on things like glucose, a sugary treat. Imagine E. coli as a tiny snacker, always looking for something yummy to eat.

            Turning Food into Energy
            When E. coli gets a hold of glucose, it's like us enjoying a delicious meal. But here's the magic part: E. coli doesn't just eat for fun. It uses glucose to create energy, the kind of energy that keeps it alive and helps it perform all its microscopic tasks.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_eat_breathe_love.add.label(
            """
            Chapter 2: Breathe
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'firebrick',
            font_size = 35
        )
        book_eat_breathe_love.add.label(
            """
            Breathing, Microbe-Style
            We breathe in oxygen from the air, but for E. coli and its microbe pals, it's a bit different. Some of these microorganisms love oxygen and use it to breathe, just like we do. It's like their version of taking a deep breath of fresh air.

            Breathing Without Oxygen
            But not all microbes are oxygen fans. Some are like rebels that can live without it. They have special powers, allowing them to thrive in places where there's no oxygen at all, like deep in the soil or even inside your digestive system.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_eat_breathe_love.add.label(
            """
            Chapter 3: Love
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0),
            background_color = 'white',
            font_color = 'firebrick',
            font_size = 35
        )
        book_eat_breathe_love.add.label(
            """
            Microbial Families
            Microbes might not have moms and dads, but they have their own way of growing their families. When they're happy and cozy in their environment, they start making lots and lots of baby microbes. When they're happy and the conditions are just right, they multiply.

            Influence of the Environment
            The environment plays a big role in how microbes grow and make babies. If it's too hot or too cold, or the conditions aren't just right, they might slow down or even not be able to grow. But when everything's perfect, they can multiply like crazy and fill their tiny world with new microbes!
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        book_eat_breathe_love.add.button('Back', self._close_back(book_eat_breathe_love), background_color=(70, 70, 70))
        book_eat_breathe_love.add.vertical_margin(20)
        return book_eat_breathe_love


    def _build_how_to_play(self):
        menu_how_to_play = pygame_menu.Menu('How to Play', 1280, 720,
                        onclose=self.toggle_menu,
                        theme=tutorial_theme)

        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Moving""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        menu_how_to_play.add.label(
            """
            Use arrows (up, down, left, righ) or WASD keys to move the character.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Interacting""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        menu_how_to_play.add.label(
            """
            Use ENTER key to open the dialogue when close to another character (scientists).

            Use ENTER key to open the simulation window when close to your desk.

            Use ENTER key to consult books when close to the library.

            Use ENTER key to take an apple from a tree ("An apple a day keeps the doctor away").

            Use ENTER key to try some coffee and see if it has some effect on you.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Buttons""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        menu_how_to_play.add.label(
            """
            Use the Mouse to click on the buttons of the dialogues.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.label(
            """Main Menu""",
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(100, 0),
            background_color = (60, 150, 140),
            font_color = 'white',
            font_size = 30,
            padding = (25,25,25,25)
        )
        menu_how_to_play.add.label(
            """
            Use M key to open the Main Menu to control the music/volume, save/exit the game and to see this tutorial again.
            """,
            max_char=-1,
            wordwrap=True,
            align=pygame_menu.locals.ALIGN_LEFT,
            margin=(0, 0)
        )
        menu_how_to_play.add.vertical_margin(50)
        menu_how_to_play.add.button('Back', self._close_back(menu_how_to_play), background_color=(70, 70, 70))
        menu_how_to_play.add.vertical_margin(50)
        return menu_how_to_play


    async def setup(self):
        while True:
            self._top_menu = self._build_top_menu()
            await run_menu(self._top_menu, self.display_surface)

            if self._pending_book is None:
                self._top_menu = None
                return

            book_id = self._pending_book
            self._pending_book = None
            book_menu = self._build_book(book_id)
            await run_menu(book_menu, self.display_surface)


    def on_button_click(self, value: str, text = None) -> None:
        if not text:
            print(f'Hello from {value}')
        else:
            print(f'Hello from {text} with {value}')



    def input(self):
        keys = pygame.key.get_pressed()
        self.timer.update()

        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()


    async def update(self):
        self.input()
        await self.setup()
