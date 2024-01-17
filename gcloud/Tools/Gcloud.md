## Gcloud project management
### Creating project
```bash
$ export PROJECT_ID=<your_project_name>
$ gcloud projects create ${PROJECT_ID} --set-as-default

$ gcloud config set project ${PROJECT_ID}
```

### Retrieve details or retrieve list
```bash
$ gcloud describe ${PROJECT_ID}

$ gcloud projects list
```

### Create app
```bash
$ gcloud app create --project=${PROJECT_ID}
```

### File yaml
```yaml
runtime: python37
entrypoint: gunicorn app:app # Specifica l'entrypoint, utilizzando Gunicorn per servire l'app Flask
handlers:
- url: /static
  static_dir: static
- url: /.*
  secure: always
  script: auto
```

### Deployment
```bash
$ gcloud app deploy

$ gcloud app browse
```

## Firestore
### Credentials setup
```bash
export NAME=webuser
export PROJECT_ID=rlfirestore2022
gcloud iam service-accounts create ${NAME}
gcloud projects add-iam-policy-binding ${PROJECT_ID}
    --member "serviceAccount:${NAME}@${PROJECT_ID}.iam.gserviceaccount.com"
    --role "roles/owner"
touch credentials.json
gcloud iam service-accounts keys create credentials.json
    --iam-account ${NAME}@${PROJECT_ID}.iam.gserviceaccount.com
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/credentials.json"
```
Perchè abbiamo bisogno di questo passaggio? Nel caso volessimo connetterci a Firestore da un applicazione Flask eseguita in locale (non su app engine).

### Local vs gcloud db
Non serve (vedi punto dopo).

### Firestore local emulator
Per lanciare un comodissimo emulatore Firestore in locale, dare:
```bash
$ gcloud emulators firestore start --host-port=127.0.0.1:9000
```
Ovviamente bisogna mettere in python la seguente variabile d'ambiente:
```
FIRESTORE_EMULATOR_HOST=127.0.0.1:9000
```

### Python code lines
```python
consumi = self.db.collection('consumi').get()  # fetching della raccolta consumi

for x in consumi:  # scorrimento di tutti i documenti all'interno della raccolta
  ........

h = {
      'date': date,
      'value': value
      }
self.db.collection('consumi').document(date).set(h)  # aggiungo documenti con campi

chirp = self.db.collection('messages').document(ids).get()  # fetching del documento
if chirp.exists:
    h = {
        'id': str(chirp.get('timestamp')),  # fetch singolo campo del doc
        'message': chirp.get('message'),
        'timestamp': chirp.get('timestamp')
    }
    return h
else:
    return None


test = len(self.db.collection('consumi').get())  # controllo il numero di documenti nella raccolta
```

Alcune cose (nel caso servano):
```python
docs = self.db.collection('consumi').order_by("date", direction=firestore.Query.DESCENDING).limit(2).get()
# fetcha solo i primi due documenti dalla lista in ordine alfabetico

self.db.collection('messages').document(x.id).delete()
# per cancellare (x.id è il nome del documento!)
```

## HTML
### Declaration in Python
```python
class Faceform(Form):
  # label, topic e submit sono i nomi degli oggetti form
    label = StringField('Message', [validators.length(max=100)])
    topic = StringField('topic', [validators.length(max=100)])
    submit = SubmitField('Submit')


class Struct:  # NECESSARIO!
    def __init__(self, **entries):
        self.__dict__.update(entries)
```

### Code lines
```python
@app.route('/', methods=['GET', 'POST'])
def hello_world(): 
    c = {'Message': ''}
    if request.method == 'POST':
      # qui entra quando premi invio
        cform = Faceform(request.form)
        if cform.label.data != "":
            faccialibro_dao.add_chirps(cform.label.data)
            return 'MEssaggio inserito!'
        else:
            messages = faccialibro_dao.get_topics(cform.topic.data)
            return messages
    if request.method == 'GET':
      # se deve visualizzare la pagina con i form vuoti
        cform = Faceform(obj=Struct(**c))
        return render_template('index.html', name=c['Message'], form=cform)
```
```html
<form method="post">
<table class="table" style="width:100%">
                <tr class="td">
                  <!-- il primo label è il nome; il secondo è l'attributo -->
                  <th class="td">{{form.label.label}}</th>
                </tr>
                <tr>
                    <td class="td">{{form.label}}</td>
                </tr>
                <tr>
                  <td class="td"><input type="submit" value="Insert"></td>
                </tr>

    <tr class="td">
                  <th class="td">{{form.topic.label}}</th>
                </tr>
                <tr>
                    <td class="td">{{form.topic}}</td>
                </tr>
                <tr>
                  <td class="td"><input type="submit" value="Insert"></td>
                </tr>
            </table>
    </form>
```

## Pub/sub
### Activate pub/sub (gcloud way)
```bash
$ gcloud pubsub topics create hashtags
$ gcloud pubsub subscriptions create subs --topic hashtags
```

### Activate pub/sub (Python way)
```python
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('travel2-405610', hashtags[0][1:])
        try:
            topic = publisher.create_topic(request={"name": topic_path})
        except:
            print('Topic already created')
```
```python
publisher = pubsub_v1.PublisherClient()
subscriber = pubsub_v1.SubscriberClient()
topic_path = publisher.topic_path('travel2-405610', primo)
subscription_path = subscriber.subscription_path('travel2-405610', primo+'subs')
try:
    subscription = subscriber.create_subscription(
        request={"name": subscription_path, "topic": topic_path}
    )
except:
    print("Subs already created")
```
### Code lines
```python
from google.cloud import pubsub_v1

# questa parte qui per il punto 3
publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path('travel2-405610', 'hashtags')

# per inviare
data = messaggio.encode("utf-8")  # punto 3 anche qui
publisher.publish(topic_path, data)  # e qui
```
*Per il subscriber vedere file python subs.py.*

## Functions
### OBBLIGATORI!
```
gunicorn<21.0,>=19.2.0
flask<3.0,>=1.0
```

### HTTP
```bash
$ gcloud functions deploy [FUNCTION_NAME] --runtime [RUNTIME] --trigger-http --allow-unauthenticated
```
La funzione specificata da *nome_funzione* viene cercata da gcloud all'interno di un file *main.py* per impostazione predefinita, perché se specifichiamo come runtime python, cercherà un file .py. Quando specifichiamo HTTP come trigger è per ottenere un oggetto richiesta. Il runtime può essere, per esempio, python37.
Richiamiamo la funzione via terminale con 
```bash
$ gcloud functions call [FUNCTION_NAME] --data '{"name": "[NAME]"}'
```
oppure via richiesta http
```bash
curl -m 70 -X [POST_URI] \
    -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -H "Content-Type: application/json" \
    -d '{}'
```

### Pub/sub
```bash
$ gcloud functions deploy [FUNCTION_NAME] --trigger-topic [TOPIC_NAME] --runtime [RUNTIME]
```

### Firestore
```bash
$ gcloud functions deploy [FUNCTION_NAME] --runtime [RUNTIME] --trigger-event "providers/cloud.firestore/eventTypes/document.write" --trigger-resource "projects/[PROJECT_ID]/databases/(default)/documents/{document}/{attribute}" 
```
Questo trigger richiama la funzione con un evento simile a questo:
```json
{
    "oldValue": { // Update and Delete operations only
        A Document object containing a pre-operation document snapshot
    },
    "updateMask": { // Update operations only
        A DocumentMask object that lists changed fields.
    },
    "value": {
        // A Document object containing a post-operation document snapshot
    }
}
```
*Per lo script vedere file python main.py.*

## Telegram
```python
requests.post(
  'https://api.telegram.org/botxxxx:yyyyy/sendMessage?chat_id=zzzzz&text='+message
    )
```