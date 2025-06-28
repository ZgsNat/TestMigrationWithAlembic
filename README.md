# TestMigrationWithAlembic

## Running with Docker

This project provides a Docker setup for local development and testing. The main application runs with Python 3.11 and uses FastAPI, while PostgreSQL is used as the database. The Docker Compose configuration manages both services.

### Requirements
- Docker
- Docker Compose

### Environment Variables
- The application can use a `.env` file at the project root for environment variables. Uncomment the `env_file` line in `docker-compose.yml` if you wish to use it.
- Default PostgreSQL credentials are set in the compose file:
  - `POSTGRES_USER=postgres`
  - `POSTGRES_PASSWORD=postgres`
  - `POSTGRES_DB=app_db`

### Build and Run
1. Build and start the services:
   ```sh
   docker compose up --build
   ```
2. The FastAPI app will be available at [http://localhost:8000](http://localhost:8000).
3. PostgreSQL will be available at `localhost:5432` with the credentials above.

### Ports
- **FastAPI app:** `8000` (exposed as `8000:8000`)
- **PostgreSQL:** `5432` (exposed as `5432:5432`)

### Notes
- The application runs as a non-root user inside the container for security.
- Python dependencies are installed in a virtual environment within the container.
- Persistent PostgreSQL data is stored in a Docker volume (`pgdata`).
- The default command starts the FastAPI app with Uvicorn: `uvicorn src.main:app --host 0.0.0.0 --port 8000`.
