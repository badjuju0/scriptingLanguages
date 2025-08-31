# RSS Collector & News API

Этот репозиторий содержит Python-приложение для сбора новостей по RSS и управления ими через веб-интерфейс.
+ реализация в minikube (k8s)

---

## Структура проекта

- `api.py` – Flask API для отображения новостей, добавления RSS-лент и ключевых слов, а также управления пользователями.
- `rss_collector.py` – сборщик RSS-лент и фильтрация новостей по ключевым словам, инициализация базы данных.
- `Dockerfile` – образ для запуска приложения в Docker.
- `entrypoint.sh` – точка входа для Docker, которая инициализирует базу, запускает collector и API.
- `manifest1.yml` – пример манифеста для развертывания приложения в Minikube.

---

## Установка и запуск

### Локально через Docker

1. Собрать образ:

```bash
docker build -t badjuju0/rss:latest .


docker run -p 5000:5000 badjuju0/rss:latest
```
URL:
http://localhost:5000

Логин: admin
Пароль: supersecret

В Minikube / Kubernetes:
```bash
eval $(minikube docker-env)
docker build -t badjuju0/rss:latest .

kubectl apply -f manifest1.yml

kubectl get pods

kubectl port-forward rss-app-79b75f54bf-d6bjh 5001:5000
```
Переменные окружения
DB_PATH – путь к SQLite базе (по умолчанию /data/rss.db).

SECRET_KEY – секретный ключ для сессий Flask (по умолчанию dev).
