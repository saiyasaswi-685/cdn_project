# 🏗️ ARCHITECTURE.md  
Pro CDN – System Architecture & Request Flow

---

# 📌 1. High-Level Architecture Overview

Pro CDN is designed as a layered content delivery system that separates:

- Edge caching logic
- API business logic
- Metadata storage
- Object storage

The system optimizes asset delivery while minimizing origin server load.

---

# 🖼️ 2. Architecture Diagram

```
                ┌───────────────┐
                │    Client     │
                │ (Browser/API) │
                └───────┬───────┘
                        │ HTTP Request
                        ▼
                ┌──────────────────┐
                │      CDN Layer    │
                │  (Edge Caching)   │
                └───────┬───────────┘
                        │ Cache Miss
                        ▼
                ┌──────────────────┐
                │   FastAPI App     │
                │  (Edge Logic API) │
                └───────┬───────────┘
                        │
            ┌───────────┴───────────┐
            ▼                       ▼
   ┌────────────────┐      ┌────────────────┐
   │   PostgreSQL    │      │     MinIO      │
   │ (Metadata DB)   │      │ (Object Store) │
   └────────────────┘      └────────────────┘
```

---

# 🧩 3. Component Breakdown

## 3.1 Client
- Web browser
- Mobile app
- API consumer
- Sends HTTP requests
- Uses headers like:
  - `If-None-Match`
  - `Authorization`
  - `Cache-Control`

---

## 3.2 CDN Layer (Edge Layer)

Responsibilities:

- Caches public content
- Reduces origin load
- Serves cached responses
- Forwards requests on cache miss
- Respects:
  - `ETag`
  - `Cache-Control`
  - `Last-Modified`

---

## 3.3 FastAPI Application (Origin API)

Acts as:

- Business logic layer
- Conditional request handler
- Authentication validator
- Version controller

Core responsibilities:

- Generate SHA-256 hash (ETag)
- Validate `If-None-Match`
- Return `304 Not Modified` when applicable
- Secure private endpoints
- Manage asset versions

---

## 3.4 PostgreSQL (Metadata Database)

Stores:

- Asset ID
- Version
- SHA-256 hash (ETag)
- Visibility (public/private)
- Upload timestamp
- Last modified time

Used for:

- Fast metadata lookup
- Version tracking
- Conditional request validation

---

## 3.5 MinIO (Object Storage)

Stores:

- Actual binary files
- Versioned objects
- Large static assets

MinIO acts as an S3-compatible storage backend.

---

# 🔄 4. Detailed Request Flow

---

## 📥 Case 1: Public Asset Request (Cache Hit)

1. Client sends request:
   ```
   GET /assets/logo.png
   ```

2. CDN checks edge cache.
3. Asset found in cache.
4. CDN returns cached response.
5. Origin API is NOT contacted.

Result:
- Ultra-low latency
- Zero origin load

---

## 📥 Case 2: Public Asset Request (Cache Miss)

1. Client sends request.
2. CDN checks cache → MISS.
3. CDN forwards request to FastAPI.
4. FastAPI:
   - Queries PostgreSQL
   - Retrieves metadata
   - Fetches object from MinIO
5. FastAPI attaches headers:
   - `ETag`
   - `Cache-Control: public, max-age=...`
   - `Last-Modified`
6. CDN caches response.
7. Response returned to client.

Result:
- Future requests become cache hits.

---

## 📥 Case 3: Conditional Request (ETag Validation)

1. Client sends:
   ```
   GET /assets/logo.png
   If-None-Match: "abc123hash"
   ```

2. FastAPI compares hash with stored SHA-256.
3. If unchanged:
   - Returns:
     ```
     304 Not Modified
     ```
   - No object retrieval needed.

Result:
- Saves bandwidth
- Faster response
- No redundant data transfer

---

## 🔐 Case 4: Private Asset Request

1. Client sends:
   ```
   GET /private/report.pdf
   Authorization: Bearer <token>
   ```

2. FastAPI:
   - Validates token
   - Checks asset visibility
3. If valid:
   - Fetches object
   - Returns with:
     ```
     Cache-Control: private
     ```

4. CDN does NOT cache this content.

Result:
- Sensitive content never stored on edge

---

# 🧠 5. Caching Strategy

---

## 5.1 Public Assets

Headers used:

```
Cache-Control: public, max-age=3600
ETag: "<sha256_hash>"
Last-Modified: <timestamp>
```

Behavior:

- Cached by CDN
- Validated using ETag
- Reduces database & storage hits

---

## 5.2 Private Assets

Headers used:

```
Cache-Control: private, no-store
```

Behavior:

- Never cached by CDN
- Always validated at origin
- Requires authentication

---

# 📊 6. Performance Optimization Strategy

- Metadata stored separately from binary objects
- SHA-256 ensures deterministic caching
- 304 responses eliminate object fetch
- CDN absorbs repeated traffic
- Stateless API design for horizontal scaling

---

# 🔐 7. Security Design

- Token-based authentication for private endpoints
- Environment-based credential management
- Strict header validation
- Version-controlled assets
- No direct object storage exposure

---

# 🎯 8. Design Goals Achieved

✔ Reduced origin server load  
✔ High cache hit ratio  
✔ Secure private content delivery  
✔ Efficient conditional request handling  
✔ Version-aware asset management  

---

# 🚀 Future Improvements

- Redis-based edge metadata caching
- Distributed CDN simulation
- Signed URLs for temporary access
- Rate limiting & abuse detection
- Multi-region deployment

---

