.PHONY: test

# Build docker image. Docker hub account username is 'waterproofpatch'
docker:
	docker build . -t waterproofpatch/vue-python-template

# Run the docker container locally
run_docker: 
	docker run -p 8080:80 waterproofpatch/vue-python-template

# Push docker image to docker hub. Assumes logged in using 'docker login'.
push_docker:
	docker push waterproofpatch/vue-python-template:latest

# Deploy to AWS beanstock. Assumes logged into AWS.
deploy: docker push_docker
	eb deploy VuePythonTemplate-env

# Start the wsgi server locally. Useful to verify the uwsgi config is working
run_uwsgi:
	uwsgi --ini wsgi.ini 

# Start the backend and then the frontend
run_devel:
	python -m backend.app & (cd frontend && npm run serve)

test:
	coverage run -m pytest backend/test -s && coverage html

clean:
	rm -rf htmlcov .coverage 