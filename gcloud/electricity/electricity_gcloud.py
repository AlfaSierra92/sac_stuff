import json
from google.cloud import firestore
from datetime import datetime


class Electricity(object):
    def __init__(self):
        self.db = firestore.Client()  # connessione con db firestore

    def clean(self):
        # raccolta -> documenti -> campi
        consumi = self.db.collection('consumi').get()  # fetching della raccolta consumi

        for x in consumi:  # scorrimento di tutti i documenti all'interno della raccolta
            print(f"Cleaning: {x.id}")
            try:
                self.db.collection('consumi').document(x.id).delete()
            except Exception as e:
                print(f"Error deleting document {x.id}: {e}")

    def add_consumi(self, date, value):
        # consumi_ref = self.db.collection('consumi')
        h = {
            'date': date,
            'value': value
        }
        # consumi_ref.document(date).set(h)
        self.db.collection('consumi').document(date).set(h)  # aggiungo documenti con campi

    def get_lettura_consumi(self, date):
        consumi = []
        # consumi_ref = self.db.collection('consumi')
        # consumi_doc = consumi_ref.document(date).get()
        consumi_doc = self.db.collection('consumi').document(date).get()  # fetching del documento

        if consumi_doc.exists:
            consumi.append(consumi_doc.get("value"))
            consumi.append(False)
            return consumi
        else:
            valore = 0
            lettura = []
            data_list = []
            test = len(self.db.collection('consumi').get())  # controllo il numero di documenti nella raccolta
            if test >= 2:
                # query = self.db.collection('consumi').order_by("date", direction=firestore.Query.DESCENDING).limit(2)
                # docs = query.get()
                docs = self.db.collection('consumi').order_by("date",
                                                              direction=firestore.Query.DESCENDING).limit(2).get()
                for x in docs:
                    valore = valore + x.get("value")
                    lettura.append(x.get("value"))
                    data_list.append(datetime.strptime(x.get("date"), '%d-%m-%Y'))
                diff10 = (data_list[1] - data_list[0])
                diffnow_1 = datetime.strptime(date, '%d-%m-%Y') - data_list[1]
                valore = lettura[1] + ((lettura[1] - lettura[0]) / (diff10.total_seconds())) * (
                            diffnow_1.total_seconds())
                # valore = valore / 2

            else:
                # query = self.db.collection('consumi').order_by("date", direction=firestore.Query.DESCENDING).limit(1)
                # docs = query.get()
                docs = self.db.collection('consumi').order_by("date",
                                                              direction=firestore.Query.DESCENDING).limit(1).get()
                for x in docs:
                    valore = valore + x.get("value")
                # valore = valore / 2
            consumi.append(valore)
            consumi.append(True)
            return consumi
