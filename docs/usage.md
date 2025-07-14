# Web Search MCP 서버

이 프로젝트는 FastMCP 라이브러리를 사용하여 웹 페이지를 탐색하고 요약하는 MCP 서버의 예제입니다.

## 특징
- 비동기 작업 처리
- Redis 기반 상태 저장
- 외부 API 연동을 위한 `httpx` 사용
- `data://reports/{report_id}` 형태의 동적 리소스
- Bearer 토큰 인증 지원
- Docker 이미지 제공

## 설치
1. [uv](https://github.com/astral-sh/uv) 로 가상환경 생성
```bash
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 실행
```bash
export FASTMCP_AUTH_BEARER_PUBLIC_KEY=<PUBLIC_KEY>
python -m server
```

## Docker 사용
```bash
docker build -t web-mcp .
docker run -p 8000:8000 -e FASTMCP_AUTH_BEARER_PUBLIC_KEY=<PUBLIC_KEY> web-mcp
```

## 제공되는 툴
- `list_pages(url)` : 하위 페이지를 재귀적으로 탐색하여 URL 목록을 반환합니다.
- `page_intro(url)` : 해당 페이지의 한 줄 소개를 반환합니다.
- `page_summary(url)` : RAG 입력을 위한 요약을 생성합니다.

각 알고리즘의 상세 로직은 `src/tools/` 폴더에서 구현하면 됩니다.
