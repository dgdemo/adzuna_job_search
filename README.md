# adzuna_job_search

![Status](https://img.shields.io/badge/status-in_progress-yellow)

## 🚀 Project Overview  
This project leverages the Adzuna job-search API to build a searchable dashboard for finding job opportunities, filtering by role, location, salary, company size, and date posted. Designed with DevSecOps best practices in mind, the repo demonstrates full-stack proficiency: API consumption, data processing, front-end presentation, and infrastructure automation.

## 🧑‍💻 Why Build This  
- Gain hands-on experience with API integration, data transformation, and visualization.  
- Demonstrate skills relevant to roles in DevSecOps, Site Reliability, or Application Security through real-world job market data.  
- Provide a showcase project for your GitHub profile—easy to browse, meaningful to hiring managers, and technically rich.

## 💡 Key Features  
- Connects to the Adzuna API to fetch job listings in real-time (or near real-time).  
- Front-end UI (React/Angular/Vue – choose) for filtering, sorting, and exploring job results.  
- Backend (Node.js/Python – choose) to manage API calls, caching, and data sanitisation.  
- Terraform-defined infrastructure (AWS/Azure/GCP – choose) for deployment including CI/CD.  
- Built-in DevSecOps tooling: static code scanning, containerisation (Docker), secure secrets management (e.g., AWS Secrets Manager / HashiCorp Vault), automated linting + testing.  
- DOCS & README: clean architecture diagram, setup instructions, resume-friendly narrative.

## 🛠️ Current Status & Focus  
> 🚧 **Work in Progress**  
>  
> _This dashboard is under active development. Core features are in place, and upcoming work includes end-to-end CI/CD pipelines, hardened security configurations, and full documentation._

### ✅ In Progress
- [x] Retrieve job data from Adzuna API and store results in PostgreSQL/SQLite.  
- [x] Implement filtering by role, location, salary, date posted.  
- [ ] Add user authentication (optional for personalised job alerts).  
- [ ] Build monitoring & logging for dashboard usage and API consumption.  
- [ ] Automate deployment via Terraform + GitHub Actions.

### 🧭 Next Steps
- Add a “Saved Searches” feature.  
- Implement CI/CD with GitHub Actions that includes SAST/DAST (e.g., CodeQL, SonarQube).  
- Containerise the application and deploy to Kubernetes or AWS ECS.  
- Extend API consumption to include additional job-search sources and union datasets for richer insights.

## 🧰 Tech Stack  
- **Backend:** Node.js v18 / Python 3.11 (select)  
- **Frontend:** React v18 / TypeScript  
- **Database:** PostgreSQL / SQLite  
- **Infrastructure:** AWS (EC2/ECS, RDS, S3) via Terraform  
- **CI/CD:** GitHub Actions  
- **Security Tools:** Docker, Trivy, GitLeaks, CodeQL  
- **API:** Adzuna Job Search API → [developer.adzuna.com](https://developer.adzuna.com)

## 🔧 Getting Started  
### Prerequisites  
- Node.js or Python installed  
- Terraform (v1.x) installed  
- AWS CLI configured (if deploying to AWS)  
- Adzuna API Key & App ID (sign up at [Adzuna API](https://developer.adzuna.com))

### Local Setup  
```bash
git clone https://github.com/dgdemo/adzuna_job_search.git
cd adzuna_job_search

# Backend setup
cd backend
npm install            # or pip install -r requirements.txt  
cp .env.example .env    # fill in API keys & DB connection

# Frontend setup
cd ../frontend
npm install

# Run locally
npm run dev             # or equivalent command
