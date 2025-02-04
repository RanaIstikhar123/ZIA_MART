FROM python:3.12

LABEL maintainer="Istikhar Ali"

# Set the working directory in the container
WORKDIR /code

# Install system dependencies required for potential Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    protobuf-compiler \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry
COPY . /code
RUN poetry config virtualenvs.create false


RUN poetry install

# Expose port 8002
EXPOSE 8008

# Run the app. CMD can be overridden when starting the container
CMD ["poetry", "run", "uvicorn", "order_service.main:app", "--host", "0.0.0.0", "--port", "8008", "--reload"]