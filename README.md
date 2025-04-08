# MCP (Model Context Protocol) Server

## Project Structure
```
├── client.py             # Client-side interaction script
├── server.py             # Main MCP server implementation
├── pg_connect.py         # PostgreSQL database connection
├── lm_config.py          # Language model configuration
│
├── .env.example          # Example environment configuration
├── .env.dev              # Development environment configuration
├── requirements.txt      # Project dependencies
└── .gitignore            # Git ignore file
```

## Prerequisites
- Python 3.10+
- PostgreSQL
- API access to AI providers (Anthropic, Google)

## Installation

### 1. Clone the Repository
```bash
git https://github.com/VajraM-dev/Postgres-MCP-Server-With-SSE-Transport.git
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
1. Copy `.env.example` to `.env.dev`
2. Fill in the required configuration:

```bash
cp .env.example .env.dev
nano .env.dev  # or use your preferred text editor
```

#### Configuration Parameters
- `POSTGRES_USERNAME`: PostgreSQL database username
- `POSTGRES_PASSWORD`: PostgreSQL database password
- `POSTGRES_DB_NAME`: Database name
- `POSTGRES_HOST`: Database host
- `POSTGRES_PORT`: Database port
- `MCP_NAME`: Server name
- `MCP_HOST`: Server host
- `MCP_PORT`: Server port
- `TRANSPORT`: Communication transport (sse/stdio)
- `ANTHROPIC_API_KEY`: Anthropic API key
- `GOOGLE_API_KEY`: Google API key
- `USE_PROVIDER`: Default AI provider

## Running the Server

### Development Mode
```bash
python server.py
```

### Client Interaction
```bash
python client.py
```

## Key Features
- 🔒 Secure configuration management
- 🗃️ PostgreSQL database integration
- 🤖 Multi-provider AI model support
- 📡 Flexible communication transport
- 🛡️ Extensible tool registration

## Supported AI Providers
- Anthropic (Claude models)
- Google (Gemini models)

## Tools and Endpoints

### Available Tools
- `list_tables()`: Retrieve database tables
- Custom tools can be easily added via decorators

### Endpoints
- `/sse`: Server-Sent Events endpoint
- Customizable routing and tool registration

## Extending the Framework

### Adding New Tools
```python
@app.tool()
def custom_tool():
    """Custom tool implementation"""
    # Your tool logic here
```

### Configuring AI Providers
Modify `lm_config.py` to add or configure new AI providers.