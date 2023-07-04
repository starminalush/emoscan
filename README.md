# EmoScan

MVP для проекта распознавания лиц для онлайн-школ.

[Макеты Figma](https://www.figma.com/file/UDO1ksG3vVUUHI131DGGCC/MFDP?type=design&node-id=0%3A1&t=tSmyiOsMtYIueP19-1)

[LeanCanvas](https://www.notion.so/Lean-Canvas-5d9968e55be04d7288cda83e4c5567f6)

## Описание работы

Схема работы проекта(в идеале) выглядит следующим образом:
![я заглушка для картинки](https://drive.google.com/uc?export=view&id=1jGrIK2ULV-TIO0OxrxMwafIZFWbcWA5F)

## Документация модулей проекта 
 - [Frontend](https://github.com/starminalush/mfdp-2023-mvp/tree/main/frontend/#readme)
 - [Backend](https://github.com/starminalush/mfdp-2023-mvp/tree/main/backend/#readme)
 - [Model_deployment](https://github.com/starminalush/mfdp-2023-mvp/tree/main/model_deployment/#readme)

## Переменные окружения

| Переменная            |                              Описание                              | Значение по умолчанию |
|-----------------------|:------------------------------------------------------------------:|:---------------------:|
| FRONTEND_PORT         |               Порт для внешнего доступа к фронтенду                |         5017          |
| BACKEND_PORT          |                Порт для внешнего доступа к бекенду                 |         8001          |
| MODEL_DEPLOYMENT_PORT |       Порт для внешнего доступа к сервису с деплоем моделей        |         8000          |
| MINIO_PORT            |                   Порт для внешнего доступа к s3                   |         9005          |
| MINIO_BUCKET          | Имя бакета, где будут лежать картинки от результатов распознавания |         logs          |
| AWS_ACCESS_KEY_ID  |                          ACCESS_KEY от s3                          |           backendminio            |
| AWS_SECRET_ACCESS_KEY| SECRET_KEY от s3 |backendminio|
| POSTGRES_PASSWORD| Пароль от базы данных для сборки контейнера с базой postgres | mysecretpassword|
| POSTGRES_EXTERNAL_PORT| Порт для внешнего доступа к базе | 5411 |


## Запуск
 - Чтобы запустить модули по отдельности см. README.md для каждого модуля
 - Чтобы запустить полностью:
   1. Заполнить backend/.env согласно шаблону backend/.env.template
   2. Заполнить frontend/.env согласно шаблону frontend/.env.template
   3. Заполнить model_deployment/.env согласно шаблону model_deployment/.env.template
   4. Заполнить .env согласно шаблону .env.template
   5. Выаолнить команду
   `sudo docker compose up --build -d`
