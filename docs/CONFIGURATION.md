# 🔧 Configuration Guide

## Environment Setup

SynaptiVerse uses environment variables for configuration. This keeps secrets safe and makes deployment flexible.

---

## Quick Start

### 1. Copy the Example File

```bash
cp .env.example .env
```

### 2. Edit `.env` with Your Settings

The `.env` file is already gitignored, so it's safe to add your secrets.

### 3. Use in Code

```python
from config import Config

# Access configuration
port = Config.PORT
debug = Config.DEBUG
agent_seed = Config.COORDINATOR_SEED
```

---

## Configuration Files

### `.env.example`
- **Purpose**: Template file with all available options
- **Git Tracked**: ✅ Yes (committed to repo)
- **Contains Secrets**: ❌ No (safe defaults only)
- **When to Use**: Copy to create your `.env` file

### `.env`
- **Purpose**: Your actual configuration with real values
- **Git Tracked**: ❌ No (in .gitignore)
- **Contains Secrets**: ✅ Can contain API keys, passwords, etc.
- **When to Use**: Local development, production deployment

---

## Key Configuration Sections

### 🖥️ Server Configuration

```bash
HOST=0.0.0.0          # Listen on all interfaces
PORT=8000             # Default port
DEBUG=True            # Enable debug mode (disable in production!)
ENVIRONMENT=development
```

**Production Settings**:
```bash
DEBUG=False
ENVIRONMENT=production
```

---

### 🤖 Fetch.ai Agent Configuration

```bash
# Agent seeds (change these for production!)
COORDINATOR_SEED=your_unique_coordinator_seed_here
ADVISOR_SEED=your_unique_advisor_seed_here

# Agentverse integration (optional)
AGENTVERSE_ENABLED=False
AGENTVERSE_MAILBOX_KEY=your_mailbox_key
AGENTVERSE_API_KEY=your_api_key
```

**How to Generate Secure Seeds**:
```bash
# Option 1: OpenSSL
openssl rand -hex 32

# Option 2: Python
python3 -c "import secrets; print(secrets.token_hex(32))"
```

**Agentverse Setup**:
1. Create account at https://agentverse.ai
2. Get mailbox key from dashboard
3. Set `AGENTVERSE_ENABLED=True`

---

### 🧠 MeTTa Configuration

```bash
METTA_KNOWLEDGE_PATH=src/metta/knowledge_graphs/medical_facts.metta
METTA_CACHE_ENABLED=True
METTA_MAX_FACTS=1000
```

**Custom Knowledge Base**:
```bash
# Use different knowledge file
METTA_KNOWLEDGE_PATH=data/custom_facts.metta
METTA_MAX_FACTS=5000
```

---

### 🌐 API Configuration

```bash
# CORS settings
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
CORS_ALLOW_CREDENTIALS=True

# Rate limiting
RATE_LIMIT_ENABLED=False
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60
```

**Production CORS**:
```bash
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com
```

**Enable Rate Limiting**:
```bash
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=60    # Max 60 requests
RATE_LIMIT_PERIOD=60      # Per 60 seconds
```

---

### 🏥 Healthcare Configuration

```bash
DEFAULT_APPOINTMENT_DURATION=30  # Minutes
TIMEZONE=UTC
EMERGENCY_NOTIFICATION_ENABLED=False
EMERGENCY_WEBHOOK_URL=
```

**Emergency Notifications**:
```bash
EMERGENCY_NOTIFICATION_ENABLED=True
EMERGENCY_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

---

### 🔒 Security Configuration

```bash
# Generate with: openssl rand -hex 32
SECRET_KEY=your_secret_key_here

# Privacy settings (DO NOT CHANGE!)
STORE_PHI=False           # Never store Protected Health Information
ENABLE_ANALYTICS=False    # No user tracking
```

**Important Security Notes**:
- ✅ Always change `SECRET_KEY` in production
- ❌ Never set `STORE_PHI=True` (violates privacy-first architecture)
- ✅ Use HTTPS in production
- ✅ Rotate secrets regularly

---

### 📝 Logging Configuration

```bash
LOG_LEVEL=INFO          # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=text         # text or json
LOG_FILE=logs/synaptiverse.log
```

**Production Logging**:
```bash
LOG_LEVEL=WARNING
LOG_FORMAT=json
LOG_FILE=/var/log/synaptiverse/app.log
```

---

### 🧪 Testing Configuration

```bash
TEST_MODE=False         # Skip external API calls
MOCK_AGENTS=False      # Use mock agents instead of real ones
```

**For Unit Testing**:
```bash
TEST_MODE=True
MOCK_AGENTS=True
```

---

## Configuration Validation

The `Config` class automatically validates settings on startup:

```python
from config import Config

# Check configuration
if Config.validate():
    print("✅ Configuration is valid")
else:
    print("❌ Configuration has errors")
    
# Print current config (no secrets shown)
Config.print_config()
```

**Example Output**:
```
============================================================
SYNAPTIVERSE CONFIGURATION
============================================================
Environment: development
Debug Mode: True
Server: 0.0.0.0:8000
MeTTa Facts: 1000
Agent Seeds: synaptiverse_local_c..., synaptiverse_local_a...
Agentverse: Disabled
PHI Storage: Disabled (Privacy-First)
Log Level: INFO
============================================================
```

---

## Environment-Specific Configs

### Development (`.env`)
```bash
DEBUG=True
ENVIRONMENT=development
LOG_LEVEL=DEBUG
AGENTVERSE_ENABLED=False
```

### Staging (`.env.staging`)
```bash
DEBUG=True
ENVIRONMENT=staging
LOG_LEVEL=INFO
AGENTVERSE_ENABLED=True
AGENTVERSE_MAILBOX_KEY=staging_key
```

### Production (`.env.production`)
```bash
DEBUG=False
ENVIRONMENT=production
LOG_LEVEL=WARNING
SECRET_KEY=production_secret_change_me
AGENTVERSE_ENABLED=True
AGENTVERSE_MAILBOX_KEY=production_key
```

**Load Specific Environment**:
```bash
# Development (default)
python3 src/agents/web_ui.py

# Staging
cp .env.staging .env
python3 src/agents/web_ui.py

# Production
cp .env.production .env
python3 src/agents/web_ui.py
```

---

## Docker Configuration

### Using .env with Docker Compose

```yaml
# docker-compose.yml
services:
  web:
    build: .
    env_file:
      - .env
    ports:
      - "${PORT}:${PORT}"
```

### Passing Environment Variables

```bash
# Option 1: From .env file
docker-compose up

# Option 2: Override specific values
PORT=9000 DEBUG=True docker-compose up

# Option 3: Using --env-file
docker run --env-file .env.production synaptiverse
```

---

## Troubleshooting

### Configuration Not Loading

**Problem**: Changes to `.env` not taking effect

**Solutions**:
1. Restart the server
2. Check for syntax errors in `.env`
3. Ensure no spaces around `=` sign
4. Check file encoding (should be UTF-8)

### Validation Errors

**Problem**: `SECRET_KEY must be changed in production`

**Solution**:
```bash
# Generate new secret key
openssl rand -hex 32

# Add to .env
SECRET_KEY=your_generated_key_here
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'config'`

**Solution**:
```python
# Add parent directory to path
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from config import Config
```

---

## Best Practices

### ✅ DO:
- Use `.env` for local development
- Copy `.env.example` to `.env` when setting up
- Change all default secrets in production
- Keep `.env` out of version control
- Use different seeds for each environment
- Validate configuration on startup
- Document custom environment variables

### ❌ DON'T:
- Commit `.env` to Git
- Share `.env` files (they contain secrets!)
- Hardcode secrets in source code
- Use default seeds in production
- Enable `STORE_PHI` (violates privacy architecture)
- Disable validation in production

---

## Quick Reference

| Variable | Default | Required | Description |
|----------|---------|----------|-------------|
| `HOST` | 0.0.0.0 | No | Server bind address |
| `PORT` | 8000 | No | Server port |
| `DEBUG` | False | No | Debug mode |
| `COORDINATOR_SEED` | default | Yes | Agent coordinator seed |
| `ADVISOR_SEED` | default | Yes | Agent advisor seed |
| `SECRET_KEY` | insecure | Yes (prod) | Session secret |
| `STORE_PHI` | False | **Must be False** | PHI storage (privacy) |
| `LOG_LEVEL` | INFO | No | Logging verbosity |

---

## Need Help?

- **Configuration Issues**: Check this guide
- **Security Questions**: See security best practices above
- **Agent Setup**: See Fetch.ai documentation
- **MeTTa Configuration**: See MeTTa documentation

---

**Last Updated**: 2025-01-22  
**Version**: 1.0.0
