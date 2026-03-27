#!/usr/bin/env python3
"""
MCP Stock Server Example
A Model Context Protocol server that provides stock market data tools
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional
import random

# Simulated stock data (in production, use real API like yfinance, Alpha Vantage, etc.)
STOCK_DATABASE = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "price": 178.50},
    "GOOGL": {"name": "Alphabet Inc.", "sector": "Technology", "price": 142.30},
    "MSFT": {"name": "Microsoft Corporation", "sector": "Technology", "price": 378.90},
    "AMZN": {"name": "Amazon.com Inc.", "sector": "Consumer Cyclical", "price": 178.25},
    "TSLA": {"name": "Tesla Inc.", "sector": "Automotive", "price": 242.80},
    "META": {"name": "Meta Platforms Inc.", "sector": "Technology", "price": 484.50},
    "NVDA": {"name": "NVIDIA Corporation", "sector": "Technology", "price": 875.30},
}


class MCPStockServer:
    """MCP Server for stock market data"""
    
    def __init__(self):
        self.name = "stock-data-server"
        self.version = "1.0.0"
        self.tools = self._register_tools()
    
    def _register_tools(self) -> List[Dict[str, Any]]:
        """Register available tools"""
        return [
            {
                "name": "get_stock_price",
                "description": "Get current stock price for a given ticker symbol",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock ticker symbol (e.g., AAPL, GOOGL)"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "get_stock_info",
                "description": "Get detailed information about a stock",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock ticker symbol"
                        }
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "get_historical_prices",
                "description": "Get historical stock prices for a date range",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbol": {
                            "type": "string",
                            "description": "Stock ticker symbol"
                        },
                        "days": {
                            "type": "integer",
                            "description": "Number of days of historical data",
                            "default": 7
                        }
                    },
                    "required": ["symbol"]
                }
            },
            {
                "name": "compare_stocks",
                "description": "Compare multiple stocks side by side",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "symbols": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of stock ticker symbols to compare"
                        }
                    },
                    "required": ["symbols"]
                }
            },
            {
                "name": "search_stocks",
                "description": "Search for stocks by sector or name",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "Search query (sector name or company name)"
                        }
                    },
                    "required": ["query"]
                }
            }
        ]
    
    async def get_stock_price(self, symbol: str) -> Dict[str, Any]:
        """Get current stock price"""
        symbol = symbol.upper()
        
        if symbol not in STOCK_DATABASE:
            return {
                "error": f"Stock symbol '{symbol}' not found",
                "available_symbols": list(STOCK_DATABASE.keys())
            }
        
        stock = STOCK_DATABASE[symbol]
        # Simulate price fluctuation
        current_price = stock["price"] * (1 + random.uniform(-0.02, 0.02))
        
        return {
            "symbol": symbol,
            "price": round(current_price, 2),
            "currency": "USD",
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_stock_info(self, symbol: str) -> Dict[str, Any]:
        """Get detailed stock information"""
        symbol = symbol.upper()
        
        if symbol not in STOCK_DATABASE:
            return {"error": f"Stock symbol '{symbol}' not found"}
        
        stock = STOCK_DATABASE[symbol]
        current_price = stock["price"] * (1 + random.uniform(-0.02, 0.02))
        
        return {
            "symbol": symbol,
            "name": stock["name"],
            "sector": stock["sector"],
            "current_price": round(current_price, 2),
            "day_high": round(current_price * 1.03, 2),
            "day_low": round(current_price * 0.97, 2),
            "volume": random.randint(10000000, 100000000),
            "market_cap": f"${random.randint(500, 3000)}B",
            "pe_ratio": round(random.uniform(15, 35), 2),
            "timestamp": datetime.now().isoformat()
        }
    
    async def get_historical_prices(self, symbol: str, days: int = 7) -> Dict[str, Any]:
        """Get historical stock prices"""
        symbol = symbol.upper()
        
        if symbol not in STOCK_DATABASE:
            return {"error": f"Stock symbol '{symbol}' not found"}
        
        base_price = STOCK_DATABASE[symbol]["price"]
        historical_data = []
        
        for i in range(days, 0, -1):
            date = datetime.now() - timedelta(days=i)
            price = base_price * (1 + random.uniform(-0.05, 0.05))
            historical_data.append({
                "date": date.strftime("%Y-%m-%d"),
                "open": round(price * 0.99, 2),
                "high": round(price * 1.02, 2),
                "low": round(price * 0.98, 2),
                "close": round(price, 2),
                "volume": random.randint(50000000, 150000000)
            })
        
        return {
            "symbol": symbol,
            "period": f"{days} days",
            "data": historical_data
        }
    
    async def compare_stocks(self, symbols: List[str]) -> Dict[str, Any]:
        """Compare multiple stocks"""
        comparison = []
        
        for symbol in symbols:
            symbol = symbol.upper()
            if symbol in STOCK_DATABASE:
                stock = STOCK_DATABASE[symbol]
                current_price = stock["price"] * (1 + random.uniform(-0.02, 0.02))
                comparison.append({
                    "symbol": symbol,
                    "name": stock["name"],
                    "price": round(current_price, 2),
                    "sector": stock["sector"]
                })
            else:
                comparison.append({
                    "symbol": symbol,
                    "error": "Not found"
                })
        
        return {
            "comparison": comparison,
            "timestamp": datetime.now().isoformat()
        }
    
    async def search_stocks(self, query: str) -> Dict[str, Any]:
        """Search stocks by sector or name"""
        query = query.lower()
        results = []
        
        for symbol, data in STOCK_DATABASE.items():
            if (query in data["name"].lower() or 
                query in data["sector"].lower() or 
                query in symbol.lower()):
                results.append({
                    "symbol": symbol,
                    "name": data["name"],
                    "sector": data["sector"],
                    "price": data["price"]
                })
        
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a tool call"""
        try:
            if tool_name == "get_stock_price":
                return await self.get_stock_price(arguments["symbol"])
            elif tool_name == "get_stock_info":
                return await self.get_stock_info(arguments["symbol"])
            elif tool_name == "get_historical_prices":
                days = arguments.get("days", 7)
                return await self.get_historical_prices(arguments["symbol"], days)
            elif tool_name == "compare_stocks":
                return await self.compare_stocks(arguments["symbols"])
            elif tool_name == "search_stocks":
                return await self.search_stocks(arguments["query"])
            else:
                return {"error": f"Unknown tool: {tool_name}"}
        except Exception as e:
            return {"error": f"Tool execution failed: {str(e)}"}
    
    def list_tools(self) -> List[Dict[str, Any]]:
        """List all available tools"""
        return self.tools
    
    def get_server_info(self) -> Dict[str, Any]:
        """Get server information"""
        return {
            "name": self.name,
            "version": self.version,
            "protocol_version": "2024-11-05",
            "capabilities": {
                "tools": True,
                "resources": False,
                "prompts": False
            }
        }


async def main():
    """Demo the MCP Stock Server"""
    print("=" * 70)
    print("MCP Stock Server Example")
    print("=" * 70)
    print()
    
    server = MCPStockServer()
    
    # Display server info
    print("Server Info:")
    print(json.dumps(server.get_server_info(), indent=2))
    print()
    
    # List available tools
    print("Available Tools:")
    for tool in server.list_tools():
        print(f"  - {tool['name']}: {tool['description']}")
    print()
    
    # Demo tool calls
    print("=" * 70)
    print("Demo Tool Calls")
    print("=" * 70)
    print()
    
    # 1. Get stock price
    print("1. Get Stock Price (AAPL):")
    result = await server.call_tool("get_stock_price", {"symbol": "AAPL"})
    print(json.dumps(result, indent=2))
    print()
    
    # 2. Get stock info
    print("2. Get Stock Info (TSLA):")
    result = await server.call_tool("get_stock_info", {"symbol": "TSLA"})
    print(json.dumps(result, indent=2))
    print()
    
    # 3. Get historical prices
    print("3. Get Historical Prices (GOOGL, 5 days):")
    result = await server.call_tool("get_historical_prices", 
                                    {"symbol": "GOOGL", "days": 5})
    print(json.dumps(result, indent=2))
    print()
    
    # 4. Compare stocks
    print("4. Compare Stocks (AAPL, MSFT, GOOGL):")
    result = await server.call_tool("compare_stocks", 
                                    {"symbols": ["AAPL", "MSFT", "GOOGL"]})
    print(json.dumps(result, indent=2))
    print()
    
    # 5. Search stocks
    print("5. Search Stocks (Technology):")
    result = await server.call_tool("search_stocks", {"query": "Technology"})
    print(json.dumps(result, indent=2))
    print()
    
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
