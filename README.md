# Autonomous Trading Analysis System

A multi-agent trading platform leveraging LLMs and real-time market data to autonomously perform financial research, portfolio analysis, and strategy validation.

## Overview

This research project uses CrewAI to orchestrate multiple AI agents that work together to:
- Process real-time market data from Alpaca Markets
- Perform autonomous financial research and analysis
- Generate trading strategies and validate them
- Provide portfolio analysis and recommendations

## Tech Stack

- **Core**: Python, CrewAI
- **AI/ML**: OpenAI, LangChain
- **Market Data**: Alpaca API
- **Configuration**: YAML

## Setup

1. Clone the repository

2. Install uv (if not already installed):
```bash
pip install uv
```

3. Create virtual environment and install dependencies:
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip sync
```

4. Set up environment variables in `.env`:
```bash
OPENAI_API_KEY=your_openai_key
APCA_API_KEY_ID=your_alpaca_key
APCA_API_SECRET_KEY=your_alpaca_secret
```

## Project Structure

```
trading_analysis/
├── src/
│   └── trading_analysis/
│       ├── config/
│       │   ├── agents.yaml    # Agent configurations
│       │   └── tasks.yaml     # Task definitions
│       ├── tools/             # Custom agent tools
│       ├── crew.py           # CrewAI implementation
│       ├── main.py           # Entry point
│       └── network.py        # Market data connection
├── .env                      # Environment variables
├── uv.lock                  # Dependency lock file
└── pyproject.toml          # Project configuration
```

## Usage

Run the system:
```bash
python -m trading_analysis.main
```

## Features

- Multi-agent system for autonomous financial analysis
- Real-time market news monitoring and processing
- LLM-powered research and strategy validation
- Configurable agent and task behaviors via YAML
