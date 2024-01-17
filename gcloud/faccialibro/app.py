from flask import Flask, request, render_template
from flask_restful import Resource, Api
from faccialibro_gcloud import FaccialibroGcloud
from wtforms import Form, IntegerField, StringField, validators, SubmitField

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
faccialibro_dao = FaccialibroGcloud()

api = Api(app)
basePath = '/api/v1'


class Faceform(Form):
    label = StringField('Message', [validators.length(max=100)])
    topic = StringField('topic', [validators.length(max=100)])
    submit = SubmitField('Submit')


class Struct:
    def __init__(self, **entries):
        self.__dict__.update(entries)


class FacciaLibroChirps(Resource):
    def post(self):
        message = request.json
        if 1 <= len(message) <= 100:
            h = faccialibro_dao.add_chirps(message)
            return h, 201
        else:
            return None, 400


class FacciaLibroChirpsGet(Resource):
    def get(self, ids):
        h = faccialibro_dao.get_chirps(ids)
        if h is not None:
            return h, 200
        else:
            return None, 404


class FacciaLibroTopics(Resource):
    def get(self, topic):
        h = faccialibro_dao.get_topics(topic)
        if h is not None:
            return h, 200
        else:
            return None, 404


class FacciaLibroClean(Resource):
    def post(self):
        faccialibro_dao.clean()
        return None, 200


# perchè uso due endpoint separati per chirp? Perchè cambiano i parametri passati nella url:
api.add_resource(FacciaLibroChirps, f'{basePath}/chirp')  # POST con payload json
api.add_resource(FacciaLibroChirpsGet, f'{basePath}/chirp/<string:ids>')  # GET (please url-encode id)
api.add_resource(FacciaLibroTopics, f'{basePath}/topic/<string:topic>')
api.add_resource(FacciaLibroClean, f'{basePath}/clean')


@app.route('/', methods=['GET', 'POST'])
def hello_world():  # put application's code here
    c = {'Message': ''}
    if request.method == 'POST':
        cform = Faceform(request.form)
        if cform.label.data != "":
            faccialibro_dao.add_chirps(cform.label.data)
            return 'MEssaggio inserito!'
        else:
            messages = faccialibro_dao.get_topics(cform.topic.data)
            return messages
    if request.method == 'GET':
        cform = Faceform(obj=Struct(**c))
        return render_template('index.html', name=c['Message'], form=cform)


if __name__ == '__main__':
    app.run()
