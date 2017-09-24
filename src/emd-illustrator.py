#! /usr/bin/env python3

from tkinter import ttk
import tkinter as tk

import settings, loader
from geometry import *
from solver import solver
from visualiser import Visualiser

import os.path, cProfile

class MainWindow(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

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
        tk.Grid.rowconfigure(self.sidebar, 7, weight = 1)

        tk.Button(self.sidebar, text = 'Load file', command = self.load_file).grid(row = 0, column = 0, sticky = 'news')

        tk.Label(self.sidebar, text = 'Draw').grid(row = 1, column = 0, sticky = 'news', pady = (10, 0))
        self.category = tk.StringVar()
        self.type = tk.StringVar()

        categories = ['source', 'sink']
        types = ['point', 'segment']
        for i in range(2):
            button1 = tk.Radiobutton(self.sidebar, indicatoron = 0, text = categories[i].title(), variable = self.category, value = categories[i])
            button1.grid(row = i + 2, column = 0, sticky = 'news', ipadx = 2, ipady = 2, pady = (0, 0 if i == 0 else 10))

            button2 = tk.Radiobutton(self.sidebar, indicatoron = 0, text = types[i].title(), variable = self.type, value = types[i])
            button2.grid(row = i + 4, column = 0, sticky = 'news', ipadx = 2, ipady = 2, pady = (0, 0 if i == 0 else 10))

            if i == 0:
                button1.select()
                button1.invoke()
                button2.select()
                button2.invoke()

        tk.Label(self.sidebar, text = 'Options').grid(row = 6, column = 0, sticky = 'news')

        tk.Button(self.sidebar, text = 'Solve', command = self.solve).grid(row = 8, column = 0, sticky = 'news')

    def destroy(self):
        settings.set('main_window_geometry', self._nametowidget(self.winfo_parent()).geometry())
        settings.save()
        super().destroy()

    def load_file(self):
        data = loader.load('test.json')
        for source in data['sources']:
            self.visualiser.draw(source, True)
        for sink in data['sinks']:
            self.visualiser.draw(sink, False)

    def solve(self):
        point = Point(10, 10)
        segment = Segment(Point(100, 30), Point(70, 80))
        #solver.solve(point, segment)

        self.visualiser.draw_point(point, True)
        self.visualiser.draw_segment(segment, False)
        self.visualiser.draw_flow(point, Point(85, 55))

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
