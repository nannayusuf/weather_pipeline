# Weather Pipeline: Weather Data ETL Pipeline

This project implements a robust, production-ready ETL (Extract, Transform, Load) pipeline focused on collecting, processing, and storing weather data. Developed with best practices in data engineering and DevOps, it serves as a comprehensive portfolio showcasing skills in software development and data orchestration.

## Project Overview

The `weather_pipeline` is designed to automate the flow of weather data, from its origin in external APIs to its storage in an analytical database. It utilizes a modern architecture based on containers and workflow orchestration to ensure scalability, reliability, and easy maintenance.

## Key Features

-   **Weather Data Extraction**: Collects weather information from external APIs (requires an API key).
-   **Data Transformation**: Processes and cleans raw data, preparing it for analysis and storage.
-   **Data Loading**: Stores transformed data in a dedicated PostgreSQL database.
-   **Workflow Orchestration**: Manages and schedules pipeline steps using Apache Airflow.
-   **Containerization**: Packages the application and its services in Docker containers to ensure consistent and reproducible environments.
-   **Code Quality**: Continuous integration with linting, formatting, type checking, and automated tests.

## Technologies Used

This project demonstrates proficiency in the following technologies and tools:

-   **Python**: Main programming language for ETL pipeline development.
-   **Apache Airflow**: Platform for programmatically authoring, scheduling, and monitoring data workflows.
-   **Docker & Docker Compose**: For containerization and orchestration of multiple services.
-   **PostgreSQL**: Relational database for storing raw and processed data, as well as Airflow metadata.
-   **Pandas**: Library for data manipulation and analysis.
-   **Pydantic-Settings**: Secure configuration and environment variable management.
-   **Structlog**: Structured logging for improved observability and debugging.
-   **Ruff**: Python linter and formatter.
-   **Mypy**: Static type checker for Python.
-   **Pytest & Pytest-Cov**: Testing framework and code coverage tool.
-   **Pre-commit**: Hooks to ensure code quality before commits.
-   **GitHub Actions**: For CI/CD automation (Continuous Integration and Continuous Delivery).

## Project Structure

```
.github/
├── workflows/
│   └── ci.yml             # CI/CD workflow with GitHub Actions
src/
├── weather_pipeline/
│   ├── __init__.py
│   ├── config.py          # Project configurations (Pydantic-Settings)
│   ├── main.py            # Main entry point of the pipeline
│   └── weather_pipeline.py # Main ETL logic (to be implemented)
tests/
├── __init__.py
├── test_main.py           # Basic tests for the main function
└── test_smoke.py          # Smoke tests for configurations
Dockerfile                 # Application container definition
docker-compose.yaml        # Service orchestration (Airflow, PostgreSQL)
.env.example               # Example environment variables
.gitignore                 # Files and directories to be ignored by Git
.pre-commit-config.yaml    # Pre-commit hooks configuration
mypy.ini                   # Mypy configuration
pyproject.toml             # Project metadata and dependencies (PEP 621)
requirements.in            # Development dependencies (for pip-compile)
requirements.txt           # Production dependencies
requirements-dev.txt       # Development dependencies
```

## How to Set Up and Run

To set up and run the project locally, follow the steps below:

### Prerequisites

Ensure you have the following tools installed on your machine:

-   [Docker](https://docs.docker.com/get-docker/)
-   [Docker Compose](https://docs.docker.com/compose/install/)
-   [Python 3.10+](https://www.python.org/downloads/)
-   [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)

### Execution Steps

1.  **Clone the Repository**:

    ```bash
    git clone https://github.com/nannayusuf/weather_pipeline.git
    cd weather_pipeline
    ```

2.  **Configure Environment Variables**:

    Create a `.env` file in the project root, copying from `.env.example` and filling in your own API keys and other necessary configurations. **Do not commit this file!**

    ```bash
    cp .env.example .env
    # Edit the .env file and add your WEATHER_API_KEY and FERNET_KEY for Airflow
    ```

    Example `.env`:

    ```
    WEATHER_API_KEY=your_api_key_here
    FERNET_KEY=your_generated_fernet_key_here # Generate with `python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"`
    ```

3.  **Build and Start Docker Services**:

    ```bash
    docker-compose up --build -d
    ```

    This will build the Docker images and start the `postgres`, `data-db`, `airflow-webserver`, and `airflow-scheduler` services in the background.

4.  **Access Airflow UI**:

    Once the services are running, you can access the Apache Airflow web interface at `http://localhost:8080`.

5.  **Run the ETL Pipeline (via CLI or Airflow)**:

    You can run the pipeline manually via the command line (if the main logic is implemented in `main.py`):

    ```bash
    docker-compose exec weather_pipeline python -m src.weather_pipeline.main
    ```

    Or, ideally, enable and monitor the corresponding DAG in the Airflow UI.

## TODO: Next Steps and Improvements

This project provides a solid foundation, but there are still areas for development and enhancement to make it a fully functional and demonstrable weather data ETL pipeline:

-   **Implement Main ETL Logic**: The `main()` function in `src/weather_pipeline/main.py` contains a `TODO` for integrating the extraction, transformation, and loading steps. This is the core functionality of the pipeline and should be developed to collect real-time data from a weather API, process it, and load it into the `data-db`.
-   **Develop Airflow DAGs**: Create DAGs (Directed Acyclic Graphs) in the `dags/` directory to orchestrate the extraction, transformation, and loading steps, defining their dependencies and scheduling.
-   **Comprehensive Unit Tests**: Add detailed unit tests for the extraction, transformation, and loading functions (once implemented) to ensure the robustness and correctness of the business logic.
-   **ETL Logic Documentation**: Document in the code and, if necessary, in the README itself, how extraction, transformation, and loading are performed, including data formats and business rules.
-   **Data Visualization**: Integrate a visualization tool (e.g., Metabase, Grafana) or create Python scripts to generate charts and reports from the data in `data-db`.
-   **Error Handling and Retries**: Implement robust error handling and retry strategies for pipeline steps, especially for API calls and database operations.
-   **Monitoring and Alerts**: Configure monitoring for the pipeline and alerts for failures or anomalies.

## Contribution

Contributions are welcome! Feel free to open issues for bugs or suggestions, and pull requests for new features or improvements.

