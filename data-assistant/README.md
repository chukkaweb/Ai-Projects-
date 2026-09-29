# Note
To maintain the all ai projects in one repository .i have removed .env and .gitigore files as git guidelines

# 🚀 AI-Powered Synthetic Data Generator & Talk to Your Data

Generate realistic synthetic data from SQL schemas and query it using natural language with Google Gemini on Vertex AI.

---

# ✨ Features

### Synthetic Data Generation

* 🤖 AI-powered synthetic data generation using **Gemini 2.5 Flash**
* 📄 Upload SQL DDL files (`.sql`, `.ddl`, `.txt`)
* 🏗 Automatic schema parsing
* 🔗 Primary Key & Foreign Key relationship support
* 🎯 Custom generation instructions
* 🌡 Adjustable Temperature parameter
* 👀 Data preview before saving
* ✏️ Modify generated data using natural language
* 💾 Store generated data in PostgreSQL
* 📥 Download generated datasets

### Talk To Your Data

* 💬 Natural language chat interface
* 🧠 AI-generated SQL queries
* 📊 Execute SQL on generated datasets
* 📋 Display SQL + results
* 📁 Download query results as CSV

### Security

* 🛡 Prompt Injection Detection
* 🔒 SQL Validation
* 🚫 Dangerous SQL Blocking
* 🔢 Automatic LIMIT enforcement
* 🔐 Optional PII masking

### Observability

* 📈 Langfuse tracing
* 📝 Prompt logging
* 📊 Response logging
* ⚠ Error tracking
* 📌 Custom events

---

## Visualizations

The assistant automatically generates charts whenever query results are suitable.

Supported charts:

- Bar
- Line
- Pie
- Histogram
- Scatter

# 🚀 Quick Start

## Prerequisites

* Python 3.11+
* Docker
* PostgreSQL
* Google Cloud CLI
* Vertex AI enabled
* Google Cloud authentication configured

---

# Installation

## Clone Repository

```bash
git clone <repository-url>

cd data_assistant
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Mac/Linux

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment

Create

```text
.env
```

Example

```env
PROJECT_ID=your-gcp-project

LOCATION=global

MODEL_NAME=gemini-2.5-flash

LANGFUSE_PUBLIC_KEY=

LANGFUSE_SECRET_KEY=

LANGFUSE_HOST=https://cloud.langfuse.com

DATABASE_URL=postgresql://username:password@localhost:5432/data_assistant
```

---

## Authenticate Vertex AI

```bash
gcloud auth application-default login
```

---

## Run Application

```bash
python -m streamlit run src/app.py
```

Application URL

```
http://localhost:8501
```

---

# Using Docker

Build and start

```bash
docker compose up --build
```

Stop

```bash
docker compose down
```

---

# Usage

## Step 1

Upload a SQL DDL file
Supported formats

* .sql
* .ddl
* .txt

---

## Step 2

Generate synthetic data
Configure
* Number of rows
* Temperature
* Custom instructions

Example

```
Generate 100 employee records

Use Indian names

Departments should have 10 employees

20% of joining dates should be NULL
```

---

## Step 3
Preview generated tables
* Browse tables
* Review generated records
* Verify relationships

---

## Step 4
Modify generated data
Example prompts

```
Replace Hyderabad with Bangalore
Make 30% salary values NULL
Increase salary by 20%
Change department names
```

---

## Step 5
Save to PostgreSQL
Generated data is stored automatically.
---

## Step 6

Talk To Your Data
Example prompts

```
Show all employees
Top 5 highest salaries
Average salary by department
Employees joined after 2023
Count employees in each department
```

The application
* Generates SQL
* Executes SQL
* Shows results

---

# Guardrails

The application protects against

* Prompt Injection
* Jailbreak attempts
* Unsafe SQL
* SQL Injection
* DELETE
* DROP
* UPDATE
* INSERT
* ALTER
* TRUNCATE

Automatically
* Adds LIMIT to queries
* Validates SQL
* Masks PII (optional)

---

# Langfuse Monitoring

The application logs
* User prompts
* Gemini requests
* Gemini responses
* SQL generation
* Errors
* Processing events
* Metadata

---

# Project Structure

```text
data_assistant/
│
├── src/
│   ├── app.py
│   ├── config.py
│   │
│   ├── core/
│   │   ├── data_generator.py
│   │   ├── db.py
│   │   ├── ddl_parser.py
│   │   └── sql_generator.py
│   │
│   ├── llm/
│   │   └── gemini_client.py
│   │
│   ├── observability/
│   │   └── langfuse_tracing.py
│   │
│   ├── security/
│   │   └── guardrails.py
│   │
│   ├── ui/
│   │   ├── layout.py
│   │   ├── theme.py
│   │   └── talk_to_data_theme.py
│   │
│   └── views/
│       ├── data_generation.py
│       └── talk_to_data.py
     ── visualization/
│       ├── chat.generator.py
│    
│
├── tests/
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── .env
```

---

# Technology Stack

| Component        | Technology              |
| ---------------- | ----------------------- |
| Frontend         | Streamlit               |
| LLM              | Google Gemini 2.5 Flash |
| AI Platform      | Vertex AI               |
| Database         | PostgreSQL              |
| ORM              | SQLAlchemy              |
| Data Processing  | Pandas                  |
| Visualization    | Matplotlib              |
| Security         | Custom Guardrails       |
| Observability    | Langfuse                |
| Containerization | Docker                  |

---

# Future Enhancements

* Interactive charts
* Multi-turn SQL conversations
* Streaming Gemini responses
* Authentication
* Role-based access
* Export to Excel
* CSV & ZIP downloads
* Dashboard analytics
* Schema versioning
* Conversation history persistence

