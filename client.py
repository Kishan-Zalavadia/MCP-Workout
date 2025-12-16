"""
MCP Client with Gemini AI Integration

This client connects to a local MCP server, fetches available tools,
and uses Google's Gemini AI to intelligently call those tools based on user queries.

Features:
- Automatic tool discovery from MCP server
- Gemini AI-powered natural language understanding
- Automatic retry logic for rate limit handling
- Interactive chat interface
"""

import asyncio
import sys
import time
from dotenv import load_dotenv
# MCP Libraries - for connecting to Model Context Protocol servers
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Google Gemini Library - for AI-powered interactions
import google.generativeai as genai
from google.genai import types
from google.generativeai.types import FunctionDeclaration
from google.api_core import exceptions

# ============================================================================
# CONFIGURATION
# ============================================================================

# Get your API key from: https://ai.google.dev/
# Best practice: Use environment variables or .env file you can get data from env for this api key
api_key = "your api Key"
# load_dotenv()  # Load environment variables from .env file
# api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: GEMINI_API_KEY not found.")
    print("Please set your API key in the code or use a .env file.")
    sys.exit(1)

# Configure Gemini with your API key
genai.configure(api_key=api_key)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def sanitize_schema(schema):
    """
    Remove 'title' field from JSON schema recursively.

    The Gemini API doesn't accept the 'title' field in schemas,
    but MCP servers often include it. This function removes it.

    Args:
        schema: Dictionary or other type representing the schema

    Returns:
        Sanitized schema without 'title' fields
    """
    if not isinstance(schema, dict):
        return schema
    return {k: sanitize_schema(v) for k, v in schema.items() if k != "title"}


def send_message_with_retry(chat, message):
    """
    Send a message to Gemini with automatic retry on rate limits.

    Handles 429 (ResourceExhausted) errors by waiting and retrying.
    This is important because free tier has strict rate limits.

    Args:
        chat: Gemini chat session object
        message: Message to send (string or structured content)

    Returns:
        Response from Gemini

    Raises:
        SystemExit: If all retries fail
    """
    max_retries = 3

    for attempt in range(max_retries):
        try:
            return chat.send_message(message)

        except exceptions.ResourceExhausted:
            # Rate limit hit - wait and retry
            wait_time = 10
            print(f"⏳ Quota limit hit (429). Waiting {wait_time}s before retry {attempt + 1}/{max_retries}...")
            time.sleep(wait_time)

        except Exception as e:
            # Other errors - don't retry
            print(f"❌ Unexpected Error: {e}")
            raise e

    # All retries failed
    print("❌ Failed after multiple retries.")
    print("Please wait a few minutes and try again.")
    sys.exit(1)

async def main():
    """
    Main function that orchestrates the MCP client and Gemini AI interaction.

    Flow:
    1. Connect to local MCP server
    2. Fetch available tools from server
    3. Configure Gemini with those tools
    4. Start interactive chat loop
    5. Handle tool calls and responses
    """

    # ========================================================================
    # STEP 1: Configure MCP Server Connection
    # ========================================================================
    server_params = StdioServerParameters(
        command=sys.executable,  # Use current Python interpreter
        args=["server.py"],       # Run server.py as subprocess
        env=None                  # Inherit current environment
    )

    print("🔌 Connecting to MCP Server...")

    # Connect to server using stdio (standard input/output)
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()

            # ================================================================
            # STEP 2: Fetch Available Tools from Server
            # ================================================================
            tools_list = await session.list_tools()
            print(f"🛠️  Server provided tools: {[t.name for t in tools_list.tools]}")

            # ================================================================
            # STEP 3: Convert MCP Tools to Gemini Format
            # ================================================================
            gemini_tools_config = []

            for tool in tools_list.tools:
                # Remove 'title' field that Gemini doesn't accept
                clean_schema = sanitize_schema(tool.inputSchema)

                # Create Gemini-compatible tool declaration
                gemini_tools_config.append(
                    FunctionDeclaration(
                        name=tool.name,
                        description=tool.description,
                        parameters=clean_schema
                    )
                )

            # ================================================================
            # STEP 4: Initialize Gemini Model with Tools
            # ================================================================
            model = genai.GenerativeModel(
                model_name='gemini-2.5-flash-lite',  # Fast, cost-effective model
                tools=gemini_tools_config             # Provide available tools
            )

            # Start chat session with manual function calling
            # (We handle tool execution ourselves for MCP integration)
            chat = model.start_chat(enable_automatic_function_calling=False)

            # user_query = "Who is free today?"
            # print(f"\n👤 User asks: '{user_query}'")

            # 7. SEND MESSAGE (Using our new Retry Logic)
            # response = send_message_with_retry(chat, user_query)

            # ================================================================
            # STEP 5: Interactive Chat Loop
            # ================================================================
            print("\n💬 Chat started! Type 'exit' to quit.\n")

            while True:
                # Get user input
                user_query = input("👤 You: ")

                # Check for exit commands
                if user_query.lower() in ["exit", "quit", "bye", "goodbye"]:
                    print("👋 Goodbye!")
                    break

                # Send user message to Gemini (with retry logic)
                response = send_message_with_retry(chat, user_query)

                # ============================================================
                # STEP 6: Tool Execution Loop
                # ============================================================
                # Keep processing until we get a text response (not a tool call)
                while response.candidates and response.candidates.content.parts:
                    part = response.candidates.content.parts[0]

                    # Check if Gemini wants to call a tool
                    if part.function_call:
                        fc = part.function_call
                        tool_name = fc.name
                        tool_args = fc.args

                        print(f"🤖 Gemini wants to call: {tool_name}({tool_args})")

                        try:
                            # ================================================
                            # Execute the tool via MCP server
                            # ================================================
                            result = await session.call_tool(
                                tool_name,
                                arguments=dict(tool_args)
                            )

                            # Get the tool output
                            tool_output = result.content
                            print(f"📦 Tool Output: {str(tool_output)}")

                            # ================================================
                            # Send tool result back to Gemini
                            # ================================================
                            # Gemini needs to see the result to formulate final answer
                            response = send_message_with_retry(
                                chat,
                                {
                                    "parts": [
                                        {
                                            "function_response": {
                                                "name": tool_name,
                                                "response": {"result": tool_output}
                                            }
                                        }
                                    ]
                                }
                            )

                        except Exception as e:
                            print(f"❌ Error calling tool {tool_name}: {e}")
                            break

                    else:
                        # ====================================================
                        # No more tool calls - display final answer
                        # ====================================================
                        try:
                            # Extract text response from Gemini
                            text_ans = response.text
                            print(f"🤖 AI: {text_ans}")

                        except ValueError:
                            # Handle case where AI returns empty response
                            print("🤖 AI: [Task completed, but the AI sent no text summary]")

                        print("-" * 40)
                        break

if __name__ == "__main__":
    asyncio.run(main())
