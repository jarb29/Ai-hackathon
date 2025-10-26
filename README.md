# Web Audit Agent

## Enterprise-Grade Autonomous Web Performance & Security Auditor

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Chrome DevTools MCP](https://img.shields.io/badge/Chrome%20DevTools-MCP-blue.svg)](https://github.com/ChromeDevTools/chrome-devtools-mcp)
[![OpenAI](https://img.shields.io/badge/OpenAI-Function--Calling-green.svg)](https://platform.openai.com/docs/guides/function-calling)
[![Status: Production Ready](https://img.shields.io/badge/Status-Production%20Ready-brightgreen.svg)]()

> **Enterprise-grade autonomous AI system** that performs comprehensive web application audits through OpenAI function calling and Chrome DevTools MCP integration. Delivers actionable performance and security insights with executive-level reporting.

## 🏗️ System Architecture

```
┌─────────────────┐    ┌──────────────────┐
│   Web Interface │◀───│    FastAPI       │
│   Jinja2 + HTML │───▶│    /audit        │
│   Templates     │    │    REST API      │
└─────────────────┘    └──────────────────┘
                                │ ▲
                                ▼ │
                       ┌──────────────────┐
                       │  Audit Service   │
                       │  Business Logic  │
                       │                  │
                       └──────────────────┘
                                │ ▲
                                ▼ │
                       ┌──────────────────┐    ┌─────────────────────┐
                       │   LLM Client     │    │   MCP Tool Client   │
                       │   OpenAI API     │───▶│   JSON-RPC          │
                       │   GPT-4o-mini    │◀───│   Communication     │
                       │   3-Phase Calls  │    │                     │
                       └──────────────────┘    └─────────────────────┘
                                │ ▲                        │ ▲
                                │ │                        ▼ │
                                │ │            ┌─────────────────────┐
                                │ │            │  Chrome DevTools    │
                                │ │            │  MCP Server         │
                                │ │            │  (Node.js Process)  │
                                │ │            │                     │
                                │ │            │   Browser Tools:    │
                                │ │            │   • navigate_page   │
                                │ │            │   • performance_*   │
                                │ │            │   • evaluate_script │
                                │ │            │   • take_screenshot │
                                │ │            └─────────────────────┘
                                ▼ │
                       ┌──────────────────┐
                       │  Complete Report │
                       │  Technical +     │
                       │  Executive Data  │
                       └──────────────────┘
```

## 🧠 Three-Phase AI Architecture

### **OpenAI LLM Call Flow**

```
Phase 1: Function Calling
┌─────────────────────────────────────────────────────────────┐
│ OpenAI Call #1: Tool Selection                              │
│ ┌─────────────────┐    ┌─────────────────────────────────┐ │
│ │ System Prompt   │───▶│ AI selects browser tools        │ │
│ │ Web Audit Expert│    │ • navigate_page                 │ │
│ │ Persona         │    │ • performance_start_trace       │ │
│ └─────────────────┘    │ • evaluate_script               │ │
│                        │ • take_screenshot               │ │
│                        └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ Execute MCP Tools   │
                    │ Chrome DevTools     │
                    │ Browser Automation  │
                    └─────────────────────┘
                                │
                                ▼
Phase 2: Structured Analysis
┌─────────────────────────────────────────────────────────────┐
│ OpenAI Call #2: Technical Audit Report                     │
│ ┌─────────────────┐    ┌─────────────────────────────────┐ │
│ │ Tool Results    │───▶│ AI analyzes browser data        │ │
│ │ • Performance   │    │ • Core Web Vitals extraction   │ │
│ │ • Security      │    │ • Vulnerability assessment     │ │
│ │ • Network       │    │ • Technical recommendations    │ │
│ └─────────────────┘    │ • Structured JSON output       │ │
│                        └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
Phase 3: Executive Summary
┌─────────────────────────────────────────────────────────────┐
│ OpenAI Call #3: C-Suite Business Impact                    │
│ ┌─────────────────┐    ┌─────────────────────────────────┐ │
│ │ Technical Audit │───▶│ AI creates executive summary    │ │
│ │ Results         │    │ • Business impact assessment   │ │
│ │                 │    │ • ROI estimates & timelines    │ │
│ │                 │    │ • Risk prioritization          │ │
│ │                 │    │ • Investment recommendations   │ │
│ └─────────────────┘    └─────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌─────────────────────┐
                    │ Complete Report     │
                    │ Technical + Exec    │
                    │ Dual-Audience Value │
                    └─────────────────────┘
```

## 🎯 Core Value Proposition

### **Autonomous Intelligence**

- **Single Input**: Provide only a target URL
- **Zero Configuration**: Self-configuring AI analysis
- **Real Browser Data**: Live Chrome DevTools integration
- **Executive Interface**: Enterprise-grade web dashboard

### **Enterprise-Grade Analysis**

- **Performance Metrics**: Core Web Vitals, Lighthouse scores, TTFB analysis
- **Security Assessment**: OWASP Top 10, security headers, vulnerability scanning
- **Business Impact**: Risk-prioritized recommendations with ROI analysis
- **AI-Powered Insights**: Three-phase OpenAI analysis with executive reporting
- **Dual-Audience Reports**: Technical details + C-suite business summaries

### **Production Integration**

- **FastAPI Backend**: Enterprise-ready REST architecture
- **CI/CD Pipeline**: Automated quality gates and SLO enforcement
- **Executive Reporting**: C-suite ready dashboards and insights
- **Batch Processing**: Multi-site auditing capabilities

## 🛠️ Tools & Agent Capabilities

| Tool/Agent                  | Function                           | Technology               | Output                        |
| --------------------------- | ---------------------------------- | ------------------------ | ----------------------------- |
| **navigate_page**           | Load website and capture metrics   | Chrome DevTools MCP      | Navigation data, page info    |
| **performance_start_trace** | Begin performance measurement      | Chrome DevTools API      | Core Web Vitals tracking      |
| **performance_stop_trace**  | End performance measurement        | Chrome DevTools API      | Performance metrics           |
| **evaluate_script**         | Run JavaScript for security checks | Chrome DevTools Runtime  | Security headers, HTTPS       |
| **list_network_requests**   | Analyze HTTP requests and headers  | Network domain API       | Security headers, performance |
| **take_screenshot**         | Visual page state capture          | Page.captureScreenshot   | Visual validation             |
| **list_console_messages**   | Monitor JS errors/warnings         | Runtime.consoleAPICalled | Error detection               |
| **🤖 AI Audit Agent**       | Comprehensive web analysis         | OpenAI 3-Phase + MCP     | Technical + Executive Reports |

## 📊 Comprehensive Audit Coverage

### **Performance Indicators**

- Core Web Vitals (LCP, FID, CLS, INP)
- Lighthouse Performance Score
- Time to First Byte (TTFB)
- First Contentful Paint (FCP)
- Time to Interactive (TTI)
- Resource optimization analysis
- Console error detection

### **Security Assessment**

- HTTPS validation and TLS configuration
- Security headers (CSP, HSTS, X-Frame-Options)
- OWASP Top 10 vulnerability scanning
- Network request security analysis
- Certificate validation
- Attack surface analysis

## 🚀 Quick Start Guide

### **Prerequisites**

- **Python 3.9+** with pip
- **Node.js 20+** (for Chrome DevTools MCP server)
- **OpenAI API Key** with GPT-4 access

### **Core Dependencies**

- **OpenAI**: GPT-4o integration with function calling
- **FastAPI**: High-performance web framework
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment
- **Jinja2**: Template engine for web interface
- **Chrome DevTools MCP**: Browser automation protocol

### **Installation**

#### **Option 1: Docker (Recommended)**

```bash
# Clone repository
git clone <repository-url>
cd Ai-hackathon

# Configure environment
echo "OPENAI_API_KEY=your-key-here" > .env

# Build and start (single command)
make docker-up

# Other Docker commands
make docker-down    # Stop containers
make docker-clean   # Remove containers and images
make docker-logs    # Show container logs
make docker-fix     # Nuclear reset for Docker issues
```

#### **Option 2: Local Development**

```bash
# Clone repository
git clone <repository-url>
cd Ai-hackathon

# Install dependencies
make install

# Configure environment
echo "OPENAI_API_KEY=your-key-here" > .env

# Start the application
make run
```

### **Usage Options**

#### **Web Interface**

```bash
# Access professional dashboard
open http://localhost:9000
```

#### **REST API**

```bash
# Direct API call
curl -X POST "http://localhost:9000/audit" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# API documentation
open http://localhost:9000/docs
```

#### **Python API**

```python
# Direct API usage
import requests

response = requests.post("http://localhost:9000/audit",
    json={"url": "https://your-target-site.com"})
result = response.json()

print(f"Performance Score: {result['performance']['lighthouse_score']}")
print(f"Security Risk: {result['security']['risk_level']}")
print(f"Executive Summary: {result['executive_summary']['business_impact']}")
print(f"Investment Priority: {result['executive_summary']['investment_priority']}")
```

## 📁 Project Architecture

```
Ai-hackathon/
├── 🏗️ src/                         # Production backend
│   ├── app/                        # FastAPI application
│   │   ├── routes/                 # API endpoints
│   │   │   ├── audit.py            # Web audit REST endpoint
│   │   │   └── health.py           # Health check endpoint
│   │   └── main.py                 # FastAPI app setup & configuration
│   ├── business/                   # Core audit logic
│   │   └── audit_logic.py          # AuditService orchestration
│   ├── clients/                    # External service clients
│   │   ├── llm_client.py           # OpenAI GPT-4o integration
│   │   ├── mcp_tool_client.py      # Chrome DevTools MCP client
│   │   └── service_factory.py      # Dependency injection factory
│   ├── config/                     # Configuration management
│   │   ├── config.py               # Application settings (Pydantic)
│   │   └── logging_config.py       # Multi-file logging setup
│   ├── schemas/                    # Pydantic data models
│   │   ├── requests.py             # API request validation
│   │   └── responses.py            # Audit response structure
│   ├── prompts/                    # LLM prompt templates
│   │   └── prompts.py              # OpenAI system & user prompts
│   ├── helpers/                    # Utilities and validators
│   │   ├── exceptions.py           # Custom exception classes
│   │   └── validators.py           # URL validation logic
│   ├── middleware/                 # HTTP middleware
│   │   └── logging_middleware.py   # Request/response logging
│   └── utils/                      # Utilities and tools
│       ├── logger.py               # Centralized logging setup
│       ├── log_context.py          # Correlation ID & performance tracking
│       └── mcp_tools_exporter.py   # MCP tools documentation utility
├── 🌐 frontend/                    # Web interface
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── base.html               # Base template layout
│   │   ├── index.html              # Landing page
│   │   ├── dashboard.html          # Audit dashboard
│   │   └── report.html             # Audit results display
│   ├── static/                     # Static assets
│   │   ├── css/                    # Stylesheets
│   │   ├── js/                     # JavaScript files
│   │   └── images/                 # Image assets
│   └── routes/                     # Web routes
│       └── web.py                  # Frontend route handlers
├── 🐳 docker/                      # Docker configuration
│   ├── mcp-service.js              # Node.js MCP HTTP service
│   └── package.json                # Node.js dependencies
├── 📊 logs/                        # Application logs
│   ├── app.log                     # General application logs
│   ├── error.log                   # Error and exception logs
│   ├── metrics.log                 # Business metrics (METRIC level)
│   └── debug.log                   # Development debugging logs
├── .env                            # Environment variables
├── Makefile                        # Streamlined development commands
├── docker-compose.dev.yml          # Multi-container orchestration
├── Dockerfile.api                  # FastAPI service container
├── Dockerfile.mcp                  # Chrome MCP service container
├── pyproject.toml                  # Project configuration & dependencies
└── README.md                       # Project documentation
```

## 🎯 Use Case Scenarios

### **Development Teams**

- Pre-deployment validation with real browser data
- Performance regression detection
- Security compliance verification

### **DevOps & SRE**

- CI/CD integration with FastAPI endpoints
- SLO monitoring with automated thresholds
- Incident prevention through proactive scanning

### **Executive Leadership**

- Enterprise-grade audit intelligence
- Risk assessment with business impact quantification
- Strategic planning with performance investment ROI

## 🔧 Technical Stack

### **Core Technologies**

- **Backend**: FastAPI, Python 3.9+
- **AI/LLM**: OpenAI GPT-4o with function calling
- **Browser Automation**: Chrome DevTools MCP + Node.js
- **Frontend**: Jinja2 templates, HTML/CSS
- **Data Validation**: Pydantic schemas
- **Protocol**: JSON-RPC for MCP communication

### **Architecture Patterns**

- Clean dependency injection
- Three-phase AI analysis pipeline
- Real-time browser integration
- Executive-grade reporting

### **Docker Implementation**

- **Multi-stage builds**: Optimized Alpine Linux images
- **Service orchestration**: Docker Compose with health checks
- **Development workflow**: Streamlined Make commands
- **Production ready**: Proper networking and volume management

## 🚀 Make Commands

```bash
# Development
make install      # Install dependencies
make run          # Start application locally
make stop         # Stop application
make clean        # Clean build artifacts

# Docker
make docker-up    # Build and start containers
make docker-down  # Stop containers
make docker-clean # Remove containers and images
make docker-logs  # Show container logs
make docker-fix   # Nuclear reset for Docker issues
```

---

**Status**: Production Ready | **License**: MIT | **Built with**: FastAPI, OpenAI, Chrome DevTools MCP

_Enterprise-grade web auditing with executive-level intelligence_ 🏛️mance web framework
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for production deployment
- **Jinja2**: Template engine for web interface
- **Chrome DevTools MCP**: Browser automation protocol

### **Installation**

#### **Option 1: Docker (Recommended)**

```bash
# Clone repository
git clone <repository-url>
cd AiHackanton

# Configure environment
echo "OPENAI_API_KEY=your-key-here" > .env

# Build and start with Docker
make docker-build
make docker-up

# Other Docker commands
make docker-down    # Stop containers
make docker-clean   # Remove containers and images
make docker-logs    # Show container logs
```

#### **Option 2: Local Development**

```bash
# Clone repository
git clone <repository-url>
cd AiHackanton

# Create virtual environment
python3 -m venv .venv1
source .venv1/bin/activate  # On Windows: .venv1\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies (for Chrome DevTools MCP)
npm install -g @modelcontextprotocol/server-chrome-devtools

# Configure environment
echo "OPENAI_API_KEY=your-key-here" > .env

# Start the application
make run
# OR manually: PYTHONPATH=. python src/app/main.py
```

### **Usage Options**

#### **Quick Start with Docker**

```bash
# Start everything
make docker-up

# Access web interface
open http://localhost:9000
```

#### **Web Interface**

```bash
# Access professional dashboard
open http://localhost:9000
```

#### **REST API**

```bash
# Direct API call
curl -X POST "http://localhost:9000/audit" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'

# API documentation
open http://localhost:9000/docs
```

#### **Python API**

```python
# Direct API usage
import requests

response = requests.post("http://localhost:9000/audit",
    json={"url": "https://your-target-site.com"})
result = response.json()

print(f"Performance Score: {result['performance']['lighthouse_score']}")
print(f"Security Risk: {result['security']['risk_level']}")
print(f"Executive Summary: {result['executive_summary']['business_impact']}")
print(f"Investment Priority: {result['executive_summary']['investment_priority']}")
```

## 📁 Project Architecture

```
AiHackanton/
├── 🏗️ src/                         # Production backend
│   ├── app/                        # FastAPI application
│   │   ├── routes/                 # API endpoints
│   │   │   ├── audit.py            # Web audit REST endpoint
│   │   │   └── health.py           # Health check endpoint
│   │   └── main.py                 # FastAPI app setup & configuration
│   ├── business/                   # Core audit logic
│   │   └── audit_logic.py          # AuditService orchestration
│   ├── clients/                    # External service clients
│   │   ├── llm_client.py           # OpenAI GPT-4o-mini integration
│   │   ├── mcp_tool_client.py      # Chrome DevTools MCP client
│   │   └── service_factory.py      # Dependency injection factory
│   ├── config/                     # Configuration management
│   │   ├── config.py               # Application settings (Pydantic)
│   │   └── logging_config.py       # Multi-file logging setup
│   ├── schemas/                    # Pydantic data models
│   │   ├── requests.py             # API request validation
│   │   └── responses.py            # Audit response structure
│   ├── prompts/                    # LLM prompt templates
│   │   └── prompts.py              # OpenAI system & user prompts
│   ├── helpers/                    # Utilities and validators
│   │   ├── exceptions.py           # Custom exception classes
│   │   └── validators.py           # URL validation logic
│   ├── middleware/                 # HTTP middleware
│   │   └── logging_middleware.py   # Request/response logging
│   └── utils/                      # Utilities and tools
│       ├── logger.py               # Centralized logging setup
│       ├── log_context.py          # Correlation ID & performance tracking
│       └── mcp_tools_exporter.py   # MCP tools documentation utility
├── 🌐 frontend/                    # Web interface
│   ├── templates/                  # Jinja2 HTML templates
│   │   ├── base.html               # Base template layout
│   │   ├── index.html              # Landing page
│   │   ├── dashboard.html          # Audit dashboard
│   │   └── report.html             # Audit results display
│   ├── static/                     # Static assets
│   │   ├── css/                    # Stylesheets
│   │   ├── js/                     # JavaScript files
│   │   └── images/                 # Image assets
│   └── routes/                     # Web routes
│       └── web.py                  # Frontend route handlers
├── 📊 logs/                        # Application logs
│   ├── app.log                     # General application logs
│   ├── error.log                   # Error and exception logs
│   ├── metrics.log                 # Business metrics (METRIC level)
│   └── debug.log                   # Development debugging logs
├── .env                            # Environment variables
├── pyproject.toml                  # Project configuration & dependencies
└── README.md                       # Project documentation
```

## 🎯 Use Case Scenarios

### **Development Teams**

- Pre-deployment validation with real browser data
- Performance regression detection
- Security compliance verification

### **DevOps & SRE**

- CI/CD integration with FastAPI endpoints
- SLO monitoring with automated thresholds
- Incident prevention through proactive scanning

### **Executive Leadership**

- Enterprise-grade audit intelligence
- Risk assessment with business impact quantification
- Strategic planning with performance investment ROI

## 🔧 Technical Stack

### **Core Technologies**

- **Backend**: FastAPI, Python 3.9+
- **AI/LLM**: OpenAI GPT-4o-mini with function calling
- **Browser Automation**: Chrome DevTools MCP + Node.js
- **Frontend**: Jinja2 templates, HTML/CSS
- **Data Validation**: Pydantic schemas
- **Protocol**: JSON-RPC for MCP communication

### **Architecture Patterns**

- Clean dependency injection
- Single-agent AI analysis
- Real-time browser integration
- Executive-grade reporting

---

**Status**: Production Ready | **License**: MIT | **Built with**: FastAPI, OpenAI, Chrome DevTools MCP

_Single-agent web auditing with enterprise-grade intelligence_ 🤖

_Enterprise-grade web auditing with executive-level intelligence_ 🏛️
