from crewai.tools import BaseTool
from typing import Type, Optional
from pydantic import BaseModel, Field
import json
from alpaca.trading.client import TradingClient
import os
from alpaca.common.exceptions import APIError

try:
    # Create a new client instance for each call
    client = TradingClient(
        os.getenv("APCA_API_KEY_ID"), 
        os.getenv("APCA_API_SECRET_KEY")
    )

    ticker = None

    if ticker:
        portfolio = client.get_position(ticker)
    else:
        portfolio = client.get_all_positions()
    
    # Convert portfolio to a serializable format
    if isinstance(portfolio, list):
        portfolio_data = [{
            'symbol': pos.symbol,
            'qty': str(pos.qty),
            'market_value': str(pos.market_value),
            'avg_entry_price': str(pos.avg_entry_price),
            'current_price': str(pos.current_price),
            'unrealized_pl': str(pos.unrealized_pl),
            'unrealized_plpc': str(pos.unrealized_plpc),
            'asset_id': str(pos.asset_id),
            'change_today': str(pos.change_today)
        } for pos in portfolio]
    else:
        portfolio_data = {
            'symbol': portfolio.symbol,
            'qty': str(portfolio.qty),
            'market_value': str(portfolio.market_value),
            'avg_entry_price': str(portfolio.avg_entry_price),
            'current_price': str(portfolio.current_price),
            'unrealized_pl': str(portfolio.unrealized_pl),
            'unrealized_plpc': str(portfolio.unrealized_plpc),
            'asset_id': str(portfolio.asset_id),
            'change_today': str(portfolio.change_today)
        }

    # Save to file for debugging
    try:
        os.makedirs('data', exist_ok=True)
        with open('data/portfolio.json', 'w') as f:
            json.dump(portfolio_data, f, indent=2)
    except Exception as e:
        print(f"Warning: Could not save portfolio data to file: {str(e)}")
    
except APIError as e:
    print(f"Failed to fetch portfolio data: {str(e)}")
except Exception as e:
    print(f"Unexpected error: {str(e)}")