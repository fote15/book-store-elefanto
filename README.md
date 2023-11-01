# Elefanto tech assignment

Rest API for book store

## Installation

Make sure you have [Docker](https://www.docker.com/products/docker-desktop/) to run the app.

```bash
make build
make up
```

## Additinal make features

```python
make make_migrations
make lint
make test
make create_superuser
make add_app

```

## Дополнительно для ревьеверов

Тесты на модулях core и user, а так же wait_for_db команда были в проекте изначально.
Если у вас уже стоит инстанс Postgres, убедитель что у вас есть база - dev_store
Приятного просмотра!

## License

[MIT](https://choosealicense.com/licenses/mit/)
