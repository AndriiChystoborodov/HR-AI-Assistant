[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/GlQxzqll)

# 🌿 Project GreenLeaf: Enterprise AI HR Agent (Basel Ops)

## Team: GreenLeaf AI | Track: Guided Lab (Weeks 1-4)

### 1. Project Overview

This repository contains the logic, data governance, and integration architecture for the GreenLeaf Logistics AI HR Agent. Our goal is to automate the Tier-1 support triage for GreenLeaf employees - it must be accurate, persistent, and secure. We built a production-ready Web UI that manages HR knowledge across three domains: Policies, Holidays (Live API), and Python Logic.

### 2. 🛠 Tech Stack 

Component | Description
-- | --
Interface | WebUI, Angular
AI Brain | Gemini 2.5 Flash
Orchestration | LangChain Agent
External API | OpenHolidays API
Back-end | Python Scripts
Data | Handbook markdown, Employee data injected in context
Documentation | GitHub Wiki (Technical Specs)

---

### 2.1 Actual Technologies & Dependencies

#### Backend Dependencies
- **FastAPI** - Modern web framework for building APIs
- **Uvicorn** - ASGI server for running FastAPI
- **LangChain** - Agent orchestration and tool management
- **LangChain OpenRouter** - LLM integration via OpenRouter API
- **Requests** - HTTP client for external APIs
- **Spacy 3.8.0** - NLP for entity recognition and text processing
- **python-dotenv** - Environment variable management
- **CORS Middleware** - Cross-Origin Resource Sharing for frontend-backend communication

#### Frontend Dependencies
- **Angular 19.2.0** - Modern web framework with TypeScript
- **RxJS 7.8.0** - Reactive programming library
- **Angular Router** - Client-side routing
- **Angular Forms** - Form handling and validation
- **Angular HttpClient** - HTTP requests to backend

---

### 2.2 Frontend-Backend Communication Architecture

The application uses a **REST API** architecture with HTTP for communication:

### 3. 🚀 Quick Start Guide

#### Backend Setup (FastAPI Web Server)

**Prerequisites:**
- Python 3.8+
- pip

**Installation & Running:**

```bash
cd backend

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # Update with your API keys (OpenRouter, etc.)

# Start the FastAPI web server
python -m uvicorn start_app:app --reload
```

The web server will run on `http://localhost:8000` by default.

#### Backend CLI & Debug Mode

You can also use the terminal CLI interface with optional debug logging:

```bash
# Run interactive CLI in terminal
python main.py

# Run CLI with debug mode enabled (shows source logs from agent flow)
python main.py --debug
```

**Debug Mode Output:**
- Shows LangChain agent decision steps
- Displays tool selection logic
- Prints source data used for responses
- Helpful for troubleshooting agent behavior

**CLI Usage:**
- Type your question and press Enter
- Type `exit` or `quit` to stop

Example:
```
LeafAI terminal chat
Type 'exit' or 'quit' to stop.

You: What are the Swiss public holidays?
LeafAI: [Response from agent]

You: exit
See you later!
```

#### Frontend Setup (Angular)

**Prerequisites:**
- Node.js 18+ & npm

**Installation & Running:**

```bash
cd frontend/ui

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will run on `http://localhost:4200` by default.

---

### 4. How to Navigate

-   **`/backend`**: FastAPI application with AI agent orchestration
    - `start_app.py` - FastAPI web server entry point
    - `main.py` - CLI interface with debug mode support
    - `agent.py` - LangChain agent with tools
    - `holiday_api.py` - Swiss holidays integration
    - `security/pii.py` - PII masking/unmasking utilities
    - `data/handbook.md` - GreenLeaf handbook for RAG
    - `prompts/system_prompt.md` - System prompt for LLM

-   **`/frontend/ui`**: Angular web interface
    - `src/app/services/assistant.service.ts` - Backend communication
    - `src/app/pages/assistant/` - Main chat interface components

-   **`/data`**: Contains the cleaned, non-PII (Personally Identifiable Information) version of the GreenLeaf Handbook.
    
-   **`Wiki`**: Detailed technical documentation, API specifications, and Swiss FADP (nDSG) compliance notes.
    
-   **`Projects`**: Our Agile Kanban board used for tracking Sprint progress and User Stories.
    

### 5. Frontend-Backend Communication Architecture

The application uses a **REST API** architecture with HTTP for communication:

**Architecture Diagram:**
```
Angular Frontend                FastAPI Backend
    (port 4200)                  (port 8000)
         │                             │
    User Input                         │
         │                             │
      CLI Tool                    Agent Processing
    (Optional)                    - Tool Selection
    ┌──────────────────────────────────┐
    │ HTTP POST /ask                   │
    │ { "question": "..." }            │
    │──────────────────────────────────→
         │                             │
         │                      - LangChain Orchestration
         │                      - Holiday API Calls
         │                      - PII Masking
         │                             │
    ┌──────────────────────────────────┐
    │ HTTP Response (200)              │
    │ { "answer": "..." }              │
    │←──────────────────────────────────
     │                                  │
  Display                          Return Result
  Result                                │
```

**Communication Flow:**

1. **Frontend Request**: 
   - User enters a question in the Angular UI
   - `AssistantService` sends HTTP POST request to `/ask` endpoint
   - Request payload: `{ "question": "user input" }`

2. **Backend Processing**:
   - FastAPI receives request at `/ask` endpoint in `start_app.py`
   - `run_main_flow()` agent is executed with the question
   - Agent determines if we need to use the tool:
     - **Holiday Tool** - Fetches Swiss holidays via OpenHolidays API
   - Response is generated and PII is masked before returning

3. **Frontend Response**:
   - Response received as `{ "answer": "response text" }`
   - Angular displays the answer to the user
   - RxJS Observable pattern handles async operations

**CLI Interface:**
- Direct Python interface for testing without web server
- Useful for debugging agent logic
- Built-in debug mode for detailed logging

---

### 6. Project Objectives
1. **Architectual Decisions** Each architectural decision must be backed by rational arguments that you must be able to explain.

2. **Backend Processing**:
   - FastAPI receives requests at `/ask` endpoint in `main.py`
   - `run_main_flow()` agent is executed with the question
   - Agent determines which tools to use:
     - **Holiday Tool** - Fetches Swiss holidays via OpenHolidays API
     - **Handbook Tool** - Custom Python logic
   - Response is generated, and PII is masked before returning

3. **Frontend Response**:
   - Response received as `{ "answer": "response text" }`
   - Angular displays the answer to the user
   - RxJS Observable pattern handles async operations

**CORS Configuration**: Backend allows requests from any origin (`allow_origins=["*"]`) to support development and production deployments.

### 3. Quick Start Guide

#### Backend Setup (FastAPI + Python)

**Prerequisites:**
- Python 3.8+
- pip

**Installation & Running:**

```bash
cd backend

# Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env  # Update with your API keys (OpenRouter, etc.)

# Start the FastAPI server
uvicorn main:app --reload
```

The backend will run on `http://localhost:8000` by default.

#### Frontend Setup (Angular)

**Prerequisites:**
- Node.js 18+ & npm

**Installation & Running:**

```bash
cd frontend/ui

# Install dependencies
npm install

# Start the development server
npm start
```

The frontend will run on `http://localhost:4200` by default.

---

### 4. How to Navigate

-   **`/backend`**: FastAPI application with AI agent orchestration
    - `main.py` - FastAPI server entry point
    - `agent.py` - LangChain agent with tools
    - `holiday_api.py` - Swiss holidays integration
    - `security/pii.py` - PII masking/unmasking utilities
    - `data/handbook.md` - Contains the cleaned, non-PII (Personally Identifiable Information) version of the GreenLeaf Handbook.
    - `prompts/system_prompt.md` - System prompt for LLM
      
-   **`/frontend/ui`**: Angular web interface
    - `src/app/services/assistant.service.ts` - Backend communication
    - `src/app/pages/assistant/` - Main chat interface components
        
-   **`Wiki`**: Detailed technical documentation, API specifications, and Swiss FADP (nDSG) compliance notes.
    
-   **`Projects`**: Our Agile Kanban board is used for tracking Sprint progress and User Stories.

---

## Backend Components

### Web Server (`start_app.py`)

FastAPI application that provides REST API endpoints for the frontend.

- Endpoint: `POST /ask` - Accepts questions and returns AI agent responses
- CORS enabled for frontend communication
- Request: `{ "question": string }`
- Response: `{ "answer": string }`

### CLI Interface (`main.py`)

Terminal-based interface for testing and debugging the agent directly.

**Features:**
- Interactive conversation loop
- Debug mode with `--debug` flag
- Shows agent reasoning and tool selection
- Useful for development and troubleshooting

**Example:**
```bash
python main.py --debug
```

Output shows:
- Which tools are being selected
- How the agent is reasoning
- Data used from RAG/APIs
- PII masking verification

---

## Holiday API Implementation (`holiday_api.py`)

### What it does

Fetches Swiss public holidays from the [OpenHolidays API](https://www.openholidaysapi.org) and cleans the raw JSON response into simple, flat records.

- Retrieves national holidays for Switzerland (or any supported country)
- Supports canton-level filtering — e.g. `CH-ZH` for Zurich, `CH-BE` for Bern
- Normalises nested API fields (name lists, subdivision objects) into plain strings
- Prints results in a readable table format

### Requirements

Install the dependency:

```bash
pip install requests
```

### Usage

Run the script directly:

```bash
python holiday_api.py
```

This will print:
1. All Swiss national holidays for the current year
2. Holidays specific to the Zurich canton (`CH-ZH`)

To use it in your own code:

```python
from holiday_api import fetch_holidays

# National holidays
holidays = fetch_holidays(country_iso="CH", language_iso="EN")

# Canton-specific holidays
zh_holidays = fetch_holidays(country_iso="CH", subdivision_code="CH-ZH")

# Custom date range
holidays = fetch_holidays(valid_from="2026-01-01", valid_to="2026-06-30")
```

Each returned record contains:

| Field | Description |
|---|---|
| `id` | Unique holiday ID |
| `name` | Holiday name |
| `start_date` | Start date (YYYY-MM-DD) |
| `end_date` | End date (YYYY-MM-DD) |
| `type` | `Public` or `Optional` |
| `nationwide` | `True` if it applies to all cantons |
| `subdivisions` | List of canton codes (e.g. `["CH-ZH"]`) |
