# SIFIBR Collections Docker Management
.PHONY: help build up down restart logs shell

help:
	@echo "SIFIBR Collections Docker Commands:"
	@echo "  make dev      - Development mode (React + Django)"
	@echo "  make prod     - Production mode (Nginx + Django)"

dev:
	cd docker && docker-compose --profile dev up --build

prod:
	cd docker && docker-compose --profile prod up --build -d

down:
	cd docker && docker-compose down

logs:
	cd docker && docker-compose logs -f

clean:
	cd docker && docker-compose down -v --rmi all --remove-orphans
