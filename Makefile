


deploy:
	docker build -t five-year-journal --file build/Dockerfile --target production .
	docker tag five-year-journal-api registry.heroku.com/${HEROKU_APP_NAME}/web
	docker push registry.heroku.com/${HEROKU_APP_NAME}/web
	heroku container:release web -a ${HEROKU_APP_NAME}
