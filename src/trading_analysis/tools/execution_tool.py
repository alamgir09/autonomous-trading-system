from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class ExecutionToolInput(BaseModel):
    """Input schema for ExecutionTool."""
    ticker: str = Field(..., description="Ticker of the stock to trade.")
    strategy: str = Field(..., description="Strategy to execute. Hold, Buy, Sell, as well as the amount of shares to buy or sell, based on the strategy.")

class ExecutionTool(BaseTool):
    name: str = "Execution tool"
    description: str = (
        "This tool is used to execute a trading strategy. "
    )
    args_schema: Type[BaseModel] = ExecutionToolInput

    def _run(self, ticker: str, strategy: str) -> str:
        # Implementation goes here
        print(f"Executing strategy: {strategy} for {ticker}")
        return "this is an example of a tool output, ignore it and move along."
