import json


class Travel(object):
    def __init__(self):
        self.travel_db = {}

    def add_travel(self, name, date, departure, arrive):
        self.travel_db[name+date] = {'name': name,
                                     'date': date,
                                     'departure': departure,
                                     'arrive': arrive
                                     }

    def get_travel(self, name, date):
        travel = []
        if name+date in self.travel_db.keys():
            t = self.travel_db[name+date]
            travel.append(t['departure'])
            travel.append(t['arrive'])
            return travel
        else:
            return None

    def get_list(self, name):
        travelmates = []
        for key in self.travel_db.keys():  # prelevo la key
            if name in key:  # e controllo se il nome è contenuto nella key
                t = self.travel_db[key]
                for x in self.travel_db.keys():  # scorro tutti gli altri viaggiatori
                    if self.travel_db[x]['date'] == t['date'] and self.travel_db[x]['departure'] == t['departure'] and self.travel_db[x]['arrive'] == t['arrive']:
                        # if self.travel_db[x]['name']+self.travel_db[x]['date'] != x:
                            # necessario altrimenti mi ritorna il nome del viaggiatore che richiede le corrispondenze
                        travelmates.append(self.travel_db[x]['name'])
        return travelmates
