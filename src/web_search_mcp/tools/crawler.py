from fastmcp import tool

@tool
async def crawl_site(url: str) -> list[str]:
    """
    Crawls a website starting from the given URL and returns a list of all found sub-page URLs.
    
    :param url: The starting URL to crawl.
    :return: A list of unique URLs found on the site.
    """
    # NOTE: The user will implement the actual crawling logic here.
    # This is a placeholder implementation.
    print(f"Crawling site: {url}")
    # Example logic:
    # 1. Fetch the initial page.
    # 2. Parse for links.
    # 3. Recursively visit links on the same domain.
    # 4. Keep track of visited URLs to avoid loops.
    return [
        f"{url}/page1",
        f"{url}/page2",
        f"{url}/page3",
    ]