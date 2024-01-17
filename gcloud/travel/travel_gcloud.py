import json
from google.cloud import firestore
from datetime import datetime

class Travel(object):
    def __init__(self):
        self.db = firestore.Client()

    def add_travel(self, name, date, departure, arrive):
        travel_ref = self.db.collection('travel')
        h = {'name': name,
             'date': date,
             'departure': departure,
             'arrive': arrive
             }
        travel_ref.document(name+date).set(h)

    def get_travel(self, name, date):
        travel = []
        name = name.lower()
        travel_doc = self.db.collection('travel').document(name + date).get()

        if travel_doc.exists:
            travel.append(travel_doc.get("departure"))
            travel.append(travel_doc.get("arrive"))
            return travel
        else:
            return None

    def get_list(self, name):
        travelmates = []

        # forse il .get() lo devi fare fuori dai costrutti if e for ???
        travel_documents = self.db.collection('travel').get()

        for doc in travel_documents:
            if name.lower() in doc.get("name"):
                for x in travel_documents:
                    data1 = datetime.strptime(x.get("date"), "%Y-%m-%d")
                    data2 = datetime.strptime(doc.get("date"), "%Y-%m-%d")
                    diff = data1-data2
                    if (
                            (data1 == data2 or abs(diff.days) <= 1)
                            and x.get("departure") == doc.get("departure")
                            and x.get("arrive") == doc.get("arrive")):
                        travelmates.append(x.get("name"))
        return travelmates

    def get_list_route(self, name):
        travelmates = []
        departure = ""
        arrive = ""
        # forse il .get() lo devi fare fuori dai costrutti if e for ???
        travel_documents = self.db.collection('travel').get()

        for doc in travel_documents:
            if name.lower() in doc.get("name"):
                for x in travel_documents:
                    data1 = datetime.strptime(x.get("date"), "%Y-%m-%d")
                    data2 = datetime.strptime(doc.get("date"), "%Y-%m-%d")
                    diff = data1-data2
                    if (
                            (data1 == data2 or abs(diff.days) <= 1)
                            and x.get("departure") == doc.get("departure")
                            and x.get("arrive") == doc.get("arrive")):
                        departure = x.get("departure")
                        arrive = x.get("arrive")
        travelmates.append(departure)
        travelmates.append(arrive)
        return travelmates
