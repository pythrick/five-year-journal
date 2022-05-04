
format:
	poetry run black . && poetry run isort .

lint:
	poetry run pre-commit install && poetry run pre-commit run -a -v

test:
	poetry run pytest -sx

deploy: VER=$(shell git log -1 --pretty=format:"%h")
deploy:
	docker build -t five-year-journal-api:$(VER) --file build/Dockerfile --target production .
	docker tag five-year-journal-api:$(VER) registry.heroku.com/$(HEROKU_APP_NAME)/web
	docker push registry.heroku.com/$(HEROKU_APP_NAME)/web
	heroku container:release web -a $(HEROKU_APP_NAME)
