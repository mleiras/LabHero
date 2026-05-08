import sys
import os

APP_NAME = 'LabHero'

def get_resource_path(relative_path):
    """ Get the absolute path to a read-only resource bundled with the game."""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def get_save_path(filename):
    """Return the absolute path for a user-writable save file.

    Saves live outside the bundle so they survive reinstall and work in
    PyInstaller --onefile builds, where the bundle dir is a temp folder.
    """
    if sys.platform == 'win32':
        base = os.path.join(os.environ.get('APPDATA', os.path.expanduser('~')), APP_NAME)
    elif sys.platform == 'darwin':
        base = os.path.join(os.path.expanduser('~'), 'Library', 'Application Support', APP_NAME)
    else:
        xdg = os.environ.get('XDG_DATA_HOME')
        base = os.path.join(xdg, APP_NAME) if xdg else os.path.join(os.path.expanduser('~'), '.local', 'share', APP_NAME)
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, filename)
