# MCP Stock Server Example

A comprehensive example of implementing a **Model Context Protocol (MCP)** server in Python for stock market data operations.

## 📋 Overview

This example demonstrates how to build an MCP server that provides stock market data tools. It includes:

- **MCP Server** (`mcp_stock_server.py`) - Implements the MCP protocol with stock data tools
- **MCP Client** (`mcp_stock_client.py`) - Demonstrates how to interact with the server
- **5 Stock Tools** - Price lookup, info retrieval, historical data, comparison, and search

## 🎯 What is MCP?

**Model Context Protocol (MCP)** is a standardized protocol that allows AI models to interact with external tools and data sources. It provides:

- **Tool Discovery** - Models can discover available tools
- **Structured Calling** - Tools have well-defined schemas
- **Type Safety** - Input/output validation
- **Extensibility** - Easy to add new tools

## 🚀 Features

### Available Tools

1. **get_stock_price** - Get current stock price
   - Input: `symbol` (string)
   - Output: Price, currency, timestamp

2. **get_stock_info** - Get detailed stock information
   - Input: `symbol` (string)
   - Output: Name, sector, price, volume, market cap, P/E ratio

3. **get_historical_prices** - Get historical price data
   - Input: `symbol` (string), `days` (integer, default: 7)
   - Output: Array of daily OHLCV data

4. **compare_stocks** - Compare multiple stocks
   - Input: `symbols` (array of strings)
   - Output: Side-by-side comparison

5. **search_stocks** - Search by sector or name
   - Input: `query` (string)
   - Output: Matching stocks with details

### Advanced Client Features

- **Portfolio Summary** - Aggregate portfolio statistics
- **Sector Analysis** - Analyze all stocks in a sector
- **Performance Tracking** - Track stock performance over time with trend analysis

## 📦 Installation

No external dependencies required! Uses only Python standard library:

```bash
# Clone or download the files
# No pip install needed!
```

## 🎮 Usage

### Run the Server Demo

```bash
python3 mcp_stock_server.py
```

This will demonstrate all 5 tools with example calls.

### Run the Client Demo

```bash
python3 mcp_stock_client.py
```

This shows:
- Basic operations (price lookup, stock info)
- Advanced operations (portfolio, sector analysis, performance tracking)
- Stock comparison
- Search functionality

### Use in Your Code

```python
import asyncio
from mcp_stock_server import MCPStockServer
from mcp_stock_client import MCPStockClient

async def main():
    # Initialize server and client
    server = MCPStockServer()
    client = MCPStockClient(server)
    
    # Get stock price
    result = await client.execute_tool("get_stock_price", symbol="AAPL")
    print(f"Apple stock: ${result['price']}")
    
    # Get portfolio summary
    portfolio = await client.get_portfolio_summary(["AAPL", "GOOGL", "MSFT"])
    print(f"Portfolio value: ${portfolio['total_value']}")
    
    # Analyze sector
    tech_analysis = await client.analyze_sector("Technology")
    print(f"Tech sector average: ${tech_analysis['average_price']}")

asyncio.run(main())
```

## 🏗️ Architecture

### MCP Server Structure

```python
class MCPStockServer:
    def __init__(self):
        self.name = "stock-data-server"
        self.version = "1.0.0"
        self.tools = self._register_tools()
    
    def _register_tools(self):
        """Register tools with schemas"""
        return [
            {
                "name": "tool_name",
                "description": "What it does",
                "inputSchema": {
                    "type": "object",
                    "properties": {...},
                    "required": [...]
                }
            }
        ]
    
    async def call_tool(self, tool_name, arguments):
        """Execute tool calls"""
        # Route to appropriate handler
```

### Tool Schema Format

Each tool follows this structure:

```json
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
}
```

## 📊 Example Output

### Get Stock Price

```json
{
  "symbol": "AAPL",
  "price": 180.41,
  "currency": "USD",
  "timestamp": "2026-02-22T15:25:14.942488"
}
```

### Get Stock Info

```json
{
  "symbol": "TSLA",
  "name": "Tesla Inc.",
  "sector": "Automotive",
  "current_price": 247.62,
  "day_high": 255.05,
  "day_low": 240.2,
  "volume": 97021141,
  "market_cap": "$2081B",
  "pe_ratio": 31.82
}
```

### Portfolio Summary

```json
{
  "portfolio": [...],
  "total_stocks": 3,
  "total_value": 706.62,
  "average_price": 235.54
}
```

### Sector Analysis

```json
{
  "sector": "Technology",
  "stock_count": 5,
  "average_price": 411.9,
  "highest_price": 875.3,
  "lowest_price": 142.3,
  "price_range": 733.0
}
```

## 🔧 Customization

### Add New Stocks

Edit the `STOCK_DATABASE` in `mcp_stock_server.py`:

```python
STOCK_DATABASE = {
    "AAPL": {"name": "Apple Inc.", "sector": "Technology", "price": 178.50},
    "YOUR_SYMBOL": {"name": "Company Name", "sector": "Sector", "price": 100.00},
}
```

### Add New Tools

1. Register the tool in `_register_tools()`:

```python
{
    "name": "your_tool_name",
    "description": "What it does",
    "inputSchema": {...}
}
```

2. Implement the handler method:

```python
async def your_tool_name(self, param1: str) -> Dict[str, Any]:
    # Implementation
    return {"result": "data"}
```

3. Add routing in `call_tool()`:

```python
elif tool_name == "your_tool_name":
    return await self.your_tool_name(arguments["param1"])
```

### Connect to Real APIs

Replace simulated data with real API calls:

```python
# Example with yfinance
import yfinance as yf

async def get_stock_price(self, symbol: str):
    ticker = yf.Ticker(symbol)
    data = ticker.history(period="1d")
    return {
        "symbol": symbol,
        "price": float(data['Close'].iloc[-1]),
        "currency": "USD",
        "timestamp": datetime.now().isoformat()
    }
```

## 🎓 Learning Points

### MCP Concepts Demonstrated

1. **Tool Registration** - How to define tools with schemas
2. **Type Safety** - Input validation through schemas
3. **Async Operations** - All operations are async for scalability
4. **Error Handling** - Graceful error responses
5. **Tool Discovery** - Clients can list available tools
6. **Structured Responses** - Consistent JSON output format

### Best Practices

- ✅ Use descriptive tool names and descriptions
- ✅ Define clear input schemas with types
- ✅ Provide helpful error messages
- ✅ Return consistent response formats
- ✅ Use async/await for I/O operations
- ✅ Validate inputs before processing
- ✅ Document all parameters and return values

## 🔍 How It Works

### Tool Call Flow

```
1. Client discovers available tools
   ↓
2. Client selects tool and prepares arguments
   ↓
3. Client calls server.call_tool(name, args)
   ↓
4. Server validates arguments against schema
   ↓
5. Server routes to appropriate handler
   ↓
6. Handler processes request and returns data
   ↓
7. Client receives structured response
```

### Example Flow

```python
# 1. Client discovers tools
tools = client.list_available_tools()
# ['get_stock_price', 'get_stock_info', ...]

# 2. Client prepares call
tool_name = "get_stock_price"
arguments = {"symbol": "AAPL"}

# 3. Client executes
result = await client.execute_tool(tool_name, **arguments)

# 4. Server validates and processes
# 5. Client receives result
print(result)  # {"symbol": "AAPL", "price": 180.41, ...}
```

## 🚀 Next Steps

### Enhancements to Try

1. **Add More Tools**
   - Stock alerts/notifications
   - Technical indicators (RSI, MACD)
   - News sentiment analysis
   - Dividend information

2. **Improve Data**
   - Connect to real APIs (yfinance, Alpha Vantage)
   - Add caching for performance
   - Implement rate limiting

3. **Add Features**
   - WebSocket support for real-time updates
   - Authentication and authorization
   - Multi-currency support
   - Watchlist management

4. **Production Ready**
   - Add logging
   - Implement proper error handling
   - Add unit tests
   - Create Docker container

## 📚 Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Python Async Programming](https://docs.python.org/3/library/asyncio.html)
- [JSON Schema](https://json-schema.org/)

## 📝 License

This is an educational example. Feel free to use and modify for your projects!

## 🤝 Contributing

This is a learning example. Suggestions for improvements are welcome!

---

**Made with Bob** 🤖