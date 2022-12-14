# Панель для администратора онлайн кинотеатра

Необходима для загрузки модераторами или администраторами сайта информации о фильмах

# Запуск контейнеров
Скопировать структуру содержимого .env.example в .env перед запуском со своими данными
```bash
cp .env.example .env
```

Запуск контейнеров
```bash
docker-compose down && docker-compose build && docker-compose up -d
```

Доступ к psql в postgres внутри контейнера.
``` bash
docker exec -it simple_project_postgres_1 psql -h <HOST> -d <NAME> -U <USER>
```

Доступ к контейнеру service.
``` bash
docker exec -it simple_project_service_1 /bin/bash
```

Админка доступна по адресу 

http://127.0.0.1/admin