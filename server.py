"""
MCP Server with Custom Tools

This server provides tools for user management and scheduling using FastMCP.
It can be used with:
1. Claude Desktop (via claude_desktop_config.json)
2. Python clients (like client.py)
3. MCP Inspector (for debugging)

Available Tools:
- get_users_by_name: Get user details by name
- get_all_user: Get all users in database
- get_user_schedule: Get schedule for a specific user
"""

from mcp.server.fastmcp import FastMCP
import sys

# ============================================================================
# INITIALIZE MCP SERVER
# ============================================================================
# Create MCP server instance with a descriptive name
mcp = FastMCP("my first mcp server")

# ============================================================================
# DATABASE (In-Memory)
# ============================================================================
# In a real application, this would be a proper database (PostgreSQL, MongoDB, etc.)
# For demonstration, we use simple Python lists and dictionaries

# User Database - stores user information
user_DB = [
    {"id": 1, "name": "kishan", "role": "admin"},
    {"id": 2, "name": "neel", "role": "user"},
    {"id": 3, "name": "pritam", "role": "user"},
    {"id": 4, "name": "rahul", "role": "user"}
]

# Schedule Database - stores user schedules
schedules_db = [
    {"name": "kishan", "schedule": ["9:00 AM - Team Meeting", "2:00 PM - Code Review"]},
    {"name": "neel", "schedule": ["10:00 AM - Client Call", "4:00 PM - Report Writing"]},
    {"name": "pritam", "schedule": ["11:00 AM - Project Update", "3:00 PM - Testing"]}
]

# Log server initialization to stderr (won't interfere with MCP protocol on stdout)
print("server is inittialising", file=sys.stderr)

# ============================================================================
# MCP TOOLS
# ============================================================================
# Tools are functions decorated with @mcp.tool() that can be called by AI models
# Each tool should have a clear docstring describing what it does

@mcp.tool()
def get_users_by_name(name: str) -> str:
    """
    Get the user detail from the username.

    This tool searches the user database for a user with the given name
    and returns their complete information (id, name, role).

    Args:
        name: The username to search for (case-insensitive)

    Returns:
        A string with user details if found, or "User not found" message

    Example:
        Input: "kishan"
        Output: "User found its detail is {'id': 1, 'name': 'kishan', 'role': 'admin'}"
    """
    # Search through all users
    for user in user_DB:
        # Case-insensitive comparison
        if user['name'].lower() == name.lower().strip():
            # Debug log (goes to stderr, not MCP protocol)
            print("User found its detail is " + str(user))
            return "User found its detail is " + str(user)

    return "User not found"


@mcp.tool()
def get_all_user():
    """
    Get all user details from the database.

    This tool returns the complete list of all users in the system.
    Useful for queries like "show me all users" or "who are the team members".

    Returns:
        List of all user dictionaries

    Example:
        Output: [{'id': 1, 'name': 'kishan', 'role': 'admin'}, ...]
    """
    # Debug log
    print("All user detail called")
    return user_DB


@mcp.tool()
def get_user_schedule(name: str) -> str:
    """
    Get User schedule for a specific user.

    This tool retrieves the daily schedule for a given user.
    Returns their list of scheduled activities with times.

    Args:
        name: The username to get schedule for (case-insensitive)

    Returns:
        A string with the user's schedule if found, or "Schedule not found" message

    Example:
        Input: "kishan"
        Output: "User Kishan schedule is ['9:00 AM - Team Meeting', '2:00 PM - Code Review']"
    """
    # Search through all schedules
    for schedule in schedules_db:
        # Case-insensitive comparison
        if schedule['name'].lower() == name.lower().strip():
            # Debug log
            print("User found its schedule is " + str(schedule['schedule']))
            return f"User {name.capitalize()} schedule is {schedule['schedule']}"

    return f"Schedule not found for user {name}"


# ============================================================================
# SERVER ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Start the MCP server
    # This will listen for requests via stdio (standard input/output)
    mcp.run()
