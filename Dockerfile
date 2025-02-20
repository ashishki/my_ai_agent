# Используем официальный базовый образ Python
FROM python:3.10-slim

# Обновляем систему и устанавливаем зависимости для сборки (если нужно)
RUN apt-get update && apt-get install -y build-essential

# Создаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --upgrade pip && pip install -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Указываем переменные окружения (при необходимости)
ENV PORT=8000

# Открываем порт
EXPOSE 8000

# Запускаем приложение с Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
