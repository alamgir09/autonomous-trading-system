from crewai.tools import BaseTool
from typing import Type, Literal
from pydantic import BaseModel, Field, field_validator
import json
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
import os
from alpaca.common.exceptions import APIError


class ExecutionToolInput(BaseModel):
    """Input schema for ExecutionTool."""
    ticker: str = Field(..., description="Ticker symbol of the stock to trade (e.g. 'AAPL').")
    position: str = Field(..., description="Position to take. Must be one of: 'Buy', 'Sell', or 'Hold'.")
    amount: float = Field(..., description="Amount of shares to buy or sell. Must be a positive number.")
    
    @field_validator('position')
    def validate_position(cls, v):
        if v.lower() not in ['buy', 'sell', 'hold']:
            raise ValueError("Position must be one of: 'Buy', 'Sell', or 'Hold'")
        return v.capitalize()
    
    @field_validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError("Amount must be positive")
        return v

class ExecutionTool(BaseTool):
    name: str = "TradeExecution"
    description: str = (
        "Executes trades on Alpaca. Use this tool to buy, sell, or hold positions. "
        "Provide the ticker symbol, position action (Buy, Sell, Hold), and the amount of shares. "
        "Returns confirmation with order details or error message."
    )
    args_schema: Type[BaseModel] = ExecutionToolInput

    def _run(self, ticker: str, position: str, amount: float) -> str:
        try:
            print(f"Executing {position} order for {amount} shares of {ticker}")

            if position == 'Hold':
                return json.dumps({
                    "status": "success",
                    "message": f"Hold position maintained for {ticker}"
                })

            # Create a client instance
            client = TradingClient(
                os.getenv("APCA_API_KEY_ID"), 
                os.getenv("APCA_API_SECRET_KEY")
            )

            # If selling, check if we have the position
            if position == 'Sell':
                try:
                    # Try to get the specific position directly
                    try:
                        # Use get_position for the specific ticker
                        owned_position = client.get_position(ticker)
                        
                        # Check if we have enough shares
                        owned_qty = float(owned_position.qty)
                        if owned_qty < amount:
                            return json.dumps({
                                "status": "error",
                                "message": f"Cannot sell {amount} shares of {ticker} - only own {owned_qty} shares"
                            })
                            
                        print(f"Position check passed: Own {owned_qty} shares of {ticker}, selling {amount}")
                        
                    except APIError as e:
                        # Position not found - handle gracefully
                        if "position does not exist" in str(e).lower() or "not found" in str(e).lower():
                            return json.dumps({
                                "status": "error",
                                "message": f"Cannot sell {ticker} - position not found in portfolio"
                            })
                        else:
                            # Re-raise if it's a different API error
                            raise
                        
                except Exception as e:
                    print(f"Error checking position: {e}")
                    return json.dumps({
                        "status": "error",
                        "message": f"Failed to verify position before selling: {str(e)}"
                    })

            # Create order side
            order_side = OrderSide.BUY if position == 'Buy' else OrderSide.SELL

            # Create a market order request
            market_order_data = MarketOrderRequest(
                symbol=ticker,
                qty=amount,
                side=order_side,
                time_in_force=TimeInForce.DAY
            )

            # Submit the order
            result = client.submit_order(market_order_data)
            
            # Serialize the result
            result_dict = result.to_dict()

            # Add summary for better readability
            summary = {
                "status": "success",
                "action": position,
                "ticker": ticker,
                "shares": amount,
                "order_id": result_dict.get("id"),
                "order_status": result_dict.get("status"),
                "filled_price": result_dict.get("filled_avg_price"),
            }

            # Save to file for debugging
            try:
                os.makedirs('data', exist_ok=True)
                with open(f'data/{ticker}_execution_result.json', 'w') as f:
                    json.dump(result_dict, f, indent=2)
            except Exception as e:
                print(f"Warning: Could not save execution result to file: {str(e)}")

            # Return summary with full result
            return json.dumps({
                "summary": summary,
                "details": result_dict
            })
        
        except APIError as e:
            error_msg = str(e)
            print(f"Alpaca API error: {error_msg}")
            
            # Try to provide more helpful error messages for common issues
            if "insufficient buying power" in error_msg.lower():
                return json.dumps({
                    "status": "error",
                    "message": f"Cannot execute {position} order for {ticker}: Insufficient funds in account"
                })
            elif "position sell quantity exceeds current position size" in error_msg.lower():
                return json.dumps({
                    "status": "error",
                    "message": f"Cannot sell {amount} shares of {ticker}: Not enough shares owned"
                })
            else:
                return json.dumps({
                    "status": "error",
                    "message": f"Alpaca API error: {error_msg}"
                })
                
        except Exception as e:
            print(f"Unexpected error: {e}")
            return json.dumps({
                "status": "error",
                "message": f"Unexpected error: {str(e)}"
            })
