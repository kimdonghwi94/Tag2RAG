import asyncio
from mcp_client import McpClient

async def main():
    """
    An example script demonstrating how to use the Web Search MCP server.
    """
    # Initialize the client to connect to the local server
    client = McpClient(base_url="http://localhost:8000")

    # --- Example 1: Use the 'get_metadata' tool ---
    print("--- 1. Getting Metadata ---")
    target_url = "https://context7.com/"
    try:
        metadata = await client.run_tool("get_metadata", {"url": target_url})
        print(f"Metadata for {target_url}:")
        print(metadata)
    except Exception as e:
        print(f"Error getting metadata: {e}")

    print("\n" + "="*30 + "\n")

    # --- Example 2: Use the 'summarize_page' tool ---
    print("--- 2. Summarizing Page ---")
    try:
        summary = await client.run_tool("summarize_page", {"url": target_url})
        print(f"Summary for {target_url}:")
        print(summary)
    except Exception as e:
        print(f"Error summarizing page: {e}")

    print("\n" + "="*30 + "\n")

    # --- Example 3: Access the dynamic 'report' resource ---
    print("--- 3. Accessing Dynamic Report Resource ---")
    report_id = "user123_analysis_456"
    report_uri = f"data://reports/{report_id}"
    try:
        report = await client.get_resource(report_uri)
        print(f"Report for URI {report_uri}:")
        print(report)
    except Exception as e:
        print(f"Error accessing resource: {e}")


if __name__ == "__main__":
    # Note: You need to install the mcp-client library first
    # pip install mcp-client
    asyncio.run(main())