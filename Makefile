docker:
	docker build . -t vue-python-template

run_docker:
	docker run -p 8080:80 vue-python-template
