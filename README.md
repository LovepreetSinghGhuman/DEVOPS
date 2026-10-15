# RetailPulse 🚀

RetailPulse is a production-grade, containerized retail analytics and transaction processing platform built with modern asynchronous Python, robust database management, caching, background workers, reverse proxy load balancing, monitoring, and automated CI/CD.

---

## 🏗️ Architecture & Tech Stack

- **Backend Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Asynchronous Python web framework)
- **Database & ORM:** PostgreSQL with [SQLAlchemy](https://www.sqlalchemy.org/)
- **Caching & Message Broker:** [Redis](https://redis.io/)
- **Background Tasks:** [Celery](https://docs.celeryq.dev/) for asynchronous data processing and fraud worker pipelines
- **Reverse Proxy & Load Balancing:** [Nginx](https://www.nginx.com/)
- **Observability & Metrics:** [Prometheus](https://prometheus.io/) via `prometheus-fastapi-instrumentator`
- **Testing:** `pytest` with `httpx` integration testing
- **CI/CD:** Automated GitHub Actions pipeline with containerized service health checks

---

## 📂 Project Structure

```text
retail-pulse/
├── .github/
│   └── workflows/
│       └── ci.yml               # GitHub Actions CI pipeline configuration
├── nginx/
│   └── nginx.conf               # Nginx reverse proxy & load balancer configuration
├── prometheus/
│   └── prometheus.yml           # Prometheus metrics scraping configuration
├── src/
│   ├── core/                    # Core configs, security, database session, Redis cache, Celery app
│   ├── models/                  # SQLAlchemy ORM models (Users, Transactions)
│   ├── schemas/                 # Pydantic data validation schemas
│   ├── scripts/                 # Data ingestion and initialization utilities
│   ├── services/                # Background worker logic & fraud detection services
│   └── main.py                  # FastAPI application entrypoint & API routers
├── tests/
│   └── test_api.py              # Integration tests for authentication and API endpoints
├── Dockerfile                   # Production container build specification
├── docker-compose.yml           # Multi-container orchestration (App, Postgres, Redis, Nginx, Prometheus)
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
└── README.md
```

---

## ⚙️ Getting Started & Local Setup

### 1. Clone the Repository & Configure Environment
```bash
git clone https://github.com/LovepreetSinghGhuman/DEVOPS.git
cd retail-pulse
cp .env.example .env
```

### 2. Create Virtual Environment & Install Dependencies
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Run the Test Suite
```bash
PYTHONPATH=. pytest -v
```

---

## 🐳 Docker Compose Deployment

To spin up the entire stack (FastAPI application, PostgreSQL database, Redis cache, Nginx reverse proxy, and Prometheus metrics server):

```bash
docker-compose up --build -d
```

- **API Gateway (Nginx):** `http://localhost/`
- **FastAPI Documentation (Swagger UI):** `http://localhost/docs`
- **Prometheus Dashboard:** `http://localhost:9090`

---

## 🛡️ CI/CD Pipeline

The platform includes a fully automated GitHub Actions CI workflow (`.github/workflows/ci.yml`) that triggers on every push and pull request. It spins up isolated PostgreSQL and Redis service containers, installs dependencies, and runs the complete `pytest` test suite to ensure deployment reliability.
