# Contributing to SynaptiVerse

Thank you for your interest in contributing to SynaptiVerse! This document provides guidelines for contributions.

## 🚀 Quick Start

1. **Fork the repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/yourusername/synaptiVerse.git
   cd synaptiVerse
   ```
3. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**
5. **Run tests**
   ```bash
   pytest tests/ -v
   ```
6. **Commit and push**
   ```bash
   git commit -m "feat: Add your feature"
   git push origin feature/your-feature-name
   ```
7. **Open a Pull Request**

## 🧪 Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install pytest pytest-asyncio pytest-cov black flake8 mypy

# Run tests
pytest tests/ -v
```

## 📝 Commit Message Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `test:` Adding or updating tests
- `refactor:` Code refactoring
- `style:` Code style changes (formatting)
- `chore:` Maintenance tasks

**Examples:**
```
feat: Add multi-language symptom support
fix: Resolve MeTTa query timeout issue
docs: Update deployment guide
test: Add E2E test for emergency routing
```

## 🧹 Code Style

We use **Black** for code formatting and **flake8** for linting:

```bash
# Format code
black src/ tests/

# Check linting
flake8 src/ tests/ --max-line-length=100
```

## ✅ Testing Requirements

- All new features must include tests
- Maintain or improve code coverage
- Run full test suite before PR:
  ```bash
  pytest tests/ --cov=src
  ```

## 🔍 Pull Request Process

1. Update README.md if needed
2. Update documentation in `docs/`
3. Add tests for new functionality
4. Ensure all tests pass
5. Request review from maintainers

## 🐛 Reporting Bugs

Use GitHub Issues with:
- Clear title
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Relevant logs

## 💡 Feature Requests

We welcome feature ideas! Please:
- Check existing issues first
- Describe the use case
- Explain expected behavior
- Consider implementation approach

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Thank You!

Your contributions make SynaptiVerse better for everyone!
