![LabHero](LabHero.png)

# LabHero

A serious game that empowers non-bioinformaticians to learn how to use genome-scale metabolic models.

The game consists of simulating distinct environmental and genetic modifications of towards specific objectives. At each game level, the player is required to define a strategy that encompasses selecting a medium and/or choosing genetic modifications to achieve a certain result.


## Table of Contents

 1. [Introduction](#introduction)
 2. [Installation](#installation)
 3. [Game Story](#game-story)
 4. [Controls](#controls)
 5. [Playing LabHero](#playing-labhero)


## Introduction

This game was developed as a part of the master's thesis of Mónica Leiras "Development of a serious game to stimulate the learning of genome-scale metabolic modeling concepts" (MSc in Bioinformatics - University of Minho).

## Installation

The easiest way to play is to download the latest Windows build from the [Releases page](https://github.com/mleiras/LabHero/releases/latest).

  1. Download `LabHero-v0.1.0-windows.zip` from the latest release.
  2. Extract the zip anywhere on your machine.
  3. Double-click `LabHero.exe` to play.

Save files are written to `%APPDATA%\LabHero\` so they persist across game updates.

A macOS build is planned but not yet available.

<details>
  <summary>"Not Safe" Warning nstructions</summary><br>

When you try to open the application, Windows may show a message like:

> "Windows protected your PC"

This appears because the executable is not signed with a developer certificate. Signing software requires a paid certificate, which is standard for commercial projects but disproportionate for a small academic project.

To open the game the first time:

1. Click "More info" on the dialog box.
2. Click the "Run anyway" button.

You only need to do this once per machine.

</details>

<br>

<details>
<summary>Run from source</summary>
<br>

LabHero was tested with Python 3.10.11. Newer Python versions (3.13+) work but may need a workaround for the pinned MEWpy version.

1. Clone the repository:
    ```bash
    git clone
https://github.com/mleiras/LabHero.git
    cd LabHero
    ```
2. (Recommended) Set up a virtual environment:
    ```bash
    python3 -m venv .venv
    ```

    Windows:
    ```bash
    .venv\Scripts\activate
    ```

    macOS/Linux:
    ```bash
    source .venv/bin/activate
    ```

3. Install requirements:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the game:
    ```bash
    python3 LabHero.py
    ```

   **Note:** If `python3` doesn't work, try `python` instead.

</details>

A couple of small things to flag while you review:

- The "Releases page" link uses /releases/latest, which is GitHub's auto-redirect to whatever release is currently

</details>

## Game Story 

You’re a bioinformatician working at the University. You have a desk in the office of the Bioinformatics Department, where you can chat and socialize with your fellow bioinformaticians about the various projects they work on.

Your job is to help fellow researchers with the various problems they encounter during their projects. In the labs, you’ll find various missions in the field of systems biology and metabolic modeling. To complete these missions you’ll need to talk to the researchers and understand the challenges they face.

You will quickly find yourself having to carry out simulations with different environmental and genetic conditions, as suggested by the researchers, in order to obtain results more quickly. 

You can also study and learn more about systems biology and metabolic modeling with books you’ll find in your office library to help you complete the missions.

Welcome to LabHero!


## Controls

**Moving:**

Use arrows (up, down, left, righ) or WASD keys to move the character.

**Interacting:**

Use ENTER key to open the dialogue when close to another character.

Use ESCAPE key to close the dialogue with another character.

Use ENTER key to open the simulation window when close to your desk.

Use ENTER key to consult books when close to the library.

Use ENTER key to take an apple from a tree, because why not?

Use ENTER key to try some coffee and see if it has some effect on you.


**Buttons:**

Use the Mouse to click on the buttons of the dialogues and simulation menu.

**Main Menu:**

Use M key to open the Main Menu to change your name, control the music/volume, save/exit the game and to see this tutorial again.

## Playing LabHero

[![Playing LabHero Video](video_labhero.jpg)](https://www.youtube.com/watch?v=ky_Ov7gZDlg)
