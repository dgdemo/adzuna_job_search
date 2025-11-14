# adzuna_job_search

![Status](https://img.shields.io/badge/status-MVP_in_progress-yellow)

## 🚀 Project Overview

This project uses the **Adzuna Job Search API** to fetch real job listings and expose them via a simple **FastAPI** backend.  

The goal is to build a small but realistic “job market intelligence” service that you can later extend with a React UI, Terraform-based infrastructure, and DevSecOps tooling (scanning, CI/CD, etc.).

Right now, the focus is on:

- Clean, well-structured **Python backend** code.
- Clear **API integration** with Adzuna.
- A roadmap that tells a convincing **DevSecOps story** for hiring managers.

---

## 🧑‍💻 Why This Exists

- Practice integrating with a real-world REST API (Adzuna).
- Show experience with:
  - Python / FastAPI
  - API clients, pagination, filtering logic
  - Secure config via environment variables
- Provide a portfolio project that’s:
  - Easy to clone and run locally
  - Easy for reviewers to skim and understand

---

## 💡 Current Features (MVP)

**Implemented / in progress:**

- FastAPI backend with:
  - `/health` endpoint for basic health-checks.
  - `/search` endpoint that:
    - Calls the Adzuna Job Search API.
    - Accepts query params such as `what`, `where`, `min_salary`, `max_days_old`, `page`.
    - Returns **normalized JSON** (title, company, salary, location, etc.).
- Configuration via `.env` file (no secrets in the repo).
- Basic error handling when the Adzuna API fails or keys are missing.

---

## 🧭 Roadmap

### Short-Term (Backend-focused)

- [ ] Add SQLite storage for caching results.
- [ ] Add unit tests for the Adzuna client and normalization logic.
- [ ] Add logging (structured logs for requests & errors).
- [ ] Add pre-commit hooks (formatting, linting).

### Medium-Term (Frontend + UX)

- [ ] React + TypeScript frontend that calls the FastAPI `/search` endpoint.
- [ ] Search form and results table (filter, sort, pagination).
- [ ] Basic charts (e.g., salary distribution, top titles).

### Long-Term (DevSecOps / Cloud)

- [ ] Dockerize the backend.
- [ ] Deploy to AWS (e.g., ECS or EC2) using Terraform.
- [ ] GitHub Actions CI/CD:
  - Run tests & linting on PRs.
  - Build & push Docker image.
  - SAST with CodeQL.
  - Container scanning with Trivy.
- [ ] Add GitLeaks and a simple secrets policy / pre-commit config.

---

## 🧰 Tech Stack

**Current (MVP):**

- **Language:** Python 3.11
- **Framework:** FastAPI
- **HTTP Client:** `httpx`
- **Config:** `python-dotenv` with `.env`
- **API:** [Adzuna Job Search API](https://developer.adzuna.com)

**Planned:**

- **Frontend:** React 18 + TypeScript
- **Database:** SQLite locally, PostgreSQL or managed DB in the cloud
- **Infrastructure:** AWS via Terraform
- **CI/CD:** GitHub Actions
- **Security Tooling:** Docker, Trivy, GitLeaks, CodeQL

---

## 🔧 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/dgdemo/adzuna_job_search.git
cd adzuna_job_search
