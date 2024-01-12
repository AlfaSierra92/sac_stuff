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

consumi_doc = self.db.collection('consumi').document(date).get()  # fetching del documento

test = len(self.db.collection('consumi').get())  # controllo il numero di documenti nella raccolta
```

Alcune cose (nel caso servano):
```python
docs = self.db.collection('consumi').order_by("date", direction=firestore.Query.DESCENDING).limit(2).get()
# fetcha solo i primi due documenti dalla lista in ordine alfabetico
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