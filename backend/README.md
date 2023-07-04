Backend для получения результатов распознавания с сервиса model_deployment и записи логов в minio и postgres.

## Переменные окружения

| Переменная           |            Описание             |     Значение по умолчанию     |
|----------------------|:-------------------------------:|:-----------------------------:|
| MODEL_DEPLOYMENT_URI | Адрес сервиса с деплоем моделей | http://model_deployment:8000/ |
| S3_ENDPOINT_URL      |    Адрес S3 для записи логов    |   http://miniobackend:9000    |
 | BUCKET               |    Бакет S3 для записи логов    |             logs              |
 | POSTGRES_USER        |        Пользователь базы        |           postgres            |
 | POSTGRES_PASSWORD    |    Пароль пользователя базы     |       mysecretpassword        |
 | POSTGRES_HOST        |    Адрес подключения к базе     |       postgres_backend        |
 | POSTGRES_PORT        |       Порт доступа к базе       |             5432              |
 | POSTGRES_DB          |      Название базы данных       |           postgres            |


## Структура сервиса

```
    ├── api                       <- Основной модуль апи.
    │   └── endpoints             <- Модуль с api-эндпоинтами сервиса.
    |
    ├── core                      
    │   └── db                    <- Модуль для подключений БД.
    │   └── s3                    <- Модуль для подключений S3.
    |
    ├── crud                      <- Модуль для выполнения CRUD-операций в БД.
    |
    ├── data_classes              <- Модуль c dataclases сервис.
    |
    ├── services                  <- Модуль со внутренней логикой и всем, что не относится к CRUD.
    |
    ├── schemas                   <- Модуль с pydantic-схемами сервиса.
    ├── converters                <- Модуль с конвертерами из формата в формат.
    |
    ├── .env.template             <- Шаблон .env файла.
    |
    ├── Dockerfile                <- Конфиг docker образа.
    |
    ├── main.py                   <- Скрипт инициализации приложения.
    |
    └── requirements.txt          <- Файл с зависимостями.
```

## Запуск
1. Заполните backend/.env по примеру backend/.env.template
2. Заполните .env по примеру .env.template в корне проекта
3. Выполните команду ниже. База поднимется сама вместе с s3 хранилищем minio.

```sudo docker compose up --build -d backend```

