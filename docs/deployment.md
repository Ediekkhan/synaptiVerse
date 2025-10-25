# SynaptiVerse - Deployment Guide

**Production Deployment Instructions**  
**ASI Alliance Hackathon Submission**

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Docker Deployment](#docker-deployment)
4. [Agentverse Registration](#agentverse-registration)
5. [Cloud Deployment](#cloud-deployment)
6. [Monitoring & Maintenance](#monitoring--maintenance)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

- **Python 3.10 or higher**
- **pip** (Python package manager)
- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**

### Required Accounts

- **Agentverse Account** - [Register here](https://agentverse.ai)
- **GitHub Account** - For repository access
- **Cloud Provider Account** (for production) - AWS, GCP, or Azure

### System Requirements

**Minimum (Development):**
- CPU: 2 cores
- RAM: 4 GB
- Disk: 10 GB free space
- Network: Internet connection

**Recommended (Production):**
- CPU: 4+ cores
- RAM: 8+ GB
- Disk: 50 GB SSD
- Network: 100 Mbps+

---

## Local Development Setup

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/synaptiVerse.git
cd synaptiVerse
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your values
nano .env  # or use your preferred editor
```

**Required environment variables:**

```env
# Agent Seeds (generate unique seeds)
COORDINATOR_SEED=your_unique_coordinator_seed_phrase_here
ADVISOR_SEED=your_unique_advisor_seed_phrase_here

# Agentverse Configuration
AGENTVERSE_API_KEY=your_agentverse_api_key

# Optional
LOG_LEVEL=INFO
AGENTVERSE_URL=https://agentverse.ai
```

**Generate unique seeds:**

```python
import secrets
print(f"Coordinator seed: {secrets.token_urlsafe(32)}")
print(f"Advisor seed: {secrets.token_urlsafe(32)}")
```

### Step 5: Test MeTTa Knowledge Graph

```bash
# Test MeTTa interface independently
python src/metta/metta_interface.py
```

Expected output:
```
=== Test 1: Flu symptoms ===
{
  "status": "success",
  "identified_symptoms": ["fever", "headache", "body_aches"],
  "possible_conditions": [...]
}
```

### Step 6: Run Agents Locally

**Terminal 1 - Appointment Coordinator:**
```bash
python src/agents/appointment_coordinator.py
```

Expected output:
```
============================================================
🚀 APPOINTMENT COORDINATOR AGENT STARTED
============================================================
Agent Name: appointment-coordinator
Agent Address: agent1q...
Chat Protocol: ENABLED
Manifest Publishing: ENABLED
============================================================
```

**Terminal 2 - Medical Advisor:**
```bash
python src/agents/medical_advisor.py
```

Expected output:
```
============================================================
🚀 MEDICAL ADVISOR AGENT STARTED
============================================================
Agent Name: medical-advisor
Agent Address: agent1q...
MeTTa Knowledge Graph: LOADED
============================================================
```

### Step 7: Run Tests

```bash
# Run E2E tests
python tests/e2e_scenarios.py

# Or use pytest
pytest tests/ -v

# With coverage
pytest tests/ --cov=src --cov-report=html
```

---

## Docker Deployment

### Step 1: Build Docker Images

```bash
# Build images
docker-compose build

# Verify images built successfully
docker images | grep synaptiverse
```

### Step 2: Configure Environment

Ensure `.env` file is properly configured (see Local Setup Step 4).

### Step 3: Start Services

```bash
# Start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Check service status
docker-compose ps
```

Expected output:
```
NAME                  STATUS              PORTS
appointment-coordinator   Up 10 seconds       8000/tcp
medical-advisor           Up 10 seconds       8001/tcp
```

### Step 4: Verify Agents Running

```bash
# Check coordinator logs
docker-compose logs coordinator | grep "STARTED"

# Check advisor logs
docker-compose logs advisor | grep "STARTED"
```

### Step 5: Stop Services

```bash
# Stop all services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

---

## Agentverse Registration

### Step 1: Create Agentverse Account

1. Visit [https://agentverse.ai](https://agentverse.ai)
2. Sign up / Log in
3. Navigate to "My Agents"

### Step 2: Get Agent Addresses

When agents start, they print their addresses:

```bash
# From agent logs
docker-compose logs coordinator | grep "Agent address"
# Output: Agent address: agent1qxxx...

docker-compose logs advisor | grep "Agent address"
# Output: Agent address: agent1qyyy...
```

**Save these addresses** - you'll need them!

### Step 3: Register Coordinator Agent

1. In Agentverse UI, click "Add Agent"
2. Enter agent details:
   - **Name:** `appointment-coordinator`
   - **Address:** `agent1qxxx...` (from logs)
   - **Endpoint:** `http://your-server-ip:8000/submit`
   
3. Upload manifest:
   - Upload `agent-manifests/coordinator_manifest.yaml`
   
4. Enable Chat Protocol:
   - Check "Chat Protocol Enabled"
   - Set content type: `text/plain, application/json`
   
5. Add tags:
   - `innovationlab`
   - `hackathon`
   - `healthcare`
   
6. Click "Register Agent"

### Step 4: Register Advisor Agent

Repeat Step 3 with:
- **Name:** `medical-advisor`
- **Address:** `agent1qyyy...` (from logs)
- **Endpoint:** `http://your-server-ip:8001/submit`
- **Manifest:** `agent-manifests/advisor_manifest.yaml`

### Step 5: Verify Registration

1. In Agentverse, navigate to "Agent Discovery"
2. Search for your agents by name
3. Verify they appear with "Active" status
4. Test Chat Protocol:
   - Click on agent
   - Send test message: "Hello"
   - Verify agent responds

### Step 6: Update README

Update README.md with your agent addresses:

```markdown
### Appointment Coordinator Agent
- **Agentverse Address**: `agent1qxxx...` ✅

### Medical Advisor Agent
- **Agentverse Address**: `agent1qyyy...` ✅
```

---

## Cloud Deployment

### Option 1: AWS EC2

#### Launch Instance

```bash
# Instance type: t3.medium or larger
# AMI: Ubuntu 22.04 LTS
# Storage: 30 GB GP3
# Security Group: Allow ports 8000, 8001, 22
```

#### Deploy Application

```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-ip

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Clone and deploy
git clone https://github.com/yourusername/synaptiVerse.git
cd synaptiVerse
cp .env.example .env
nano .env  # Configure

# Start services
docker-compose up -d
```

### Option 2: Google Cloud Run

```bash
# Build and push images
docker build -t gcr.io/your-project/coordinator:latest -f Dockerfile .
docker push gcr.io/your-project/coordinator:latest

# Deploy to Cloud Run
gcloud run deploy appointment-coordinator \
  --image gcr.io/your-project/coordinator:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

### Option 3: Kubernetes

```yaml
# k8s-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: appointment-coordinator
spec:
  replicas: 3
  selector:
    matchLabels:
      app: coordinator
  template:
    metadata:
      labels:
        app: coordinator
    spec:
      containers:
      - name: coordinator
        image: synaptiverse/coordinator:latest
        ports:
        - containerPort: 8000
        env:
        - name: COORDINATOR_SEED
          valueFrom:
            secretKeyRef:
              name: agent-secrets
              key: coordinator-seed
```

Deploy:
```bash
kubectl apply -f k8s-deployment.yaml
kubectl apply -f k8s-service.yaml
```

---

## Monitoring & Maintenance

### Health Checks

```bash
# Check agent health
curl http://localhost:8000/health
curl http://localhost:8001/health
```

### Log Monitoring

```bash
# Real-time logs
docker-compose logs -f

# Filter by service
docker-compose logs -f coordinator
docker-compose logs -f advisor

# Save logs to file
docker-compose logs > logs/$(date +%Y%m%d).log
```

### Performance Monitoring

```bash
# Container resource usage
docker stats

# Specific service
docker stats appointment-coordinator
```

### Automated Monitoring (Production)

**Use Prometheus + Grafana:**

```yaml
# docker-compose.override.yml
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Backup & Recovery

**Backup agent configuration:**
```bash
# Backup .env and manifests
tar -czf backup-$(date +%Y%m%d).tar.gz .env agent-manifests/

# Store securely (encrypted)
gpg -c backup-$(date +%Y%m%d).tar.gz
```

**Recovery:**
```bash
# Restore from backup
gpg -d backup-20251022.tar.gz.gpg | tar -xz
docker-compose up -d
```

---

## Troubleshooting

### Issue: Agent Not Starting

**Symptom:** Agent exits immediately after start

**Solutions:**
```bash
# Check logs for errors
docker-compose logs coordinator

# Common causes:
1. Invalid SEED in .env
2. Port already in use
3. Missing dependencies

# Verify environment
docker-compose config

# Restart with fresh state
docker-compose down -v
docker-compose up -d
```

### Issue: Chat Protocol Not Working

**Symptom:** Agent doesn't respond to messages

**Solutions:**
```bash
# Verify manifest published
# Check agent logs for "Manifest Publishing: ENABLED"

# Test locally first
python -c "from uagents_core.contrib.protocols.chat import chat_protocol_spec; print(chat_protocol_spec)"

# Check Agentverse registration
# Ensure endpoint is accessible: http://your-ip:8000/submit
```

### Issue: MeTTa Queries Failing

**Symptom:** "No reasoning path found"

**Solutions:**
```bash
# Test MeTTa interface
python src/metta/metta_interface.py

# Verify knowledge graph loaded
python -c "from src.metta import get_metta_knowledge_graph; kg = get_metta_knowledge_graph(); print(f'{len(kg.knowledge_base)} facts loaded')"

# Check symptom keywords
# Ensure inputs match expected format (lowercase, underscore-separated)
```

### Issue: High Memory Usage

**Symptom:** Container using >2GB RAM

**Solutions:**
```bash
# Limit container resources
# Add to docker-compose.yml:
services:
  coordinator:
    deploy:
      resources:
        limits:
          memory: 1G
        reservations:
          memory: 512M
```

### Issue: Can't Connect from ASI:One

**Symptom:** Messages sent from ASI:One don't reach agent

**Solutions:**
```bash
# Check firewall
sudo ufw allow 8000
sudo ufw allow 8001

# Verify endpoint accessible
curl http://your-public-ip:8000/submit

# Check Agentverse endpoint configuration
# Must be public IP or domain, not localhost

# Use ngrok for testing
ngrok http 8000
# Update Agentverse endpoint to ngrok URL
```

### Getting Help

**Resources:**
- [Fetch.ai Documentation](https://docs.fetch.ai)
- [uAgents GitHub](https://github.com/fetchai/uAgents)
- [SingularityNET Docs](https://singularitynet.io/docs)
- [Agentverse Support](https://agentverse.ai/support)

**Report Issues:**
- GitHub Issues: [github.com/yourusername/synaptiVerse/issues](https://github.com/yourusername/synaptiVerse/issues)

---

## Production Checklist

Before going to production:

- [ ] Unique agent seeds generated and secured
- [ ] Environment variables properly configured
- [ ] HTTPS enabled for endpoints
- [ ] Firewall rules configured
- [ ] Monitoring and alerting set up
- [ ] Backup strategy implemented
- [ ] Agents registered on Agentverse
- [ ] Chat Protocol tested end-to-end
- [ ] All E2E tests passing
- [ ] Documentation reviewed and updated
- [ ] Security audit completed
- [ ] Compliance review (HIPAA if applicable)
- [ ] Incident response plan documented
- [ ] Team trained on operations

---

**Last Updated:** October 2025  
**Version:** 1.0.0  
**Authors:** SynaptiVerse Team
