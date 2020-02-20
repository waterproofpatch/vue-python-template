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
