"""Placeholder tool implementations for the WebSearchMCP."""

from fastmcp.tools import Tool
import httpx


@Tool.from_function
async def list_pages(url: str) -> list[str]:
    """Explore subpages of the given URL and return a list.

    TODO: implement the actual crawling algorithm.
    """
    # Placeholder implementation
    async with httpx.AsyncClient() as client:
        await client.get(url)
    return []


@Tool.from_function
async def page_intro(url: str) -> str:
    """Return a one-line introduction of the web page."""
    return ""


@Tool.from_function
async def page_summary(url: str) -> str:
    """Return a summary for RAG input."""
    return ""
