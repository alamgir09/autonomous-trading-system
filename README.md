# Intelligent Trading Agents

A terminal-based, multi-agent AI system leveraging CrewAI to monitor financial news, analyze company data, and execute trades based on predefined criteria using the Alpaca Markets API.

## Project Overview

This project demonstrates the power of AI agent orchestration in financial markets by implementing a crew of specialized agents that work together to:

1. Monitor real-time news for specified stock tickers
2. Research company fundamentals and financial documents
3. Analyze market sentiment and conditions
4. Make trading decisions based on user-defined criteria
5. Execute trades via the Alpaca Markets API

## Key Features

- **CrewAI Orchestration**: Specialized agents working together in a coordinated workflow
- **Terminal-Based Interface**: Simple CLI for configuration and monitoring
- **YAML Configuration**: Define agent roles, goals, and trading criteria
- **Simulation Mode**: Test strategies with paper trading before deploying real capital
- **Performance Tracking**: Monitor and analyze trading performance via terminal output

## Technical Stack

- **Framework**: CrewAI for agent orchestration
- **Interface**: Rich and Typer for terminal UI
- **Storage**: SQLite for historical data
- **Agent Tools**: Custom AlpacaNewsTool, AlpacaTradingTool, SerperDevTool
- **APIs**: Alpaca Markets (trading & news WebSocket), OpenAI, SerperDev
- **Deployment**: Single Docker container

## Getting Started

### Prerequisites

- Python 3.9+
- Docker (optional)
- Alpaca Markets API account
- SerperDev API key (for web search capabilities)
- OpenAI API key (for sentiment analysis)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/intelligent-trading-agents.git
   cd intelligent-trading-agents
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

## Project Structure

```
intelligent-trading-agents/
├── src/
│   ├── intelligent_trading_agents/
│   │   ├── __init__.py
│   │   ├── crew.py                # CrewAI implementation
│   │   ├── main.py                # CLI entry point
│   │   ├── services/              # Core services
│   │   │   ├── __init__.py
│   │   │   └── news_monitor.py    # Alpaca WebSocket news service
│   │   ├── tools/                 # Custom tools
│   │   │   ├── __init__.py
│   │   │   ├── alpaca_news.py     # News processing tool
│   │   │   └── alpaca_trading.py  # Trading execution tool
│   │   └── utils/                 # Helper functions
│   │       ├── __init__.py
│   │       └── logging.py         # Logging configuration
├── config/
│   ├── agents.yaml                # Agent definitions
│   └── tasks.yaml                 # Task definitions
├── tests/                         # Test suite
├── .env.example                   # Environment variables template
├── Dockerfile                     # Docker configuration
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── PROJECT_REQUIREMENTS.md        # Detailed project requirements
└── SYSTEM_ARCHITECTURE.md         # System architecture documentation
```

## Usage

1. Configure your watchlist and trading parameters in `config/agents.yaml` and `config/tasks.yaml`

2. Start the news monitoring service:
   ```bash
   python -m intelligent_trading_agents monitor --tickers AAPL,MSFT,GOOGL
   ```
   This will connect to Alpaca's WebSocket API and listen for news events related to your tickers.

3. Run the trading system in simulation mode:
   ```bash
   python -m intelligent_trading_agents run --mode simulation --tickers AAPL,MSFT,GOOGL
   ```

4. Run in live trading mode (use with caution):
   ```bash
   python -m intelligent_trading_agents run --mode live --tickers AAPL,MSFT,GOOGL
   ```

5. View trading history and performance:
   ```bash
   python -m intelligent_trading_agents history
   ```

## News Monitoring Service

The system uses Alpaca's WebSocket API to monitor real-time news events. When a relevant news item is detected, it:

1. Performs initial sentiment analysis using OpenAI
2. Triggers the CrewAI workflow if the news is potentially significant
3. Logs the event for future reference

Example news monitoring code:

```python
class AlpacaNewsMonitor:
    def __init__(self, api_key, api_secret, tickers):
        self.api_key = api_key
        self.api_secret = api_secret
        self.tickers = tickers
        self.ws = None
        
    def start(self):
        """Start the WebSocket connection to Alpaca's news stream"""
        self.ws = websocket.WebSocketApp(
            "wss://stream.data.alpaca.markets/v1beta1/news",
            on_open=self._on_open,
            on_message=self._on_message,
            on_error=self._on_error,
            on_close=self._on_close
        )
        self.ws.run_forever()
        
    def _on_open(self, ws):
        """Authenticate and subscribe to news for specified tickers"""
        auth_msg = {
            'action': 'auth',
            'key': self.api_key,
            'secret': self.api_secret
        }
        ws.send(json.dumps(auth_msg))
        
        # Subscribe to news for specific tickers or all news
        subscribe_msg = {
            'action': 'subscribe',
            'news': self.tickers if self.tickers else ['*']
        }
        ws.send(json.dumps(subscribe_msg))
        
    def _on_message(self, ws, message):
        """Process incoming news messages"""
        data = json.loads(message)
        if isinstance(data, list) and len(data) > 0:
            event = data[0]
            if event.get('T') == 'n':  # News event
                self._process_news_event(event)
                
    def _process_news_event(self, event):
        """Process a news event and trigger the CrewAI workflow if significant"""
        headline = event.get('headline', '')
        symbols = event.get('symbols', [])
        
        # Perform initial sentiment analysis
        sentiment_score = self._analyze_sentiment(headline)
        
        # If sentiment is significant, trigger the CrewAI workflow
        if abs(sentiment_score - 50) > 20:  # More than 20 points from neutral
            self._trigger_crew_workflow(event, sentiment_score)
            
    def _analyze_sentiment(self, headline):
        """Analyze the sentiment of a headline using OpenAI"""
        # Implementation similar to your JavaScript example
        # Returns a score from 0-100
```

## Agent Configuration

Agents are defined in `config/agents.yaml` with their roles, goals, and backstories:

```yaml
news_monitor:
  role: "Financial News Analyst"
  goal: "Monitor real-time news for specified stock tickers and identify significant events"
  backstory: "You are an expert financial news analyst with years of experience identifying market-moving news..."

financial_analyst:
  role: "Financial Research Specialist"
  goal: "Analyze company fundamentals and provide investment recommendations"
  backstory: "You are a seasoned financial analyst with expertise in fundamental analysis..."
```

## Task Configuration

Tasks are defined in `config/tasks.yaml` with their descriptions, expected outputs, and assigned agents:

```yaml
monitor_news_task:
  description: "Monitor financial news for the specified tickers and identify significant events"
  expected_output: "A list of significant news events that could impact stock prices"
  agent: "news_monitor"

analyze_stocks_task:
  description: "Analyze the financial data and news events to make trading recommendations"
  expected_output: "Trading recommendations with rationale"
  agent: "financial_analyst"
```

## Development Roadmap

See [PROJECT_REQUIREMENTS.md](PROJECT_REQUIREMENTS.md) for the detailed development phases and roadmap.

## System Architecture

See [SYSTEM_ARCHITECTURE.md](SYSTEM_ARCHITECTURE.md) for the detailed system architecture and component interactions.

## License

MIT

## Acknowledgments

- Alpaca Markets for their trading API and news WebSocket
- CrewAI for the agent orchestration framework
- OpenAI for sentiment analysis capabilities
- SerperDev for web search capabilities
