# Этот образ предназначен только для локальной разработки и проверок в CI.
# Он содержит как runtime-, так и dev-зависимости проекта и не оптимизирован
# для запуска приложения в production.
FROM python:3.14-slim

# Стабильные логи без буферизации, отсутствие .pyc-файлов в примонтированном
# проекте и отдельное окружение, которое не перекрывается bind mount-ом.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /workspace

# uv устанавливается отдельно, после чего зависимости фиксируются uv.lock.
# go-task-bin добавляет команду task, чтобы внутри контейнера были доступны
# те же команды разработки, что и на локальной машине.
RUN pip install --no-cache-dir uv go-task-bin

# Отдельное копирование метаданных позволяет Docker повторно использовать слой
# с зависимостями, пока pyproject.toml и uv.lock остаются неизменными.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --dev --no-install-project

# Исходный код при обычном запуске Compose подключается поверх этой директории.
# COPY оставляет образ самодостаточным для CI, где bind mount может не применяться.
COPY . .

# Без переопределения команды контейнер запускает тесты.
CMD ["pytest", "-p", "no:cacheprovider"]
