from flask import Flask, render_template, request
from flask_restful import Resource, Api
from wtforms import Form, IntegerField, StringField, validators, SubmitField
from colors_local import Colors

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
colors_dao = Colors()

# rest stuff
api = Api(app)
basePath = '/api/v1'


class ColorList(Resource):
    def get(self):
        return colors_dao.get_list(), 200


class ColorsResource(Resource):
    def get(self, colorname):
        colorname = colorname.lower()
        rgba = colors_dao.get_rgba(colorname)
        if rgba is None:
            return None, 404
        else:
            return rgba

    # aggiungi colore
    def post(self, colorname):
        colorname = colorname.lower()
        # r = colors_dao.get_rgba(colorname)
        if not colors_dao.get_color(colorname) is None:  # check if it exists
            return None, 409  # if it exists go out
        colordata = request.json
        if colorname is None or colordata['red'] > 255 or colordata['green'] > 255 or colordata['blue'] > 255:
            return None, 400
        colors_dao.add_color(colorname, colordata['red'], colordata['green'], colordata['blue'])
        return None, 201

    # aggiorna colore
    def put(self, colorname):
        colorname = colorname.lower()
        if colors_dao.get_color(colorname) is None:  # check if it exists
            return None, 400  # if exists go out
        colordata = request.json
        if colorname is None or colordata['red'] > 255 or colordata['green'] > 255 or colordata['blue'] > 255:
            return None, 400
        colors_dao.add_color(colorname, colordata['red'], colordata['green'], colordata['blue'])
        return None, 201

    # rimuovi colore
    def delete(self, colorname):
        if colors_dao.get_color(colorname) is None:  # check if it exists
            return None, 400  # if it doesn't exist go out
        colors_dao.del_color(colorname)
        return None, 201


api.add_resource(ColorList, f'{basePath}/colors/')
api.add_resource(ColorsResource, f'{basePath}/colors/<string:colorname>')


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


if __name__ == '__main__':
    app.run()