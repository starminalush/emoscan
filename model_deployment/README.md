Model deployment
==============================
Описание: 
---------------------
Cервис для инференса нейросетевых моделей на основе [Ray Serve](https://docs.ray.io/en/latest/serve/index.html). 
Модели:
 - [MTCNN](https://pypi.org/project/mtcnn/) для детекции лиц
 - [DeepSort](https://pypi.org/project/deep-sort-realtime/) для трекинга лиц
 - [EmotionRecognition](https://github.com/starminalush/mfdp-2023) - наша обученная модель распознавания лиц на основе DAN

**Примечение:**

Модели для детекции лиц и трекинга были сознательно использованы такие простые, потому что мне показалось не очень хорошей идеей вносить сюда подмодули с нормальными моделями.
На это есть следующие причины:
 - Если деплоить, то все через onnxruntime. Переводить сторонние модели в ONNX не особо наглядно.
 - Качество этих моделей для MVP вполне устраивает.
 - Это снизит размер готового образа. Он и так потребляет слишком много ресурсов из-за Ray Serve.

Если ваша модель лежит на mlflow и не сконвертирована в onnx, запустите следующий скрипт, прежде чем продолжать.

Описание запуска модуля
---------------------
 - заполнить .env файл в model_deployment/.env
 - заполнить .env файл в корне проекта.
 - `sudo docker compose up --build -d model_deployment`. 
Примечание: если на моменте билда появляется ошибка failed to fetch anonymous token: unexpected status: 401 Unauthorized, выполните следующую команду:
`sudo docker pull  nvcr.io/nvidia/cuda:11.6.0-cudnn8-devel-ubuntu20.04` и снова запустите `sudo docker compose up --build -d model_deployment`
 
Контейнер весит почти 20гб, потому что внутри у него анаконда



