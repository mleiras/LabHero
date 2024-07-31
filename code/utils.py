import sys
import os

def get_resource_path(relative_path):
    """ Get the absolute path to the resource"""
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
