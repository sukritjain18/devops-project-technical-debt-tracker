# Technical Debt Tracker

![CI Status](https://github.com/sukritjain18/devops-project-technical-debt-tracker/actions/workflows/ci-cd.yml/badge.svg)


**Student Name:** Sukrit Jain  
**Registration No:** 23fe10cse00089  
**Course:** CSE3253 DevOps [PE6]  
**Semester:** VI (2025-2026)  
**Project Type:** CI/CD & Monitoring  
**Difficulty:** Intermediate  

---

## Project Overview

### Problem Statement
Track, quantify, and visualize technical debt in DevOps pipelines to reduce risk and improve maintainability.

### Objectives
- Identify technical debt in code repositories  
- Visualize debt trends over time  
- Integrate with CI/CD pipelines for real-time feedback  

### Key Features
- Debt scoring of codebases  
- Dashboard visualization  
- Alerts for increasing debt  

---

## Technology Stack

### Core Technologies
- Programming Language: Python  
- Framework: Flask  
- Database: SQLite  

### DevOps Tools
- Version Control: Git  
- CI/CD: GitHub Actions  
- Containerization: Docker  
- Monitoring: Prometheus & Grafana  

---

## Getting Started

### Prerequisites
- [ ] Docker Desktop v20.10+  
- [ ] Git 2.30+  
- [ ] Python 3.8+  

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/sukritjain18/devops-project-technical-debt-tracker.git
cd devops-project-technical-debt-tracker
```

### 2. Run Using Docker (Recommended)

```bash
docker-compose up --build
```

### 3. Access the Application

- Web Interface: http://localhost:8080  
- API: http://localhost:8080/api  

---

## Alternative Installation (Without Docker)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run Flask application
python src/app.py
```

---

## Project Structure

```
devops-project-technical-debt-tracker/
│
├── README.md
├── .gitignore
├── LICENSE
│
├── src/                     # Application source code
├── docs/                    # Documentation files
├── infrastructure/          # Docker / IaC configurations
├── pipelines/               # CI/CD configurations
├── tests/                   # Test suites
├── monitoring/              # Monitoring & alert configs
├── presentations/           # Presentation materials
└── deliverables/            # Final submission files
```

---

## Configuration

### Environment Variables

Create a `.env` file in the root directory:

```
APP_ENV=development
DB_HOST=localhost
DB_PORT=5432
API_KEY=your_api_key_here
```

---

## CI/CD Pipeline

### Workflow File
`.github/workflows/ci-cd.yml`

### Pipeline Stages
1. Code Quality Check (Linting & Static Analysis)  
2. Build (Docker Image Build)  
3. Unit Testing  
4. Security Scan  
5. Deployment (if configured)

### Trigger Conditions
- Push to main branch  
- Pull Request to main branch  

---

## Monitoring

- Prometheus for metrics collection  
- Grafana for dashboard visualization  
- Alert rules for detecting increasing technical debt  

---

## License

This project is licensed under the MIT License.