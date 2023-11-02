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

## Firestore management
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

