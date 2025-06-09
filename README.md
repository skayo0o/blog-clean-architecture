# Блог с Clean Architecture

## Описание

Это учебный проект блога, реализованный по принципам Clean Architecture на Python с использованием FastAPI, SQLAlchemy и SQLite.  
В проекте реализованы сущности: **User**, **Post**, **Comment**.  
Архитектура разделена на три слоя:  
- **Domain** (бизнес-логика и модели)
- **Data** (доступ к данным, репозитории, фабрики)
- **Presentation** (REST API, схемы)

Используются паттерны **Repository** и **Factory**.

## Быстрый старт

1. Установите зависимости:
    ```
    pip install -r requirements.txt
    ```

2. Запустите сервер:
    ```
    uvicorn main:app --reload
    ```

3. Откройте документацию API:
    - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
    - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

4. Для тестирования используйте коллекцию Postman:  
   Импортируйте файл `postman_collection.json` в Postman.


## Паттерны

- **Repository** — абстрагирует работу с БД для каждой сущности.
- **Factory** — фабрика для создания репозиториев.


---

**Автор: skayo0o**