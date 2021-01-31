ENVIRONMENT			?= dev
APP_NAME            = gaa-api-${ENVIRONMENT}
IMAGE				= gaa-api-${ENVIRONMENT}
TAG                 = latest
PORT				?= 5000
PYTEST_OPTIONS		?= -p no:cacheprovider --cov src.api
DATABASE_URL 		:= $(shell eval heroku config:get DATABASE_URL -a gaa-api-${ENVIRONMENT})

clean:
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

build: clean
	docker build -t $(IMAGE) .

dbui:
	heroku config:get DATABASE_URL -a gaa-api-${ENVIRONMENT} | xargs pgweb --url

run:
	docker run -e ENVIRONMENT=${ENVIRONMENT} -e DATABASE_URL=${DATABASE_URL} -u :1000 -p $(PORT):5000 $(IMAGE)

lint:
	docker run -u :1000 --entrypoint '/bin/sh' $(IMAGE) -c "python3 -m pylint src"

test:
	docker run -u :1000 --entrypoint '/bin/sh' $(IMAGE) -c "python3 -m pytest $(PYTEST_OPTIONS) tests/test_*"

run-dev:
	python3 -m pip install ${ARTIFACTORY_OPTIONS} -r src/requirements.txt --user
	DATABASE_URL=$(DATABASE_URL) python3 run_server.py

lint-dev:
	python3 -m pip install ${ARTIFACTORY_OPTIONS} -r src/dev-requirements.txt --user
	python3 -m pip install ${ARTIFACTORY_OPTIONS} -r src/requirements.txt --user
	python3 -m pylint src

test-dev:
	python3 -m pip install ${ARTIFACTORY_OPTIONS} -r src/dev-requirements.txt --user
	python3 -m pip install ${ARTIFACTORY_OPTIONS} -r src/requirements.txt --user
	python3 -m pytest $(PYTEST_OPTIONS) tests/test_*

publish:
	heroku container:push web -a ${APP_NAME}

release:
	heroku container:release web -a ${APP_NAME}

open:
	heroku open -a ${APP_NAME}

tail-logs:
	heroku logs --tail -a ${APP_NAME}

full-release: clean build publish release open