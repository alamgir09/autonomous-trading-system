from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field
import json

class PortfolioToolInput(BaseModel):
    """Input schema for MyCustomTool."""
    ticker: str = Field(..., description="Return the portfolio holdings for the given ticker")


class PortfolioTool(BaseTool):
    name: str= "PortfolioAnalyzer"
    description: str = (
        "Retrieves current portfolio holdings and position details for a given ticker"
    )
    args_schema: Type[BaseModel] = PortfolioToolInput

    def _run(self, ticker: str) -> str:
        # You could fetch this from your database or trading platform
        holdings = {
            "AAPL": {
                "shares": 100,
                "average_cost": 140.50,
                "current_value": 15000.00,
                "position_opened": "2024-01-15"
            }
        }
        return json.dumps(holdings.get(ticker, "No position found"))