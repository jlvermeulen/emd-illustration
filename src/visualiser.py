import tkinter as tk
from PIL import Image, ImageDraw, ImageTk
import math

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

    def draw_flow_polygons(self, polygons):
        bboxes = []
        polys  = []
        bbox = [float('inf'), float('inf'), 0, 0]

        for poly in polygons:
            minx, miny, maxx, maxy = float('inf'), float('inf'), 0, 0
            for v in poly.vertices:
                minx = math.floor(min(minx, v.x))
                miny = math.floor(min(miny, v.y))
                maxx = math.ceil(max(maxx, v.x))
                maxy = math.ceil(max(maxy, v.y))

            bboxes.append((minx, miny, maxx, maxy))
            bbox[0] = math.floor(min(bbox[0], minx))
            bbox[1] = math.floor(min(bbox[1], miny))
            bbox[2] = math.ceil(max(bbox[2], maxx))
            bbox[3] = math.ceil(max(bbox[3], maxy))

            poly_image = Image.new('RGBA', (maxx - minx, maxy - miny))
            poly_draw  = ImageDraw.Draw(poly_image)
            poly_draw.polygon([(v.x - minx, v.y - miny) for v in poly.vertices], fill = (128, 128, 128, 64), outline = (0, 0, 0, 255))

            polys.append(poly_image)

        composite = Image.new('RGBA', (bbox[2] - bbox[0], bbox[3] - bbox[1]), (255, 255, 255, 255))
        for i in range(len(polys)):
            composite.paste(polys[i], (bboxes[i][0] - bbox[0], bboxes[i][1] - bbox[1]), mask = polys[i])

        self.image = ImageTk.PhotoImage(composite)
        self.canvas.create_image(bbox[0], bbox[1], anchor = 'nw', image = self.image)

    def draw_flow(self, flow):
        if isinstance(flow, geometry.Segment):
            self.draw_flow_segment(flow.start, flow.end)
        elif isinstance(flow, geometry.Polygon):
            self.draw_flow_polygon(flow.vertices)

    def draw(self, obj, issource):
        if isinstance(obj, geometry.Point):
            self.draw_point(obj, issource)
        elif isinstance(obj, geometry.Segment):
            self.draw_segment(obj, issource)

    def draw_all(self, data):
        self.clear()
        if 'flows' in data:
            if all(isinstance(x, geometry.Polygon) for x in data['flows']):
                self.draw_flow_polygons(data['flows'])
            else:
                for flow in data['flows']:
                    self.draw_flow(flow)
        if 'sources' in data:
            for source in data['sources']:
                self.draw(source, True)
        if 'sinks' in data:
            for sink in data['sinks']:
                self.draw(sink, False)

    def clear(self):
        self.canvas.delete('all')
