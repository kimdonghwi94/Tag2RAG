from fastmcp.tools import Tool


@Tool.from_function
async def page_summary(url: str) -> str:
    """Return a summary for RAG input."""
    return ""
