from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json
from alpaca.trading.client import TradingClient
import os
from alpaca.common.exceptions import APIError

class PortfolioToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    ticker: str = Field(..., description="Return the portfolio holdings for the given ticker, or return all holdings if no ticker is provided")
    


class PortfolioTool(BaseTool):
    name: str= "PortfolioAnalyzer"
    description: str = (
        "Retrieves current portfolio holdings or position details for a given ticker, either by providing a ticker or not providing one"
    )
    args_schema: Type[BaseModel] = PortfolioToolInput

    def _run(self, ticker: str = None) -> str:
        try:
            # Create a new client instance for each call
            client = TradingClient(
                os.getenv("ALPACA_API_KEY"), 
                os.getenv("ALPACA_SECRET_KEY")
            )

            # if ticker:
            #     portfolio = client.get_position(ticker)
            # else:
            portfolio = client.get_all_positions()
            
            print("Portfolio:")
            print("type: ", type(portfolio))
            print(portfolio)

            result = json.dumps(portfolio)
            with open('portfolio.json', 'w') as f:
                f.write(result)

            return json.dumps(result)
            
        except APIError as e:
            return json.dumps({"error": f"Failed to fetch portfolio data: {str(e)}"})
        except Exception as e:
            return json.dumps({"error": f"Unexpected error: {str(e)}"})