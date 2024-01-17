from flask import Flask, request, render_template
from flask_restful import Resource, Api
from electricity_gcloud import Electricity
from datetime import datetime

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
electricity_dao = Electricity()

api = Api(app)
basePath = '/api/v1'


class ElectricityResource(Resource):
    def post(self, data):
        try:
            datetime.strptime(data, '%d-%m-%Y')
        except ValueError:
            return None, 400
        lettura_req = request.json
        if not "value" in lettura_req:
            return None, 400
        lettura = lettura_req["value"]
        if isinstance(lettura, str) is True:
            return None, 400
        if lettura <= 0:
            return None, 400
        old_value = electricity_dao.get_lettura_consumi(data)
        if old_value[1] is not True:  # la funzione ritorna un valore anche se non esiste la lettura
            return None, 409
        electricity_dao.add_consumi(data, lettura)
        h = {
            'isInterpolated': False,
            'value': lettura
        }
        return h, 201

    def get(self, data):
        try:
            # datetime.date.fromisoformat(data)
            datetime.strptime(data, '%d-%m-%Y')
        except ValueError:
            return None, 400
        value = electricity_dao.get_lettura_consumi(data)
        if value is not None:
            h = {
                'isInterpolated': value[1],
                'value': int(value[0])
            }
            return h, 200
        else:
            return None, 400


class ElectricityClean(Resource):
    def get(self):
        electricity_dao.clean()


api.add_resource(ElectricityResource, f'{basePath}/consumi/<string:data>')
api.add_resource(ElectricityClean, f'{basePath}/clean')
# api.add_resource(ElectricityResource, f'{basePath}/travel/<string:user>/<string:data>')


def date_from_str(d):
    try:
        return datetime.strptime(d, '%d-%m-%Y')
    except:
        return None


def str_from_date(d):
    return d.strftime('%d-%m-%Y')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
