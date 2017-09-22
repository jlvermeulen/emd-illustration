#! /usr/bin/env python3

from tkinter import ttk
import tkinter as tk

import settings
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
        tk.Grid.rowconfigure(self, 0, weight = 1)

        self.sidebar = tk.Frame(self)
        self.sidebar.grid(row = 0, column = 1, sticky = 'news')
        tk.Grid.rowconfigure(self.sidebar, 5, weight = 1)

        tk.Label(self.sidebar, text = 'Mode').grid(row = 0, column = 0)
        self.mode = tk.StringVar()

        self.mode_options = {
                                'point-point': Visualiser(self),
                                'point-segment': Visualiser(self),
                                'segment-segment': Visualiser(self)
                            }

        i = 1
        for name, value in self.mode_options.items():
            button = tk.Radiobutton(self.sidebar, indicatoron = 0, text = name.title(), variable = self.mode, value = name, command = self.switch_mode)
            button.grid(row = i, column = 0, sticky = 'news', ipadx = 2, ipady = 2)

            value.grid(row = 0, column = 0, sticky = 'news', padx = (0, 5))

            if i == 2:
                button.select()
                button.invoke()
            i += 1

        tk.Label(self.sidebar, text = 'Options').grid(row = 4, column = 0, pady = (10, 0))

        tk.Button(self.sidebar, text = 'Solve', command = self.solve).grid(row = 6, column = 0, sticky = 'news')

    def destroy(self):
        settings.set('main_window_geometry', self._nametowidget(self.winfo_parent()).geometry())
        settings.save()
        super().destroy()

    def switch_mode(self):
        self.mode_options[self.mode.get()].tkraise()
        settings.set('mode', self.mode.get())

    def solve(self):
        mode = self.mode.get()
        if mode == 'point-segment':
            point = Point(10, 10)
            segment = Segment(Point(100, 30), Point(70, 80))
            solver.solve_point_segment(point, segment)

            visualiser = self.mode_options[mode]
            visualiser.draw_point(point)
            visualiser.draw_segment(segment)
            visualiser.draw_flow(point, Point(85, 55))

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
