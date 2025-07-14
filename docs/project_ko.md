# Web Search MCP 프로젝트 안내

이 문서는 FastMCP 라이브러리를 활용해 웹 페이지를 탐색하고 요약하는 MCP 서버 프로젝트의 구조와 사용 방법을 설명합니다.

## 주요 기능
- 비동기 작업 처리
- Redis를 이용한 상태 저장
- 외부 API 연동 지원 (`httpx` 사용)
- `data://reports/{report_id}` 형식의 동적 리소스 제공
- Bearer 토큰 인증을 통한 보안 강화

## 프로젝트 구조
```
web-mcp-server/
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── uv.lock
├── .env
├── docs/
│   ├── conf.py
│   ├── index.rst
│   ├── usage.md
│   └── project_ko.md
├── src/
│   ├── server.py
│   ├── tools/
│   │   ├── crawler.py
│   │   ├── summarizer.py
│   │   └── metadata.py
│   ├── resources/
│   │   └── report.py
│   ├── auth/
│   │   └── jwt_handler.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── redis_client.py
│   └── prompts/
│       └── base.py
└── tests/
    ├── test_tools.py
    ├── test_resources.py
    └── test_auth.py
```

## 설치 방법
1. [uv](https://github.com/astral-sh/uv)로 가상환경 생성 후 의존성 설치
```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

2. 로컬 실행
```bash
export FASTMCP_AUTH_BEARER_PUBLIC_KEY=<PUBLIC_KEY>
python -m server
```

3. Docker 사용
```bash
docker compose up --build
```

## 문서화
Sphinx와 MyST-Parser를 사용해 Markdown 기반 문서를 빌드할 수 있습니다.
```bash
cd docs
sphinx-build -b html . _build
```
생성된 HTML 문서는 `docs/_build` 폴더에서 확인할 수 있습니다.

개발자는 `src/tools/` 폴더에서 각 알고리즘을 구현하여 MCP의 기능을 확장할 수 있습니다.
