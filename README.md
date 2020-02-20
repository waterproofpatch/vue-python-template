# Vue-Python-Template

Template for setting up a simple RESTful API with authentication and backend models using Python's Flask microframework and VueJS for the frontend.

## Usage

### Start the backend:

```bash
source venv/bin/activate
python -m backend.app
```

### Start the frontend:

```bash
cd frontend
npm run serve
```

### Build docker container:

```
docker build -t . vue-python-template
docker run -p 8080:80 vue-python-template
```

### Test UWSGI:

```
uwsgi --socket 0.0.0.0:5000 --protocol=http --wsgi-file backend/app.py --callable app --virtualenv ./venv
```


