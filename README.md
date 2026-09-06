# Nexus AI

**Version 16.0 FINAL — Production Portfolio Build**

Nexus AI is a local-first AI agent platform built with Python, Streamlit, Ollama and SQLite. It combines conversational AI, research, document intelligence, cybersecurity assistance, memory, autonomous planning, multi-agent orchestration, plugins, evaluation, observability and production security in one application.

## Core Features

- AI Chat with streaming responses and browser speech
- Web research and utility tools
- Document intelligence and RAG
- Cybersecurity analysis
- Persistent mission memory with SQLite
- Goal-based autonomous planning
- Adaptive memory and contextual recall
- Self-healing agent recovery
- Parallel and dependency-aware tool execution
- Multi-agent orchestration
- Read-only plugin architecture
- Prompt-injection and destructive-action protection
- Role-based production permissions
- Human approval gates for sensitive operations
- Local security audit logging
- Agent benchmarking and deterministic evaluation
- Workflow automation
- Agent observability and telemetry
- Production portfolio dashboard

## Architecture

```text
User
  ↓
Streamlit UI
  ↓
Production Security / Permission Layer
  ↓
Goal Planner / Workflow / Mission Router
  ↓
Agent Runtime
  ├── Core Tools
  ├── Plugins
  ├── RAG / Memory
  ├── Web / Utility Tools
  └── Cybersecurity Tools
  ↓
Verification + Evaluation
  ↓
SQLite Mission Memory + Security Audit + Telemetry
  ↓
Final Response / Report
```

## Technology Stack

- Python
- Streamlit
- Ollama
- SQLite
- Requests
- Local-first architecture

## Security

Nexus AI uses a read-only-by-default tool model. Sensitive operations are policy-controlled, destructive actions are blocked, prompt-injection patterns are detected, and production-sensitive operations can require explicit human approval. Security decisions are recorded locally.

## Benchmark

The final benchmark suite achieved **5/5 tests and 100/100** after deterministic benchmark isolation and performance optimization.

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Make sure Ollama is installed and the configured local model is available.

## Portfolio Description

**Nexus AI — Local-First Autonomous AI Agent Platform**

Developed a production-oriented AI agent platform integrating RAG, persistent memory, autonomous goal planning, multi-agent orchestration, parallel tool execution, plugin architecture, self-healing recovery, benchmarking, observability, and role-based security with human approval controls.

## Resume Bullets

- Built a local-first AI agent platform using Python, Streamlit, Ollama and SQLite with RAG, persistent memory, web research and cybersecurity capabilities.
- Implemented autonomous goal planning, dependency-aware parallel tool execution, multi-agent orchestration, plugins, self-healing recovery and workflow automation.
- Designed security controls including prompt-injection detection, read-only tool policies, role-based permissions, human approval gates and local audit logging.
- Developed deterministic agent benchmarking and observability dashboards, achieving **100/100** on the final benchmark suite.

## Project Status

**Production Portfolio Build — Nexus AI 16.0 FINAL**
