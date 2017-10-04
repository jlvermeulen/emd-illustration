#! /usr/bin/env python3

from tkinter import ttk
import tkinter as tk

import settings, solver, loader, exporter, dialog
from geometry import *
from visualiser import Visualiser

import os.path, cProfile, sys

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.category = tk.StringVar()
        self.type = tk.StringVar()

        self.parent.title('emd-illustrator')
        self.pack(fill = 'both', expand = 1, padx = 5, pady = 5)

        tk.Grid.columnconfigure(self, 0, weight = 1)
        tk.Grid.columnconfigure(self, 1, minsize = 100)
        tk.Grid.rowconfigure(self, 0, weight = 1)

        self.visualiser = Visualiser(self)
        self.visualiser.grid(row = 0, column = 0, sticky = 'news', padx = (0, 5))

        self.sidebar = tk.Frame(self)
        self.sidebar.grid(row = 0, column = 1, sticky = 'news')
        tk.Grid.columnconfigure(self.sidebar, 0, weight = 1)
        tk.Grid.rowconfigure(self.sidebar, 11, weight = 1)

        load_button     = tk.Button(self.sidebar, text = 'Load file', command = self.load_file)
        separator1      = ttk.Separator(self.sidebar)
        draw_label      = tk.Label(self.sidebar, text = 'Draw')
        toggles         = tk.Frame(self.sidebar)
        separator2      = ttk.Separator(self.sidebar)
        options_label   = tk.Label(self.sidebar, text = 'Options')
        subdivisions    = tk.Frame(self.sidebar)
        separator3      = ttk.Separator(self.sidebar)
        solve_button    = tk.Button(self.sidebar, text = 'Solve', command = self.solve)
        export_button   = tk.Button(self.sidebar, text = 'Export', command = self.export)
        clear_button    = tk.Button(self.sidebar, text = 'Clear', command = self.visualiser.clear)
        self.cost_label = tk.Label(self.sidebar)

        load_button     .grid(row = 0, column = 0, sticky = 'news')
        separator1      .grid(row = 1, column = 0, sticky = 'news', pady = 5)
        draw_label      .grid(row = 2, column = 0, sticky = 'news', pady = (0, 5))
        toggles         .grid(row = 3, column = 0, sticky = 'news')
        separator2      .grid(row = 4, column = 0, sticky = 'news', pady = 5)
        options_label   .grid(row = 5, column = 0, sticky = 'news', pady = (0, 5))
        subdivisions    .grid(row = 6, column = 0, sticky = 'news')
        separator3      .grid(row = 7, column = 0, sticky = 'news', pady = 5)
        solve_button    .grid(row = 8, column = 0, sticky = 'news')
        export_button   .grid(row = 9, column = 0, sticky = 'news')
        clear_button    .grid(row = 10, column = 0, sticky = 'news')
        self.cost_label .grid(row = 11, column = 0, sticky = 'ws')

        tk.Grid.columnconfigure(toggles, 0, weight = 1, uniform = 'toggles')
        tk.Grid.columnconfigure(toggles, 1, weight = 1, uniform = 'toggles')

        categories = ['source', 'sink']
        types = ['point', 'segment']
        for i in range(2):
            button1 = tk.Radiobutton(toggles, indicatoron = 0, text = categories[i].title(), variable = self.category, value = categories[i])
            button2 = tk.Radiobutton(toggles, indicatoron = 0, text = types[i].title(), variable = self.type, value = types[i])

            button1.grid(row = 0, column = (i + 1) // 2, sticky = 'news', ipadx = 4, ipady = 4)
            button2.grid(row = 1, column = (i + 1) // 2, sticky = 'news', ipadx = 4, ipady = 4)

            if i == 0:
                button1.select()
                button1.invoke()
                button2.select()
                button2.invoke()

        subdivions_label        = tk.Label(subdivisions, text = 'Subdivisions:')
        self.subdivions_entry   = tk.Spinbox(subdivisions, from_ = 0, to = 1000, width = 5)

        subdivions_label        .pack(side = 'left')
        self.subdivions_entry   .pack(side = 'left')


    def destroy(self):
        settings.set('main_window_geometry', self._nametowidget(self.winfo_parent()).geometry())
        settings.save()
        super().destroy()

    def load_file(self):
        filename = dialog.browse_json(self)
        if not filename:
            return

        self.data = loader.load(filename)
        if len(self.data['sources']) != len(self.data['sinks']):
            print('Warning: number of sources and sinks not equal, this is currently not supported.')

        self.visualiser.draw_all(self.data)
        self.show_cost(self.data)

    def solve(self):
        if not hasattr(self, 'data'):
            dialog.no_data(self)
            return

        self.solution = solver.solve(self.data, int(self.subdivions_entry.get()))

        self.visualiser.draw_all(self.solution)
        self.show_cost(self.solution)

        if len(self.data['sources']) == 1 and len(self.data['sinks']) == 1:
            split = supporting_line_intersection(self.data['sources'][0], self.data['sinks'][0])
            if not split:
                return

            print(split)

            sides = ''
            current, last_left, last_right, left, right = 0, -1, -1, 0, 0
            for flow in sorted(self.solution['flows'], key = lambda x: (x.start - split).length_squared()):
                if flow.end <= split:
                    left += 1
                    last_left = current
                    sides += 'l'
                else:
                    right += 1
                    last_right = current
                    sides += 'r'
                current += 1

            print(sides)
            print('left: {}, right: {}, last_left: {}, last_right: {}'.format(left, right, last_left, last_right))
            sys.stdout.flush()

    def export(self):
        if not hasattr(self, 'solution'):
            dialog.no_data(self)
            return

        filename = dialog.browse_export(self)
        if filename:
            exporter.export(self.solution, filename)

    def show_cost(self, solution):
        self.cost_label.config(text = 'Cost: {:g}'.format(solution['cost'] if 'cost' in solution else 0))

def main():
    root = tk.Tk()

    settings.load()
    root.geometry(settings.get('main_window_geometry'))

    app = MainWindow(root)

    root.mainloop()

profile = False
if __name__ == '__main__':
    if profile:
        cProfile.run('main()')
    else:
        main()
