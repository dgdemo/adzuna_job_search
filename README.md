# adzuna_job_search

![Status](https://img.shields.io/badge/status-MVP_in_progress-yellow)

A minimal FastAPI service that queries the Adzuna Job Search API and returns normalized job listings. This MVP serves as a starting point for a broader job-market intelligence project.

## Overview

This project currently includes:

- A simple FastAPI backend
- A `/search` endpoint that proxies and normalizes Adzuna job listings
- A `/health` endpoint for basic uptime checks
- Configuration via `.env` (Adzuna credentials)
- An HTTP client implemented using `httpx`

This MVP is intentionally lightweight and will be expanded over time into a more complete job-market intelligence service with frontend, infrastructure, and DevSecOps enhancements.

## Tech Stack

- Python 3.11
- FastAPI
- httpx
- python-dotenv
- Adzuna Job Search API

## Running Locally (Test Mode)

### 1. Clone the repository

```bash
git clone https://github.com/dgdemo/adzuna_job_search.git
cd adzuna_job_search

### 2. Create a `.env` file with your Adzuna credentials

```text
ADZUNA_APP_ID=your_id
ADZUNA_APP_KEY=your_key

### 3. Install dependencies

```bash
pip install -r requirements.txt

### 4. Start the FastAPI server with uvicorn

```bash
uvicorn app.main:app --reload

The server will be available at:

- http://127.0.0.1:8000
- http://127.0.0.1:8000/docs



