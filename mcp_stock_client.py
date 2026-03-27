#!/usr/bin/env python3
"""
MCP Stock Client Example
Demonstrates how to interact with the MCP Stock Server
"""

import asyncio
import json
from typing import Dict, Any, List


class MCPStockClient:
    """Client for interacting with MCP Stock Server"""
    
    def __init__(self, server):
        """
        Initialize client with a server instance
        
        Args:
            server: MCPStockServer instance
        """
        self.server = server
        self.available_tools = {}
        self._load_tools()
    
    def _load_tools(self):
        """Load available tools from server"""
        tools = self.server.list_tools()
        for tool in tools:
            self.available_tools[tool["name"]] = tool
    
    def list_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return list(self.available_tools.keys())
    
    def get_tool_info(self, tool_name: str) -> Dict[str, Any]:
        """Get information about a specific tool"""
        return self.available_tools.get(tool_name, {"error": "Tool not found"})
    
    async def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool with given arguments
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool arguments
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.available_tools:
            return {"error": f"Tool '{tool_name}' not available"}
        
        return await self.server.call_tool(tool_name, kwargs)
    
    async def get_portfolio_summary(self, symbols: List[str]) -> Dict[str, Any]:
        """
        Get a comprehensive portfolio summary
        
        Args:
            symbols: List of stock symbols in portfolio
            
        Returns:
            Portfolio summary with total value and individual stocks
        """
        portfolio = []
        total_value = 0
        
        for symbol in symbols:
            info = await self.execute_tool("get_stock_info", symbol=symbol)
            if "error" not in info:
                portfolio.append(info)
                total_value += info["current_price"]
        
        return {
            "portfolio": portfolio,
            "total_stocks": len(portfolio),
            "total_value": round(total_value, 2),
            "average_price": round(total_value / len(portfolio), 2) if portfolio else 0
        }
    
    async def analyze_sector(self, sector: str) -> Dict[str, Any]:
        """
        Analyze all stocks in a given sector
        
        Args:
            sector: Sector name to analyze
            
        Returns:
            Sector analysis with statistics
        """
        search_result = await self.execute_tool("search_stocks", query=sector)
        
        if "error" in search_result or not search_result.get("results"):
            return {"error": f"No stocks found in sector: {sector}"}
        
        stocks = search_result["results"]
        prices = [stock["price"] for stock in stocks]
        
        return {
            "sector": sector,
            "stock_count": len(stocks),
            "stocks": stocks,
            "average_price": round(sum(prices) / len(prices), 2),
            "highest_price": max(prices),
            "lowest_price": min(prices),
            "price_range": round(max(prices) - min(prices), 2)
        }
    
    async def track_stock_performance(self, symbol: str, days: int = 7) -> Dict[str, Any]:
        """
        Track stock performance over time
        
        Args:
            symbol: Stock symbol to track
            days: Number of days to analyze
            
        Returns:
            Performance analysis
        """
        historical = await self.execute_tool("get_historical_prices", 
                                            symbol=symbol, days=days)
        
        if "error" in historical:
            return historical
        
        data = historical["data"]
        prices = [day["close"] for day in data]
        
        first_price = prices[0]
        last_price = prices[-1]
        change = last_price - first_price
        change_percent = (change / first_price) * 100
        
        return {
            "symbol": symbol,
            "period": f"{days} days",
            "start_price": first_price,
            "end_price": last_price,
            "change": round(change, 2),
            "change_percent": round(change_percent, 2),
            "highest": max(prices),
            "lowest": min(prices),
            "average": round(sum(prices) / len(prices), 2),
            "volatility": round(max(prices) - min(prices), 2),
            "trend": "up" if change > 0 else "down" if change < 0 else "flat"
        }


async def demo_basic_operations(client: MCPStockClient):
    """Demo basic stock operations"""
    print("=" * 70)
    print("BASIC OPERATIONS")
    print("=" * 70)
    print()
    
    # List available tools
    print("Available Tools:")
    for tool in client.list_available_tools():
        print(f"  - {tool}")
    print()
    
    # Get single stock price
    print("Get Stock Price (NVDA):")
    result = await client.execute_tool("get_stock_price", symbol="NVDA")
    print(json.dumps(result, indent=2))
    print()
    
    # Get detailed stock info
    print("Get Stock Info (META):")
    result = await client.execute_tool("get_stock_info", symbol="META")
    print(json.dumps(result, indent=2))
    print()


async def demo_advanced_operations(client: MCPStockClient):
    """Demo advanced stock operations"""
    print("=" * 70)
    print("ADVANCED OPERATIONS")
    print("=" * 70)
    print()
    
    # Portfolio summary
    print("Portfolio Summary (AAPL, GOOGL, MSFT):")
    portfolio = await client.get_portfolio_summary(["AAPL", "GOOGL", "MSFT"])
    print(json.dumps(portfolio, indent=2))
    print()
    
    # Sector analysis
    print("Sector Analysis (Technology):")
    sector_analysis = await client.analyze_sector("Technology")
    print(json.dumps(sector_analysis, indent=2))
    print()
    
    # Performance tracking
    print("Track Performance (TSLA, 7 days):")
    performance = await client.track_stock_performance("TSLA", days=7)
    print(json.dumps(performance, indent=2))
    print()


async def demo_comparison(client: MCPStockClient):
    """Demo stock comparison"""
    print("=" * 70)
    print("STOCK COMPARISON")
    print("=" * 70)
    print()
    
    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]
    print(f"Comparing: {', '.join(symbols)}")
    print()
    
    result = await client.execute_tool("compare_stocks", symbols=symbols)
    
    if "comparison" in result:
        print(f"{'Symbol':<10} {'Name':<30} {'Price':<10} {'Sector':<20}")
        print("-" * 70)
        for stock in result["comparison"]:
            if "error" not in stock:
                print(f"{stock['symbol']:<10} {stock['name']:<30} "
                      f"${stock['price']:<9.2f} {stock['sector']:<20}")
    print()


async def demo_search(client: MCPStockClient):
    """Demo stock search"""
    print("=" * 70)
    print("STOCK SEARCH")
    print("=" * 70)
    print()
    
    queries = ["Apple", "Technology", "Tesla"]
    
    for query in queries:
        print(f"Search: '{query}'")
        result = await client.execute_tool("search_stocks", query=query)
        print(f"Found {result.get('count', 0)} results:")
        for stock in result.get("results", []):
            print(f"  - {stock['symbol']}: {stock['name']} (${stock['price']})")
        print()


async def main():
    """Main demo function"""
    # Import the server
    from mcp_stock_server import MCPStockServer
    
    print("=" * 70)
    print("MCP Stock Client Demo")
    print("=" * 70)
    print()
    
    # Initialize server and client
    server = MCPStockServer()
    client = MCPStockClient(server)
    
    print(f"Connected to: {server.name} v{server.version}")
    print()
    
    # Run demos
    await demo_basic_operations(client)
    await demo_advanced_operations(client)
    await demo_comparison(client)
    await demo_search(client)
    
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(main())

# Made with Bob
