FROM python:3.10-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache


# Copy the poetry.lock and pyproject.toml files
COPY poetry.lock pyproject.toml ./

# Install project dependencies using Poetry
RUN poetry install --no-root

# Copy the rest of the application code
COPY . .

# Expose the port that the Django application will run on
EXPOSE 8000

# Run the Django application
RUN chmod +x /opt/app/docker-entrypoint.sh
ENTRYPOINT [ "docker-entrypoint.sh" ]
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
