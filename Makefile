.PHONY: build up down startapp test lint add_app
build:
	docker compose build --no-cache
up:
	docker compose up
down:
	docker compose down
test:
	docker compose run --rm app sh -c "python manage.py test"
create_superuser:
	docker compose run --rm app sh -c "python manage.py createsuperuser"
lint:
	docker compose run --rm app sh -c "flake8"
check_db:
	docker compose run --rm app sh -c "python manage.py wait_for_db"
make_migrations:
	docker compose run --rm app sh -c "python manage.py wait_for_db && python manage.py makemigrations"
add_app:
	docker compose run --rm app sh -c "python manage.py startapp $(NAME)"

