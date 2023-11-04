import json


class Colors(object):
    def __init__(self):
        self.populate_db('colors.json')

    def populate_db(self, filename):
        self.color_db = {}
        with open(filename) as f:
            colors = json.load(f)
        for h in colors:
            self.color_db[h['color']] = h

    def get_rgba(self, color):
        rgba = []
        color = color.lower()
        if color in self.color_db.keys():
            c = self.color_db[color]
            rgba.append(c['code']['rgba'])
            rgba.append(c['code']['hex'])
            return rgba
        else:
            return "error"

    def get_color(self, name):
        name = name.lower()
        if name in self.color_db.keys():
            return self.color_db[name]
        else:
            return None

    def get_list(self):
        colors_list = []
        for h in self.color_db.keys():
            colors_list.append(h)
        return colors_list
