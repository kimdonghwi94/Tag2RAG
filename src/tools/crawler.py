from fastmcp.tools import Tool
import httpx


@Tool.from_function
async def list_pages(url: str) -> list[str]:
    """Explore subpages of the given URL and return a list.

    TODO: implement the actual crawling algorithm.
    """
    async with httpx.AsyncClient() as client:
        await client.get(url)
    return []
