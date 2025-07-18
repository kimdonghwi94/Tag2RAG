# Web Search MCP

A FastMCP server for web page extraction, analysis, and summarization.

This project provides a robust, scalable, and secure MCP server built with FastMCP and FastAPI. It includes features like JWT authentication, Redis caching, Prometheus monitoring, and dynamic resource generation.

## Features

- **Web Crawling**: Traverses a website to find all sub-pages.
- **Metadata Extraction**: Pulls one-line descriptions from web pages.
- **Content Summarization**: Summarizes page content for RAG models.
- **Dynamic Reports**: Generates reports on the fly via a resource URI.
- **Authentication**: Secured endpoints using JWT.
- **Caching**: Redis-backed caching for improved performance.
- **Monitoring**: Built-in metrics for Prometheus and Grafana.
- **Containerized**: Ready to run with Docker and Docker Compose.

## Getting Started

For detailed instructions on setup, usage, and API documentation, please refer to the [official documentation](./docs/build/html/index.html).

(You will need to build the docs first using Sphinx)
```bash
cd docs
make html
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
