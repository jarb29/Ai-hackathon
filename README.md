# Web Audit Agent

## Enterprise-Grade Autonomous Web Performance & Security Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Chrome DevTools MCP](https://img.shields.io/badge/Chrome%20DevTools-MCP-blue.svg)](https://github.com/ChromeDevTools/chrome-devtools-mcp)
[![OpenAI](https://img.shields.io/badge/OpenAI-Function--Calling-green.svg)](https://platform.openai.com/docs/guides/function-calling)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **Enterprise-grade autonomous AI system** that performs comprehensive web application audits through OpenAI function calling and Chrome DevTools MCP integration. Delivers actionable performance and security insights with executive-level reporting.

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 20+
- OpenAI API Key

### Installation

```bash
# Clone repository
git clone <repository-url>
cd Ai-hackathon

# Create environment file
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# Install dependencies
python3 -m venv .venv1
.venv1/bin/pip install -r requirements.txt
npm install -g @modelcontextprotocol/server-chrome-devtools

# Run application
PYTHONPATH=. .venv1/bin/python src/app/main.py
```

### Usage

```bash
# API Endpoint
curl -X POST "http://localhost:9000/api/audit" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# API Documentation
open http://localhost:9000/docs
```

## 🏗️ Architecture

Three-phase AI analysis:
1. **Tool Selection**: AI selects browser automation tools
2. **Technical Analysis**: Structured performance and security report
3. **Executive Summary**: Business impact and ROI assessment

## 📊 Features

- **Performance**: Core Web Vitals, Lighthouse scores
- **Security**: OWASP compliance, security headers
- **Executive Reporting**: Business impact analysis
- **Real Browser Data**: Chrome DevTools integration
- **Enterprise Ready**: FastAPI, Docker, CI/CD ready

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.9+
- **AI/LLM**: OpenAI GPT-4o-mini
- **Browser**: Chrome DevTools MCP
- **API**: REST with OpenAPI documentation

## 📁 Project Structure

```
Ai-hackathon/
├── src/                    # Backend application
│   ├── app/               # FastAPI routes
│   ├── business/          # Core audit logic
│   ├── clients/           # External service clients
│   ├── config/            # Configuration
│   ├── schemas/           # Data models
│   └── utils/             # Utilities
└── logs/                  # Application logs
```

## 🔧 Development

```bash
# Install dependencies
python3 -m venv .venv1
.venv1/bin/pip install -r requirements.txt

# Run locally
PYTHONPATH=. .venv1/bin/python src/app/main.py

# Clean up
rm -rf .venv1 __pycache__ .pytest_cache
find . -name "*.pyc" -delete
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Built with**: FastAPI, OpenAI, Chrome DevTools MCP | **Status**: Production Ready 🚀