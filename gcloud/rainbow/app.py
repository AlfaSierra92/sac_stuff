from flask import Flask, render_template, request
from flask_restful import Resource, Api
from wtforms import Form, IntegerField, StringField, validators, SubmitField
from colors_local import Colors
# from colors_gcp import Colors

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


class Colorform(Form):
    label = StringField('Name', [validators.length(max=10)])
    red = IntegerField('Red', [validators.NumberRange(min=0, max=255)])
    green = IntegerField('Green', [validators.NumberRange(min=0, max=255)])
    blue = IntegerField('Blue', [validators.NumberRange(min=0, max=255)])
    submit = SubmitField('Submit')


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404


@app.route('/insert', methods=['GET', 'POST'])
def insert_color():
    c = {'label': 'name', 'red': 0, 'green': 0, 'blue': 0}
    if request.method == 'POST':
        cform = Colorform(request.form)
        colors_dao.add_color(cform.label.data, cform.red.data, cform.green.data, cform.blue.data)
        c = {'label': cform.label.data, 'red': cform.red.data, 'green': cform.green.data, 'blue': cform.blue.data}
    if request.method == 'GET':
        cform = Colorform(obj=Struct(**c))
    rgbcode = '#%02X%02X%02X' % (c['red'], c['green'], c['blue'])
    return render_template('insert.html', name=c['label'], rgb=rgbcode, red=c['red'], green=c['green'], blue=c['blue'], form=cform)


@app.route('/colors/<color>')
def get_color(color):
    rgba = colors_dao.get_rgba(color)
    if rgba != "error":
        return render_template('color.html', color=color, rgba=rgba)
    else:
        return render_template('404.html', path=request.path), 404


@app.route('/')
def hello_world():  # put application's code here
    color_list = colors_dao.get_list()
    return render_template('color.html', color="", color_list=color_list)


if __name__ == '__main__':
    app.run()
