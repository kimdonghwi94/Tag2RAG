from fastmcp.tools import Tool


@Tool.from_function
async def page_intro(url: str) -> str:
    """Return a one-line introduction of the web page."""
    return ""
