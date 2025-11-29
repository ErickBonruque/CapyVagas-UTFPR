build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

migrate:
	docker-compose run --rm backend python manage.py migrate

makemigrations:
	docker-compose run --rm backend python manage.py makemigrations

shell:
	docker-compose run --rm backend python manage.py shell

deploy-docker:
	git pull
	make build
	make up -d
