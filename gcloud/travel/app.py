from flask import Flask, request, render_template
from flask_restful import Resource, Api
# from travel_local import Travel
from travel_gcloud import Travel
import datetime

app = Flask(__name__,
            static_url_path='/static',
            static_folder='static')
travel_dao = Travel()

api = Api(app)
basePath = '/api/v1'


class TravelResoure(Resource):
    def post(self, user, data):
        user = user.lower()
        data = data.lower()
        try:
            datetime.date.fromisoformat(data)
        except ValueError:
            return 'Incorrect data format', 400
        traveldata = request.json
        departure = traveldata['from']
        if len(departure) != 3:
            return 'Incorrect departure format', 400
        arrive = traveldata['to']
        if len(arrive) != 3:
            return 'Incorrect arrive format', 400
        travel = travel_dao.get_travel(user, data)
        if travel is None:
            travel_dao.add_travel(user, data, departure, arrive)
            return None, 201
        else:
            return None, 409

    def get(self, user, data):
        user = user.lower()
        data = data.lower()
        try:
            datetime.date.fromisoformat(data)
        except ValueError:
            return 'Incorrect data format', 404
        travel = travel_dao.get_travel(user, data)
        if travel is not None:
            return travel, 200
        else:
            return None, 404


class TravelList(Resource):
    def get(self, user):
        user = user.lower()
        travelMate = travel_dao.get_list(user)
        if travelMate:
            return travelMate, 200
        else:
            return None, 404


api.add_resource(TravelList, f'{basePath}/travel/<string:user>')
api.add_resource(TravelResoure, f'{basePath}/travel/<string:user>/<string:data>')


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/travel/<user>')
def get_travelmates(user):
    if user != "":
        travelmates = travel_dao.get_list(user)
        route = travel_dao.get_list_route(user)
        return render_template("mates.html", route=route, travelmates=travelmates)
    else:
        return None, 404


if __name__ == '__main__':
    app.run()
