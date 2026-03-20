# Technical Debt Tracker

![CI Status](https://github.com/sukritjain18/devops-project-technical-debt-tracker/actions/workflows/ci-cd.yml/badge.svg)
![Test Coverage](coverage.svg)
![License](https://img.shields.io/github/license/sukritjain18/devops-project-technical-debt-tracker)

---

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
- Ensure application reliability using automated testing  

### Key Features
- Debt scoring of codebases  
- Dashboard visualization  
- Alerts for increasing debt  
- Automated testing integrated with CI/CD  

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
- Testing: Pytest, Selenium  

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
├── README.md                     # Project overview & instructions
├── .gitignore                     # Git ignore rules
├── LICENSE                        # MIT License
│
├── src/                           # Application source code
│   ├── app.py                     # Flask app entrypoint
│   ├── __init__.py                # Initialize app
│   ├── config/                    # App configuration files
│   ├── scripts/                   # Helper / setup scripts
│   └── tests/                     # Internal tests for app components
│
├── tests/                         # External test suites
│   ├── unit/                      # Unit tests (Pytest)
│   ├── integration/               # Integration tests
│   └── selenium/                  # Selenium browser tests
│
├── infrastructure/                # Docker / DevOps / deployment configs
├── pipelines/                     # CI/CD workflow configurations
├── monitoring/                    # Monitoring & alert configs (Nagios)
├── docs/                          # Project documentation & diagrams
├── presentations/                 # Presentation slides / visuals
└── deliverables/                  # Submission-ready files
```

---

## Testing

Automated testing is implemented to ensure that the application works correctly and that future changes do not break existing functionality.

### Unit Testing
- Implemented using **Pytest**
- Tests verify individual components and API responses.

Run tests locally:

```bash
pytest
```

### Integration Testing
- Ensures that different components of the system work together correctly.
- Validates interaction between the Flask API and application logic.

### End-to-End Testing
- Implemented using **Selenium**
- Simulates browser interaction to verify that the application runs correctly from a user perspective.

### CI/CD Test Integration
All tests run automatically in the **GitHub Actions CI/CD pipeline** whenever code is pushed or a pull request is created.  
If any test fails, the pipeline stops, ensuring only stable code is merged into the `main` branch.

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
4. End-to-End Testing  
5. Security Scan  
6. Deployment (if configured)

### Trigger Conditions
- Push to main branch  
- Pull Request to main branch  

---

## Monitoring & Logging

### Monitoring Setup
- Tool: **Nagios**  
- Host: `devops-app` (Technical Debt Tracker)  
- Services monitored: HTTP endpoint, CPU load, Disk usage  
- Alerts triggered for:
  1. CPU usage exceeds 80%
  2. Disk usage exceeds 85%
  3. Application HTTP endpoint becomes unreachable
  4. Application response time exceeds 2 seconds

### Alerts & Notification Channels
- Email notifications  

### Logging
- Logs stored in `logs/` directory  
- Structured JSON logging  
- Log Rotation: Daily  
- Retention Period: 30 days (older logs automatically deleted)  

### Kubernetes Deployment

```powershell
# Check Cluster Status
# View cluster info
kubectl cluster-info

# List all nodes
kubectl get nodes

# Apply Kubernetes Manifests
# Apply all manifests in your Kubernetes folder
kubectl apply -f C:\Users\DELL\OneDrive\Documents\GitHub\devops-project-technical-debt-tracker\infrastructure\kubernetes

# Verify deployments, services, pods, and all resources
kubectl get deploy,svc,pods
kubectl get all
# Note: If the output says unchanged, your resources are already applied and up-to-date.

# Access the Application
# Use port-forwarding to access locally
kubectl port-forward svc/technical-debt-tracker-service 8080:8080

# Web Interface: http://localhost:8080
# API: http://localhost:8080/api
# Recommended: Use port-forwarding for local clusters like Minikube or Docker Desktop. NodePort may not work reliably on Windows.

# Debugging Pods
# List all pods in all namespaces
kubectl get pods --all-namespaces

# View logs for a specific pod
kubectl logs <pod-name>

# Describe pod for detailed info
kubectl describe pod <pod-name>

# Delete Resources (Optional)
# Delete all deployed resources from the Kubernetes folder
kubectl delete -f C:\Users\DELL\OneDrive\Documents\GitHub\devops-project-technical-debt-tracker\infrastructure\kubernetes

**Purpose:**  
Maintain observability of the application while preventing excessive storage usage.  

---

## License

This project is licensed under the MIT License.