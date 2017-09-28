import tkinter as tk

import os, os.path, argparse

settings =  {
                'main_window_geometry': '1280x720+100+100',
                'last_opened_source_dir': './',
                'export_file': './solution.json'
            }

def load():
    if os.path.isfile('settings.conf'):
        with open('settings.conf', 'r') as conf:
            for line in conf.read().splitlines():
                parts = line.strip().split('=', 1)
                if parts[0] in settings:
                    settings[parts[0]] = parts[1]

def save():
    with open('settings.conf', 'w') as conf:
        for key, value in settings.items():
            conf.write('{}={}\n'.format(key, value))

def get(name):
    return settings.get(name)

def set(name, value):
    settings[name] = value

parser = argparse.ArgumentParser(description = 'Bibliography management utility.', prog = 'emd-illustrator')
parser.add_argument('--data-dir', default = '.', help = 'The directory in which the settings are stored.')
parser.add_argument('--version', action = 'version', version = '%(prog)s 0.1')

arguments = parser.parse_args()
os.chdir(arguments.data_dir)
