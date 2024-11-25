
# Ожидаем доступности базы данных
until pg_isready -h "$DATABASE_HOST" -p "$DATABASE_PORT" -U "$POSTGRES_USER"; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done

# Выполняем миграции
python manage.py makemigrations
python manage.py migrate

# Запускаем сервер
exec "$@"
