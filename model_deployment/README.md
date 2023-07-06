Cервис для инференса нейросетевых моделей на основе [Ray Serve](https://docs.ray.io/en/latest/serve/index.html). 

## Модели:
 - [MTCNN](https://pypi.org/project/facenet-pytorch/) для детекции лиц
 - [DeepSort](https://pypi.org/project/deep-sort-realtime/) для трекинга лиц
 - [EmotionRecognition](https://github.com/starminalush/mfdp-2023) - наша обученная модель распознавания лиц на основе DAN

**Примечение:**

Модели для детекции лиц и трекинга были сознательно использованы такие простые, потому что мне показалось не очень хорошей идеей вносить сюда подмодули с нормальными моделями.
На это есть следующие причины:
 - Переводить сторонние модели в ONNX не особо наглядно.
 - Качество этих моделей для MVP вполне устраивает.

Если ваша модель распознавания эмоций лежит на mlflow и не сконвертирована в onnx, запустите [скрипт](https://github.com/starminalush/mfdp-2023/blob/main/experiments/converters/torch_to_onnx.py).

## Переменные окружения

| Переменная           |            Описание             | Значение по умолчанию |
|----------------------|:-------------------------------:|:---------------------:|
| AWS_ACCESS_KEY_ID | ACCESS_KEY для s3 хранилища | miniokey|
| AWS_SECRET_ACCESS_KEY | SECRET_KEY для s3 хранилища| miniosecretkey|
| MLFLOW_TRACKING_URI| Адрес mlflow tracking сервера, где модели лежат |http://mlflow_backend:5000 |
|MLFLOW_S3_ENDPOINT_URL| Адрес s3 хранилища mlflow сервера | http://minio:9000|
| MODEL_S3_PATH| Путь до модели для деплоя в mlflow | s3://experiments/1/465e546c511f459196393bb26b978d3a/artifacts/onnx_model.onnx |
| CUDA_VISIBLE_DEVICES| Номер карты для инференса моделей | 0|

## Структура проекта

```
    ├── aliases.py                <- Модуль с type aliases для более удобной работы.
    |
    ├── converter.py              <- Модуль c разными конвертаторами из формата в формат.
    |
    ├── .env.template             <- Шаблон .env файла.
    |
    ├── main.py                   <- Скрипт инициализации приложения и старт пайплайна моделей.
    |
    ├── Dockerfile                <- Конфиг docker образа.
    |
    ├── models.py                 <- Модуль со всеми используемыми моделями
    |
    ├── schemas.py                <- Pydantic модели для обработки результатов.
    |
    ├── utils.py                  <- Скрипт с разными полезными функциями.
    |
    └── requirements.txt          <- Файл с зависимостями.
```

## Запуск
1. Заполните .env файл в model_deployment/.env по примеру model_deployment/.env.template 
2. 3аполнить .env файл в корне проекта по примеру .env.template
3. Выполните команду

`sudo docker compose up --build -d model_deployment`. 

Примечание: если на моменте билда появляется ошибка failed to fetch anonymous token: unexpected status: 401 Unauthorized, выполните следующую команду:

`sudo docker pull  nvcr.io/nvidia/cuda:11.6.0-cudnn8-devel-ubuntu20.04`

 и снова запустите 

`sudo docker compose up --build -d model_deployment`

