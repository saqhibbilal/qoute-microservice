# Quotation Microservice (Task 2)

A FastAPI-based microservice that calculates quotation totals and generates a bilingual (EN/AR) email draft using OpenAI (or mock).

---

## Features

- POST `/quote` endpoint
- Calculates line totals + grand total
- Generates email draft in English or Arabic
- Mock mode: runs locally **without OpenAI key**
- Docker support
- OpenAPI docs at `/docs`
- Full test coverage

---

## Setup (Local)

### 1. Clone & Enter Folder

```bash
git clone <your-repo>
cd quotation-microservice
```

## Run Tests

```bash
pytest -v
```
