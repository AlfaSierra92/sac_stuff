import json
from google.cloud import firestore


class Colors(object):
    def __init__(self):
        self.db = firestore.Client()
        self.populate_db('colors.json')

    def populate_db(self, filename):
        # self.color_db = {}
        colors_ref = self.db.collection('colors')  # istanzio una raccolta chiamata colors
        with open(filename) as f:
            colors = json.load(f)
        for h in colors:
            # self.color_db[h['color']] = h
            colors_ref.document(h['color']).set(h)  # nella raccolta colors ci metto i vari colori
            # (sarebbero i documenti chiamati col nome dei "keys")

    def get_rgba(self, color):
        rgba = []
        color = color.lower()
        # if color in self.color_db.keys():
        if color != "":
            # c = self.color_db[color]
            c = self.db.collection('colors').document(color).get()
            # rgba.append(c['code']['rgba'])
            rgba.append(c.get("code.rgba"))
            # rgba.append(c['code']['hex'])
            rgba.append(c.get("code.hex"))
            return rgba
        else:
            return "error"

    def get_color(self, name):
        name = name.lower()
        # if name in self.color_db.keys():
        #    return self.color_db[name]
        # else:
        #    return None
        if name in self.db.collection('colors').get():
            return name
        else:
            return "error"

    def get_list(self):
        colors_list = []
        # for h in self.color_db.keys():
        #    colors_list.append(h)
        for h in self.db.collection('colors').stream():
            colors_list.append(h.id)
        return colors_list
