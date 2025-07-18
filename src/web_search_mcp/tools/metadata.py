from fastmcp import tool

@tool
async def get_metadata(url: str) -> str:
    """
    Extracts a one-line description from a given web page URL.
    This typically comes from the meta description tag.

    :param url: The URL of the web page.
    :return: A one-line string description of the page.
    """
    # NOTE: The user will implement the actual metadata extraction logic here.
    # This is a placeholder implementation.
    print(f"Getting metadata for: {url}")
    # Example logic:
    # 1. Fetch the page content.
    # 2. Use BeautifulSoup or lxml to parse the HTML.
    # 3. Find the '<meta name="description" content="...">' tag.
    # 4. Return the content attribute.
    return f"This is a one-line summary for the page at {url}."