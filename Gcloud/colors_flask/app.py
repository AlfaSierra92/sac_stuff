from flask import Flask, render_template, request
# from colors_local import Colors
from colors_gcp import Colors

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
colors_dao = Colors()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', path=request.path), 404


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
