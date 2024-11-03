# Microservices Project

This project consists of a microservices architecture with a user service, a notification service, and monitoring setup using Traefik and Prometheus.

## Architecture

The architecture of this microservices project is shown in the diagram below. This diagram illustrates how each service interacts within the ecosystem, including the API gateway (Traefik) and the monitoring service (Prometheus).

![Arquitecture](docs/arq.png)

## Setup Instructions

1. Create a `.env` File
   Clone the `.env.dev` file and rename it to `.env.` Configure any necessary environment variables in this file before running the application.

```bash
cp .env.dev .env
```

2. Create the Dockerfiles
   Since the `dockerfile` files are included in `.gitignore`, you’ll need to create them manually in each service folder (`notification_service` and `user_service`). Define the necessary configurations for each Dockerfile according to the requirements of each service.
3. Run the Project
   To start all services, use the following command:

```bash
docker-compose up -d
```

This will build and run the containers in detached mode.

## Accessing Services

- API Gateway (Traefik Dashboard): The API gateway is accessible at `http://localhost:8080`.
- Prometheus (Metrics Portal): The Prometheus metrics portal is available at `http://localhost:9090`.
- API Documentation (FastAPI): The API documentation for testing is available at `http://127.0.0.1/docs`.

## Notes

Ensure all necessary environment variables are set in `.env` for smooth operation.
Adjust paths and ports in `docker-compose.yml`, `prometheus.yml`, and `traefik.yml` if necessary to suit your environment.
