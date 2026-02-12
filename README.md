# 🚀 Pro CDN – High-Performance Content Delivery API

> A production-ready Content Delivery API designed to optimize asset distribution, reduce origin server load, and implement intelligent edge-logic.

---

## 📌 Overview

**Pro CDN** is a high-performance Content Delivery API built using **FastAPI**, **PostgreSQL**, and **S3-Compatible Storage (MinIO)**.

The system focuses on:

- ⚡ High-speed metadata retrieval  
- 📦 Efficient caching mechanisms  
- 🔐 Secure private content handling  
- 🧠 Intelligent edge-logic processing  
- 🏷️ Asset versioning & conditional requests  

The core objective of this project is to implement an advanced **Edge Logic Layer** that handles:

- Conditional HTTP requests (`If-None-Match`)
- Asset version control
- ETag-based validation
- Secure private asset caching policies

---

## 🏗️ Architecture Overview

```
Client → FastAPI (Edge Logic Layer) → PostgreSQL (Metadata)
                                   → MinIO (Object Storage)
```

### Flow Summary

1. Client requests asset  
2. FastAPI checks metadata (PostgreSQL)  
3. Validates ETag (SHA-256)  
4. If unchanged → Returns `304 Not Modified`  
5. If modified → Fetches from MinIO & returns updated content  

---

## 🛠️ Tech Stack

| Component        | Technology Used |
|------------------|-----------------|
| Backend API      | FastAPI (Python 3.9+) |
| Database         | PostgreSQL |
| Object Storage   | MinIO (S3-compatible) |
| Containerization | Docker & Docker Compose |
| Hashing          | SHA-256 (ETag generation) |

---

## 📂 Project Structure

```
cdn_project/
│
├── app/
│   ├── api/                # API route definitions
│   ├── core/               # Configuration & settings
│   ├── models/             # Database models
│   ├── services/           # Business logic layer
│   ├── scripts/            # Benchmark & utility scripts
│   └── main.py             # FastAPI entry point
│
├── docker-compose.yml      # Multi-container setup
├── Dockerfile              # App container configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## 🚀 Getting Started

### 1️⃣ Clone Repository

```bash
git clone https://github.com/saiyasaswi-685/cdn_project
cd cdn_project
```

---

### 2️⃣ Run Using Docker

The project is fully containerized.

```bash
docker-compose up --build -d
```

This will start:

- FastAPI App Service  
- PostgreSQL Database  
- MinIO Object Storage  

API will be available at:

```
http://localhost:8000
```

---

### 3️⃣ Environment Variables

Configured inside `docker-compose.yml`:

| Variable | Description |
|----------|------------|
| S3_ENDPOINT_URL | Object storage connection |
| DATABASE_URL | PostgreSQL connection string |
| AWS_ACCESS_KEY | S3 access key |
| AWS_SECRET_KEY | S3 secret key |

If running locally without Docker, define these variables in a `.env` file.

---

## 📖 API Documentation

After startup:

- Swagger UI → `http://localhost:8000/docs`
- ReDoc → `http://localhost:8000/redoc`

You can also export the OpenAPI specification using:

```bash
curl http://localhost:8000/openapi.json -o openapi.json
```

---

## 🎯 Core Features

### 📦 Asset Upload
- Generates SHA-256 hash
- Stores hash as ETag
- Saves metadata in PostgreSQL

---

### 🔁 Conditional Downloads
- Supports `If-None-Match`
- Returns `304 Not Modified`
- Reduces bandwidth usage

---

### 🔐 Private Asset Handling
- Uses `Cache-Control: private`
- Prevents public CDN caching
- Requires authentication token

---

### 🏷️ Asset Versioning
- Supports publishing specific versions
- Maintains version history in database
- Enables historical asset retrieval

---

## 📊 Performance Benchmark

Run benchmark script:

```bash
docker-compose exec app-service python /code/app/scripts/benchmark.py
```

Benchmark validates:

- Cache hit ratio
- Average response latency
- CDN vs Origin traffic distribution

---

## 🔒 Security Highlights

- SHA-256 content hashing for ETag
- Token-based access validation for private content
- Controlled caching policies
- Environment-based credential management
- Docker-isolated services

---

## 🧪 Future Improvements

- Redis-based edge metadata caching
- Rate limiting & throttling
- Cloud deployment (AWS / GCP)
- CI/CD integration
- CDN invalidation API
- Signed URL support for temporary access

---

## 👨‍💻 Author

Developed by **Sai Yasaswi**

---

## 📜 License

This project is intended for educational and demonstration purposes.
