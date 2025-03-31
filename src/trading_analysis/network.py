import asyncio
import os
import json
from websockets import connect
from trading_analysis.main import run
from alpaca.trading.client import TradingClient
# from alpaca.trading.client import TradingClient

class NewsMonitorService:
    def __init__(self):
        self.ws_url = "wss://stream.data.alpaca.markets/v1beta1/news"
        self.api_key = os.getenv("APCA_API_KEY_ID")
        self.secret_key = os.getenv("APCA_API_SECRET_KEY")
        self.base_url = os.getenv("APCA_API_BASE_URL")
        self.client = TradingClient(self.api_key, self.secret_key)

    async def connect(self):
        async with connect(self.ws_url) as websocket:
            # Authenticate
            auth_message = json.dumps({
                "action": "auth",
                "key": self.api_key,
                "secret": self.secret_key,
                "domain": self.base_url
            })
            await websocket.send(auth_message)

            # Subscribe to news
            subscribe_message = json.dumps({
                "action": "subscribe",
                "news": ["*"]
            })
            await websocket.send(subscribe_message)

            while True:
                try:
                    message = await websocket.recv()
                    news_data = json.loads(message)
                    news_data = news_data[0]
                    print(news_data)

                    if "headline" in news_data:
                        inputs = {
                            'ticker': news_data['symbols'],
                            'headline': news_data['headline'],
                            'content': news_data['content']
                        }
                        print("inputs", inputs)
                        run(inputs)
                        print("run complete")
                        break
                except Exception as e:
                    print(f"Error: {e}")
                    break
            

if __name__ == "__main__":
    service = NewsMonitorService()
    asyncio.run(service.connect())