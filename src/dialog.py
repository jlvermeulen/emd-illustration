from tkinter import messagebox
import tkinter.filedialog as filedialog

import settings

import os.path

def invalid_json_file(owner):
    messagebox.showerror('JSON file does not exist', 'Please give a path to an existing JSON file.', parent = owner)

def browse_json(owner):
    filename = filedialog.askopenfilename(initialdir = settings.get('last_opened_source_dir'), filetypes = [('JSON files', '*.json'), ('JSON files', '*.JSON')], parent = owner)
    if filename:
        settings.set('last_opened_source_dir', os.path.dirname(filename))
    return filename
