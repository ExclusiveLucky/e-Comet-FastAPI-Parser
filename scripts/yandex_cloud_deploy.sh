#!/bin/bash

# Название функции в Яндекс.Облаке
FUNCTION_NAME="github-repo-parser"

# Проверяем, существует ли функция
yc serverless function get --name $FUNCTION_NAME &> /dev/null

if [ $? -ne 0 ]; then
  echo "Создание новой функции $FUNCTION_NAME..."
  # Создаем новую функцию, если она не существует
  yc serverless function create --name $FUNCTION_NAME
else
  echo "Функция $FUNCTION_NAME уже существует."
fi

# Создаем новую версию функции
echo "Создание новой версии функции $FUNCTION_NAME..."
yc serverless function version create \
  --function-name $FUNCTION_NAME \
  --runtime python311 \
  --entrypoint app.services.parser.run \
  --memory 128m \
  --execution-timeout 60s \
  --source-path ./ \
  --environment DATABASE_URL="${DATABASE_URL}" GITHUB_API_TOKEN="${GITHUB_API_TOKEN}"

# Устанавливаем триггер, который будет запускать функцию каждые 6 часов
TRIGGER_NAME="github-repo-parser-trigger"
TRIGGER_SCHEDULE="rate(6h)"

# Проверяем, существует ли триггер
yc serverless trigger get --name $TRIGGER_NAME &> /dev/null

if [ $? -ne 0 ]; then
  echo "Создание нового триггера $TRIGGER_NAME..."
  yc serverless trigger create timer \
    --name $TRIGGER_NAME \
    --cron-expression "$TRIGGER_SCHEDULE" \
    --invoke-function-name $FUNCTION_NAME
else
  echo "Триггер $TRIGGER_NAME уже существует."
fi

echo "Деплой завершен!"
