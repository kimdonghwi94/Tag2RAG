import uvicorn
from fastapi import FastAPI, Depends
from fastmcp import McpServer
from prometheus_fastapi_instrumentator import Instrumentator

from .auth.jwt_auth import get_current_user
from .config import settings
from .core.cache import redis_cache
from .resources.report import ReportResource
from .tools.crawler import crawl_site
from .tools.metadata import get_metadata
from .tools.summarizer import summarize_page

# Create the MCP Server instance
mcp_server = McpServer(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
)

# Create the FastAPI app
app: FastAPI = mcp_server.app

# --- Register Tools and Resources ---
# The user will implement the actual logic for these.
mcp_server.register_tool(crawl_site)
mcp_server.register_tool(get_metadata)
mcp_server.register_tool(summarize_page)
mcp_server.register_resource(ReportResource())

# --- Add Advanced Features ---

# 1. Caching (Example for a specific tool)
@app.post("/tools/get_metadata_cached")
async def get_metadata_cached(url: str):
    cache_key = f"metadata:{url}"
    if cached := await redis_cache.get(cache_key):
        return cached
    result = await get_metadata.run(url=url)
    await redis_cache.set(cache_key, result, expire=3600) # Cache for 1 hour
    return result

# 2. Security (Example for a protected endpoint)
@app.get("/secure-data")
async def secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": "This is secure data", "user": current_user}

# 3. Monitoring
Instrumentator().instrument(app).expose(app)

# --- Main entry point for uvicorn ---
def main():
    uvicorn.run(
        "web_search_mcp.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
    )

if __name__ == "__main__":
    main()