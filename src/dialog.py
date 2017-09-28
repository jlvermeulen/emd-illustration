from tkinter import messagebox
import tkinter.filedialog as filedialog

import settings

import os.path

json_filetypes = [('JSON files', '*.json'), ('JSON files', '*.JSON')]

def invalid_json_file(owner):
    messagebox.showerror('JSON file does not exist', 'Please give a path to an existing JSON file.', parent = owner)

def empty_export(owner):
    messagebox.showerror('Nothing to export', 'Please generate some data to export.', parent = owner)

def browse_json(owner):
    filename = filedialog.askopenfilename(initialdir = settings.get('last_opened_source_dir'), filetypes = json_filetypes, parent = owner)
    if filename:
        settings.set('last_opened_source_dir', os.path.dirname(filename))
    return filename

def browse_export(owner):
    last = settings.get('export_file')
    filename = filedialog.asksaveasfilename(initialdir = os.path.dirname(last), initialfile = os.path.basename(last), defaultextension = '.json', filetypes = json_filetypes, parent = owner)
    if filename:
        settings.set('export_file', filename)
    return filename
