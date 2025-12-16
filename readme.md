# MCP (Model Context Protocol) Server & Client

A Python implementation of an MCP server with custom tools and a Gemini AI-powered client that can interact with those tools.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Available Tools](#available-tools)
- [Troubleshooting](#troubleshooting)

## 🎯 Overview

This project demonstrates how to:
1. Create a custom MCP server with tools using FastMCP
2. Build a Python client that uses Google's Gemini AI to interact with MCP tools
3. Integrate MCP server with Claude Desktop for AI-powered interactions

## ✨ Features

- **MCP Server** with custom tools for user management and scheduling
- **Gemini AI Client** with automatic tool calling and retry logic
- **Claude Desktop Integration** for seamless AI interactions
- **Rate Limit Handling** with automatic retry mechanism
- **Interactive Chat Interface** for real-time conversations

## 📦 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://ai.google.dev/))
- Claude Desktop (optional, for Claude integration)

## 🚀 Installation

### 1. Clone or Download the Project

```bash
cd /Users/kishan/Desktop/MCP/MCP_Python
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Create virtual environment
python3 -m venv MCp

# Activate virtual environment
# On macOS/Linux:
source MCp/bin/activate

# On Windows:
# MCp\Scripts\activate
```

### 3. Install Required Dependencies

```bash
# Install all required packages
pip install mcp google-generativeai python-dotenv
```

**Required Packages:**
- `mcp` - Model Context Protocol library
- `google-generativeai` - Google Gemini AI SDK
- `python-dotenv` - Environment variable management

## ⚙️ Configuration

### 1. Set Up Your Gemini API Key

**Option A: Using .env file (Recommended)**
Create a `.env` file in the project directory:
```bash
echo "GEMINI_API_KEY=your_api_key_here" > .env
```

**Option B: Direct in code**
Edit `client.py` line 14 and replace with your API key:
```python
api_key = "YOUR_ACTUAL_API_KEY_HERE"
```

### 2. Configure Claude Desktop (Optional)

To use the MCP server with Claude Desktop:

1. Open Claude Desktop settings
2. Click on "Developer" → "Edit Config"
3. Add the following to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "kishan-server": {
      "command": "python Environment Path",
      "args": [
        "your server.py file Path with server.py"
      ]
    }
  }
}
```

4. Restart Claude Desktop

## 🎮 Usage

### Running the MCP Server (Standalone)

```bash
# Make sure virtual environment is activated
source MCp/bin/activate

# Run the server
python3 server.py
```

### Running the Gemini Client

```bash
# Make sure virtual environment is activated
source MCp/bin/activate

# Run the client
python3 client.py
```

**Example Interaction:**
```
🔌 Connecting to MCP Server...
🛠️  Server provided tools: ['get_users_by_name', 'get_all_user', 'get_user_schedule']

👤 You: What is kishan's schedule?
🤖 Gemini wants to call: get_user_schedule({'name': 'kishan'})
📦 Tool Output: User Kishan schedule is ['9:00 AM - Team Meeting', '2:00 PM - Code Review']
🤖 AI: Kishan has a team meeting at 9:00 AM and a code review at 2:00 PM.
----------------------------------------

👤 You: exit
```

### Testing API Connection

```bash
python3 check_models.py
```

This will verify your Gemini API key is working correctly.

### Using MCP Inspector (Debugging)

```bash
npx @modelcontextprotocol/inspector python server.py
```

This opens a web interface to test your MCP server tools. it check you tools one by one and check proper response or not is there any error in the local server, you can catch that here.

## 📁 Project Structure

```
MCP_Python/
├── server.py              # MCP server with custom tools
├── client.py              # Gemini AI client
├── check_models.py        # API connection tester
├── .env                   # Environment variables (create this)
├── README.md              # This file
└── MCp/                   # Virtual environment folder
```

## 🛠️ Available Tools

### 1. `get_users_by_name(name: str)`
Get user details by username.

**Example:** "Get details for kishan"

### 2. `get_all_user()`
Retrieve all users in the database.

**Example:** "Show me all users"

### 3. `get_user_schedule(name: str)`
Get a user's schedule.

**Example:** "What is neel's schedule?"

## 🔧 Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'mcp'`
**Solution:** Make sure you've activated the virtual environment and installed dependencies:
```bash
source MCp/bin/activate
pip install mcp google-generativeai
```

### Issue: `429 ResourceExhausted` (Rate Limit)
**Solution:** The client has automatic retry logic. Wait 10-60 seconds and it will retry automatically.

### Issue: `404 Model Not Found`
**Solution:** Update the model name in `client.py` line 71:
```python
model_name='gemini-2.5-flash-lite'  # or 'gemini-2.0-flash'
```

### Issue: API Key Invalid
**Solution:**
1. Verify your API key at [Google AI Studio](https://ai.google.dev/)
2. Check that the key is correctly set in `.env` or `client.py`

### Issue: Claude Desktop Not Detecting Server
**Solution:**
1. Verify the paths in `claude_desktop_config.json` are absolute paths
2. Restart Claude Desktop completely
3. Check that the Python path points to your virtual environment

## 📝 Notes

- The server contains sample data for demonstration (users and schedules)
- You can add more tools by using the `@mcp.tool()` decorator in `server.py`
- The client uses `gemini-2.5-flash-lite` by default for cost efficiency
- Rate limits are handled automatically with 3 retry attempts

## 🤝 Contributing

Feel free to add more tools or improve the existing implementation!

## 📄 License

This project is for educational purposes.

---

**Quick Start Commands:**
```bash
# Setup
python3 -m venv MCp
source MCp/bin/activate
pip install mcp google-genai python-dotenv
-> as official mention or you can use
pip install mcp google-generativeai python-dotenv
# Run
python3 client.py
```
