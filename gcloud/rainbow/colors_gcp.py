import json
from google.cloud import firestore


class Colors(object):
    def __init__(self):
        self.db = firestore.Client()
        self.populate_db('colors.json')

    def add_color(self, color_name, red, green, blue):
        rgbcode = '#%02X%02X%02X' % (red, green, blue)
        colors_ref = self.db.collection('colors')
        h = {'color': color_name,
             'category': 'hue',
             'type': 'primary',
             'code': {
                 'rgba': [red, green, blue, 1],
                 'hex': rgbcode
             }}
        colors_ref.document(h['color']).set(h)

    def del_color(self, color_name):
        self.db.collection('colors').document(color_name).delete()

    def populate_db(self, filename):
        # self.color_db = {}
        colors_ref = self.db.collection('colors')  # istanzio una raccolta chiamata colors
        with open(filename) as f:
            colors = json.load(f)
        for h in colors:
            colors_ref.document(h['color']).set(h)  # nella raccolta colors ci metto i vari colori
            # (sarebbero i documenti chiamati col nome dei "keys")

    def get_rgba(self, color):
        rgba = []
        color = color.lower()
        # if color in self.color_db.keys():
        if color != "":
            c = self.db.collection('colors').document(color).get()
            rgba.append(c.get("code.rgba"))
            rgba.append(c.get("code.hex"))
            return rgba
        else:
            return "error"

    def get_color(self, name):
        name = name.lower()
        if name in self.db.collection('colors').get():
            return name
        else:
            return "error"

    def get_list(self):
        colors_list = []
        for h in self.db.collection('colors').stream():
            colors_list.append(h.id)
        return colors_list
