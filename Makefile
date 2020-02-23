# Docker hub account username is 'waterproofpatch'
docker:
	docker build . -t waterproofpatch/vue-python-template

run_docker:
	docker run -p 8080:80 waterproofpatch/vue-python-template

push_docker:
	docker push waterproofpatch/vue-python-template:latest

run_uwsgi:
	uwsgi --ini wsgi.ini

clean:
	rm app.sock
