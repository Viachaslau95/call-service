# 🚀 Запуск проекта

## 1. Запуск Docker
Собрать и запустить контейнеры:

docker-compose up --build

## 2. Запуск Celery
В отдельном терминале запустите Celery worker:

celery -A src.common.celery.celery_app.celery worker --loglevel=info

## 3. Запуск приложения локально
python run.py(или через пайчарм )
## 4. macOS: установка ffmpeg
Если работаете на Mac, установите ffmpeg:

brew install ffmpeg
