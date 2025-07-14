from __future__ import annotations

import os
from contextlib import asynccontextmanager

import redis.asyncio as redis
from fastmcp.server import FastMCP
from fastmcp.server.auth.providers.bearer_env import EnvBearerAuthProvider

from tools.crawler import list_pages
from tools.metadata import page_intro
from tools.summarizer import page_summary
from resources.report import generate_report


@asynccontextmanager
async def lifespan(app: FastMCP):
    """Manage application lifespan and shared resources."""
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    r = redis.from_url(redis_url)
    try:
        yield {"redis": r}
    finally:
        await r.aclose()


def create_server() -> FastMCP:
    """Create and configure the FastMCP server."""
    app = FastMCP(
        name="WebSearchMCP",
        instructions="웹 페이지 추출 및 요약 MCP",
        auth=EnvBearerAuthProvider(),
        lifespan=lifespan,
        cache_expiration_seconds=300,
    )

    app.add_tool(list_pages)
    app.add_tool(page_intro)
    app.add_tool(page_summary)

    app.resource("data://reports/{report_id}")(generate_report)

    return app


def main() -> None:
    app = create_server()
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app.run("http", host=host, port=port)


if __name__ == "__main__":
    main()
