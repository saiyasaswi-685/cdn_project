
```markdown
# Pro CDN: High-Performance Content Delivery API

## 📌 Project Overview
Pro CDN is a specialized Content Delivery API designed to optimize asset distribution and reduce origin server load. Built with **FastAPI**, **PostgreSQL**, and **S3-Compatible Storage (MinIO)**, the system focuses on high-speed metadata retrieval and efficient caching mechanisms.

The core objective of this project is to implement an intelligent "Edge-logic" layer that handles conditional requests, asset versioning, and private content security.

## 🛠️ Tech Stack
* **Framework:** FastAPI (Python 3.9+)
* **Database:** PostgreSQL (Relational metadata & version tracking)
* **Object Storage:** MinIO (S3-compatible storage mock)
* **Containerization:** Docker & Docker Compose
* **Hashing:** SHA-256 for ETag generation

## 🚀 Getting Started

### 1. Repository Setup
Clone the repository and navigate to the project root:
```bash
git clone <YOUR_GIT_REPOSITORY_URL>
cd cdn-project

```

### 2. Environment Configuration

The project is pre-configured to work out of the box using Docker. The following environment variables are managed within `docker-compose.yml`:

* **S3_ENDPOINT_URL**: Connection for the object storage.
* **DATABASE_URL**: Connection for the metadata database.
* **AWS_ACCESS_KEY / AWS_SECRET_KEY**: Credentials for S3 access.

### 3. Deployment

Launch the entire infrastructure using a single command:

```bash
docker-compose up --build -d

```

*The API will be available at `http://localhost:8000`.*

### 4. Running the Performance Benchmark

To verify the caching efficiency and the 100% Cache Hit Ratio, execute the following:

```bash
docker-compose exec app-service python //code/app/scripts/benchmark.py

```

## 📖 API Documentation

Once the services are running, you can access the interactive API documentation:

* **Swagger UI**: [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
* **ReDoc**: [http://localhost:8000/redoc](https://www.google.com/search?q=http://localhost:8000/redoc)

## 🎯 Key Functionalities

* **Asset Upload**: Generates a unique SHA-256 hash (ETag) based on file content.
* **Conditional Downloads**: Utilizes `If-None-Match` headers to serve `304 Not Modified` responses, saving bandwidth.
* **Private Assets**: Implements `Cache-Control: private` to ensure sensitive data is not stored on public edge servers.
* **Versioning**: Allows publishing specific versions of assets for historical tracking.

```

