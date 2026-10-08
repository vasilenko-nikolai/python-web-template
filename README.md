# Python Web Application Template

Базовый шаблон для создания новых веб-приложений на Python. Он содержит
заготовку слоистой архитектуры, управление зависимостями через `uv`, окружение
для разработки в Docker и набор команд для проверки качества кода.

Шаблон не содержит прикладной бизнес-логики. Каталоги верхнего уровня можно
наполнять и адаптировать под требования конкретного проекта.

## Технологии

- Python 3.13+
- FastAPI
- SQLAlchemy 2
- Alembic
- PostgreSQL
- pytest
- Ruff
- mypy
- [uv](https://docs.astral.sh/uv/) для управления окружением и зависимостями
- [Task](https://taskfile.dev/) для команд разработки
- Docker и Docker Compose для изолированного окружения

## Структура проекта

```text
application/    # сценарии приложения и координация бизнес-операций
domain/         # бизнес-модели и правила, не зависящие от инфраструктуры
adapters/       # адаптеры внешних интерфейсов и интеграций
infra/          # база данных, конфигурация и инфраструктурные реализации
presentation/   # HTTP API и другие входные интерфейсы
tests/          # автоматические тесты
docker/         # Docker-окружение для разработки
```

Границы слоёв служат отправной точкой, а не жёстким ограничением. Ненужные
каталоги можно удалить, а структуру — расширить под архитектуру приложения.

## Быстрый старт с Docker

Понадобятся Docker и Docker Compose. Создайте локальный файл с переменными
окружения:

```bash
cp dist.env .env
```

Соберите dev-образ и запустите тесты:

```bash
docker compose build dev
docker compose run --rm dev task test
```

`Task` и все Python-зависимости уже установлены внутри образа. Исходники
подключаются в контейнер с правом записи, поэтому результаты форматирования
сразу появляются в рабочей копии.

## Локальная разработка

Для работы без Docker понадобятся Python 3.13+, `uv` и `Task`.

Установите зависимости и запустите тесты:

```bash
uv sync --dev
uv run pytest
```

Либо активируйте окружение и используйте команды из `Taskfile.yml`:

```bash
source .venv/bin/activate
task test
```

## Команды разработки

```bash
task test         # запустить тесты
task format       # отформатировать код и применить исправления Ruff
task lint:ruff    # проверить код с помощью Ruff
task lint:mypy    # выполнить статическую проверку типов
task check        # запустить все проверки
```

Те же команды можно выполнять в Docker:

```bash
docker compose run --rm dev task test
docker compose run --rm dev task check
```

По умолчанию контейнер работает с UID/GID `1000:1000`. Если идентификаторы
локального пользователя отличаются, передайте их явно:

```bash
LOCAL_UID=$(id -u) LOCAL_GID=$(id -g) docker compose run --rm dev task format
```

## PostgreSQL

Запустить базу данных отдельно:

```bash
docker compose up -d postgres
```

Текущие параметры окружения разработки:

```text
host: localhost
port: 5432
database: workout
user: workout
password: workout
```

Из контейнера `dev` база доступна по адресу `postgres:5432`. При запуске команд
через этот сервис Compose автоматически запускает PostgreSQL и ждёт прохождения
healthcheck. Данные хранятся в именованном Docker volume `postgres-data`.

Остановить сервисы:

```bash
docker compose down
```

Удалить сервисы вместе с локальными данными PostgreSQL:

```bash
docker compose down --volumes
```

## Настройка шаблона для нового проекта

Перед началом разработки:

1. Измените `name` и `description` в `pyproject.toml`.
2. Замените параметры PostgreSQL в `docker-compose.yaml` на подходящие проекту.
3. Добавьте переменные окружения в `dist.env`, не помещая секреты в репозиторий.
4. Настройте список каталогов для Ruff и mypy в `Taskfile.yml`.
5. Добавьте точку входа FastAPI, миграции Alembic и прикладной код.

Конфигурация `docker-compose.yaml` и образ `docker/dev/Dockerfile` предназначены
для локальной разработки и CI, а не для production-развёртывания.
