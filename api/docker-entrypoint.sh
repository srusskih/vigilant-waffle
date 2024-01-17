#!/bin/bash
echo "Migrate the Database at startup of project"
poetry run python manage.py migrate

echo "Django docker is fully configured successfully."
exec "$@"
