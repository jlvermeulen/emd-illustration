import tkinter as tk

import geometry

class Visualiser(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.canvas = tk.Canvas(self, bg = 'white')
        self.canvas.pack(fill = 'both', expand = 1)

    def draw_point_(self, point, r, colour):
        self.canvas.create_oval(point.x - r, point.y - r, point.x + r, point.y + r, outline = colour, fill = colour)

    def draw_point(self, point, issource):
        self.draw_point_(point, 2, 'red' if issource else 'blue')

    def draw_segment_(self, segment, r, colour):
        self.canvas.create_line(segment.start.x, segment.start.y, segment.end.x, segment.end.y, fill = colour)
        if r > 0:
            self.draw_point_(segment.start, r, colour)
            self.draw_point_(segment.end, r, colour)

    def draw_segment(self, segment, issource):
        self.draw_segment_(segment, 1, 'red' if issource else 'blue')

    def draw_flow_segment(self, source, sink):
        self.draw_segment_(geometry.Segment(source, sink), 0, 'black')

    def draw_flow_polygon(self, vertices):
        coords = []
        for vert in vertices:
            coords.append(vert.x)
            coords.append(vert.y)

        self.canvas.create_polygon(coords, fill = 'grey', outline = 'black')

    def draw(self, obj, issource):
        if isinstance(obj, geometry.Point):
            self.draw_point(obj, issource)
        elif isinstance(obj, geometry.Segment):
            self.draw_segment(obj, issource)

    def draw_all(self, data):
        self.clear()
        if 'flows' in data:
            for flow in data['flows']:
                if isinstance(flow, geometry.Segment):
                    self.draw_flow_segment(flow.start, flow.end)
                elif isinstance(flow, geometry.Polygon):
                    self.draw_flow_polygon(flow.vertices)
        if 'sources' in data:
            for source in data['sources']:
                self.draw(source, True)
        if 'sinks' in data:
            for sink in data['sinks']:
                self.draw(sink, False)

    def clear(self):
        self.canvas.delete('all')
