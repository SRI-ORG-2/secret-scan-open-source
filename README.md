# ShopFlow — E-Commerce Platform

A microservices-based e-commerce platform built with Java, Python, and Node.js.

## Services

| Service | Stack | Port | Description |
|---------|-------|------|-------------|
| `java-order-service` | Spring Boot 3 | 8080 | Order management & inventory |
| `python-auth-service` | FastAPI | 8000 | Authentication & user management |
| `node-api-gateway` | Express.js | 3000 | API Gateway & request routing |

## Infrastructure

- PostgreSQL (orders, users)
- Redis (session store, caching)
- MongoDB (product catalog)
- AWS S3 (static assets)
- RabbitMQ (async messaging)

## Quick Start

```bash
docker-compose up -d
```

## Environment Setup

Copy the example env files and fill in credentials:

```bash
cp .env.example .env
cp services/python-auth-service/.env.example services/python-auth-service/.env
```

## Architecture

```
Client → Node API Gateway → [Java Order Service | Python Auth Service]
                          ↓
                    [PostgreSQL | Redis | MongoDB]
```
