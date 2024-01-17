from google.cloud import firestore
import re
import datetime
from google.cloud import pubsub_v1

# questa parte qui per il punto 3
publisher = pubsub_v1.PublisherClient()
# topic_path = publisher.topic_path('travel2-405610', 'hashtags')


class FaccialibroGcloud(object):
    def __init__(self):
        self.db = firestore.Client()
        self.counter = 0

    def get_hashtags(msg: str) -> list:
        return re.findall('(#\w+)', msg, re.DOTALL)

    def clean(self):
        msgs = self.db.collection('messages').get()
        hashes = self.db.collection('hashtags').get()

        for x in msgs:
            print(f"Cleaning: {x.id}")
            try:
                self.db.collection('messages').document(x.id).delete()
            except Exception as e:
                print(f"Error deleting document {x.id}: {e}")

        for x in hashes:
            print(f"Cleaning: {x.id}")
            try:
                self.db.collection('hashtags').document(x.id).delete()
            except Exception as e:
                print(f"Error deleting document {x.id}: {e}")

    def add_chirps(self, string):
        # timestamp = time.time()
        timestamp = datetime.datetime.now()
        messaggio = string
        # hashtags = self.get_hashtags(messaggio)
        hashtags = re.findall('(#\w+)', messaggio, re.DOTALL)
        print(timestamp)
        h = {
            'message': messaggio,
            'hashtags': hashtags,
            'timestamp': str(timestamp)
        }
        self.db.collection('messages').document(str(timestamp)).set(h)
        for hsh in hashtags:
            ref = self.db.collection('hashtags').document(hsh).get()
            if ref.exists:
                hash_ref = self.db.collection('hashtags').document(hsh)
                hash_ref.update({str(self.counter): str(timestamp)})
            else:
                tmp = {
                    str(self.counter): str(timestamp)
                }
                self.db.collection('hashtags').document(hsh).set(tmp)
        x = {
            'message': messaggio,
            'hashtags': hashtags,
            'timestamp': str(timestamp),
            'id': str(self.counter)
        }
        print(x)
        data = messaggio.encode("utf-8")  # punto 3 anche qui
        topic_path = publisher.topic_path('travel2-405610', hashtags[0][1:])
        try:
            topic = publisher.create_topic(request={"name": topic_path})
        except:
            print('Topic already created')
        publisher.publish(topic_path, data)  # e qui
        self.counter = self.counter + 1
        return x

    def get_chirps(self, ids):
        chirp = self.db.collection('messages').document(ids).get()

        if chirp.exists:
            # qui conosco i vari campi contenuti all'interno del document
            # quindi posso usare questa strada
            h = {
                'id': str(chirp.get('timestamp')),
                'message': chirp.get('message'),
                'timestamp': chirp.get('timestamp')
            }
            return h
        else:
            return None

    def get_topics(self, topic):
        hash_ref = self.db.collection('hashtags').document('#'+topic).get()
        lists = []
        messages = []
        if hash_ref.exists:
            data = hash_ref.to_dict()
            # qui non conosco i vari campi contenuti (ogni chirp con l'hashtag)
            # crea un campo col rispettivo valore
            # quindi devo usare una strada alternativa
            for key, value in data.items():
                print(f"{key}: {value}")
                lists.append(value)

            for x in lists:
                message_ref = self.db.collection('messages').document(x).get()
                messages.append(message_ref.get('message'))
            return messages
        else:
            return None
