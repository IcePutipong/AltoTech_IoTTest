#!/bin/bash

echo "Starting the IoT Infrastructure deployment..."

# Stop existing containers
docker-compose down

# Build and start containers
docker-compose build
docker-compose up -d

# Apply Django migrations
docker-compose exec web python manage.py migrate

# Collect static files (if applicable)
docker-compose exec web python manage.py collectstatic --noinput

echo "Deployment completed!"
