## APIs Characters

### Running with docker

#### Pre-requisites:
- docker
- docker compose

#### Steps:
1. Create a file called `.env` with environment variables in the root of the project.
2. Build with `docker compose build`.
3. Run with `docker compose up`.
4. Create migrations if necessary `alembic revision --autogenerate -m "Initial"`
5In another terminal run the migrations `docker compose exec character alembic upgrade head`.
6Run test with `docker compose exec character pytest -vv`.

#### How to use:
- Go to `http://localhost:8000/docs`.
- You can also test the endpoints with your preferred rest client. (Postman/Insomnia).
- Inside the tests directory in the dummy folder is a Postman collection with the endpoints and payload.

#### Environment Variables (.env)
```
# SETTING
ENV=dev
SECRET_KEY=BoilerPlate2024

# POSTGRES
ENGINE=postgresql+psycopg2
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_PORT=5432
POSTGRES_DB=character
POSTGRES_HOST=db
PGTZ=America/Argentina/Buenos_Aires
```
