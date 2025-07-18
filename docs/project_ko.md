# Web Search MCP - 고급 웹 검색 및 분석 MCP 서버

## 프로젝트 개요

Web Search MCP는 FastMCP 라이브러리를 기반으로 구축된 고급 웹 검색 및 분석 MCP(Model Context Protocol) 서버입니다. 이 서버는 웹 페이지 크롤링, 메타데이터 추출, 내용 요약 등의 기능을 제공하여 AI 모델이 웹 콘텐츠를 효과적으로 분석하고 활용할 수 있도록 지원합니다.

## 주요 기능

### 1. 웹 페이지 크롤링 (`list_pages`)
- **기능**: 지정된 URL에서 시작하여 하위 페이지들을 탐색하고 리스트를 추출
- **특징**:
  - 비동기 처리로 빠른 크롤링
  - 깊이 제한 및 페이지 수 제한 지원
  - 중복 URL 방지
  - 도메인 내부 링크 우선 탐색
  - 실패한 페이지에 대한 상세 오류 정보 제공

### 2. 메타데이터 추출 (`extract_page_intro`)
- **기능**: 웹 페이지의 메타데이터를 추출하고 한줄 소개 생성
- **특징**:
  - HTML 메타 태그 분석
  - Open Graph 및 Twitter Card 데이터 추출
  - JSON-LD 구조화된 데이터 파싱
  - 자동 페이지 소개 생성
  - 이미지 및 링크 정보 수집

### 3. 내용 요약 (`generate_summary`)
- **기능**: 웹 페이지 내용을 RAG(Retrieval-Augmented Generation) 입력용으로 요약
- **특징**:
  - 메인 콘텐츠 자동 추출 (광고, 네비게이션 제거)
  - 핵심 문장 및 키워드 추출
  - 구조화된 요약 데이터 생성
  - 다국어 텍스트 정리 및 정규화
  - RAG 시스템에 최적화된 형태로 데이터 구조화

### 4. 동적 보고서 생성
- **기능**: `data://reports/{report_id}` URI를 통한 동적 보고서 생성
- **지원 보고서 타입**:
  - 사이트 분석 보고서 (`site_analysis_*`)
  - 내용 요약 보고서 (`summary_*`)
  - 사용자 정의 보고서 템플릿

## 고급 기능

### 1. 비동기 작업 처리
- **asyncio 기반 비동기 처리**: 모든 웹 요청과 데이터 처리가 비동기로 수행
- **동시 요청 제한**: 설정 가능한 동시 요청 수로 서버 부하 방지
- **타임아웃 관리**: 요청별 타임아웃 설정으로 무한 대기 방지

### 2. 상태 저장 및 캐싱
- **Redis 기반 캐싱**: 자주 요청되는 데이터의 캐싱으로 응답 시간 단축
- **TTL 지원**: 캐시 만료 시간 설정으로 데이터 신선도 유지
- **캐시 통계**: 캐시 히트율 및 사용량 모니터링

### 3. 보안 및 인증
- **다중 인증 방식 지원**:
  - Bearer Token 인증 (환경변수 기반)
  - JWT 토큰 인증
  - API Key 인증
- **요청 제한**: Rate limiting으로 남용 방지
- **입력 검증**: URL 및 매개변수 유효성 검사

### 4. 모니터링 및 로깅
- **Prometheus 메트릭**: 성능 지표 수집 및 모니터링
- **구조화된 로깅**: JSON 형태의 구조화된 로그
- **성능 추적**: 각 작업별 실행 시간 및 성공률 추적

## 기술 스택

### 핵심 라이브러리
- **FastMCP**: MCP 서버 프레임워크
- **FastAPI**: 웹 API 프레임워크
- **httpx**: 비동기 HTTP 클라이언트
- **BeautifulSoup4**: HTML 파싱
- **Redis**: 캐싱 및 세션 저장

### 보안 및 인증
- **python-jose**: JWT 토큰 처리
- **passlib**: 비밀번호 해싱
- **cryptography**: 암호화 기능

### 모니터링 및 로깅
- **structlog**: 구조화된 로깅
- **prometheus-client**: 메트릭 수집
- **uvicorn**: ASGI 서버

## 설치 및 실행

### 1. 환경 설정

```bash
# 저장소 클론
git clone https://github.com/your-org/web-search-mcp.git
cd web-search-mcp

# UV를 사용한 가상환경 생성 및 의존성 설치
uv venv
source .venv/bin/activate  # Linux/Mac
# 또는
.venv\Scripts\activate  # Windows

uv pip install -e .
```

### 2. 환경 변수 설정

`.env` 파일을 생성하고 다음 설정을 추가:

```env
# 서버 설정
HOST=0.0.0.0
PORT=8000
DEBUG=false

# Redis 설정
REDIS_URL=redis://localhost:6379/0
REDIS_PASSWORD=your_redis_password

# 보안 설정
SECRET_KEY=your-super-secret-key-change-in-production
API_KEY=your-api-key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 캐시 설정
CACHE_EXPIRATION_SECONDS=300
MAX_CACHE_SIZE=1000

# 크롤링 설정
MAX_CONCURRENT_REQUESTS=10
REQUEST_TIMEOUT=30
MAX_PAGE_SIZE=10485760  # 10MB
USER_AGENT=WebSearchMCP/0.1.0

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600

# 모니터링
ENABLE_METRICS=true
METRICS_PORT=9090
```

### 3. Redis 서버 실행

```bash
# Docker를 사용한 Redis 실행
docker run -d --name redis -p 6379:6379 redis:alpine

# 또는 로컬 Redis 설치 후 실행
redis-server
```

### 4. 서버 실행

```bash
# 개발 모드
python -m web_mcp.server

# 또는 설치된 명령어 사용
web-search-mcp

# Docker를 사용한 실행
docker-compose up
```

## Docker 지원

### Dockerfile
프로젝트에는 멀티스테이지 Docker 빌드가 포함되어 있습니다:

```dockerfile
FROM python:3.12-slim as builder
# 의존성 설치 및 빌드

FROM python:3.12-slim as runtime
# 런타임 환경 설정
```

### docker-compose.yml
개발 및 프로덕션 환경을 위한 Docker Compose 설정:

```yaml
version: '3.8'
services:
  web-mcp:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - redis
    environment:
      - REDIS_URL=redis://redis:6379/0
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

## API 사용법

### 1. 페이지 크롤링

```python
# MCP 클라이언트를 통한 호출
result = await mcp_client.call_tool(
    "list_pages",
    {
        "url": "https://example.com",
        "max_depth": 2,
        "max_pages": 50
    }
)
```

### 2. 메타데이터 추출

```python
result = await mcp_client.call_tool(
    "extract_page_intro",
    {
        "url": "https://example.com/page"
    }
)
```

### 3. 내용 요약

```python
result = await mcp_client.call_tool(
    "generate_summary",
    {
        "url": "https://example.com/article",
        "max_length": 1000,
        "include_metadata": true
    }
)
```

### 4. 동적 보고서 접근

```python
# 사이트 분석 보고서
report = await mcp_client.get_resource("data://reports/site_analysis_example")

# 요약 보고서
summary_report = await mcp_client.get_resource("data://reports/summary_article123")
```

## 성능 최적화

### 1. 캐싱 전략
- **페이지 캐싱**: 동일한 URL에 대한 반복 요청 캐싱
- **메타데이터 캐싱**: 추출된 메타데이터 캐싱
- **요약 캐싱**: 생성된 요약 데이터 캐싱

### 2. 동시성 제어
- **연결 풀링**: HTTP 클라이언트 연결 재사용
- **요청 배치**: 여러 URL을 배치로 처리
- **백프레셔**: 시스템 부하에 따른 요청 속도 조절

### 3. 메모리 관리
- **스트리밍 처리**: 대용량 페이지의 스트리밍 처리
- **가비지 컬렉션**: 주기적인 메모리 정리
- **리소스 제한**: 최대 페이지 크기 및 처리 시간 제한

## 보안 고려사항

### 1. 입력 검증
- URL 형식 검증
- 허용된 도메인 제한 (선택사항)
- 매개변수 범위 검증

### 2. Rate Limiting
- IP별 요청 제한
- 사용자별 요청 제한
- 전역 요청 제한

### 3. 데이터 보호
- 민감한 정보 필터링
- 로그 데이터 마스킹
- 캐시 데이터 암호화 (선택사항)

## 확장성 고려사항

### 1. 수평 확장
- 무상태 서버 설계
- 로드 밸런서 지원
- 분산 캐시 지원

### 2. 수직 확장
- 멀티프로세싱 지원
- 메모리 사용량 최적화
- CPU 집약적 작업 최적화

### 3. 모니터링
- 성능 메트릭 수집
- 알림 시스템 연동
- 로그 집계 및 분석

## 문제 해결

### 일반적인 문제

1. **Redis 연결 실패**
   - Redis 서버 상태 확인
   - 연결 설정 검증
   - 네트워크 연결 확인

2. **크롤링 실패**
   - 대상 사이트의 robots.txt 확인
   - User-Agent 설정 확인
   - 네트워크 연결 및 DNS 확인

3. **메모리 부족**
   - 최대 페이지 크기 설정 조정
   - 동시 요청 수 감소
   - 캐시 크기 제한

### 로그 분석
구조화된 로그를 통해 문제를 진단할 수 있습니다:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "error",
  "logger": "web_mcp.tools.crawler",
  "message": "Page discovery failed",
  "url": "https://example.com",
  "error": "Connection timeout"
}
```

## 기여 가이드

### 개발 환경 설정

```bash
# 개발 의존성 설치
uv pip install -e ".[dev]"

# 코드 포맷팅
black src/ tests/
isort src/ tests/

# 린팅
flake8 src/ tests/
mypy src/

# 테스트 실행
pytest tests/ -v --cov=src/
```

### 코드 스타일
- **Black**: 코드 포맷팅
- **isort**: import 정렬
- **flake8**: 린팅
- **mypy**: 타입 체킹

### 테스트
- **pytest**: 테스트 프레임워크
- **pytest-asyncio**: 비동기 테스트 지원
- **pytest-cov**: 코드 커버리지

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 지원 및 문의

- **GitHub Issues**: [프로젝트 이슈 페이지](https://github.com/your-org/web-search-mcp/issues)
- **문서**: [프로젝트 문서](https://web-search-mcp.readthedocs.io)
- **이메일**: team@webmcp.dev

## 로드맵

### v0.2.0 (예정)
- [ ] GraphQL API 지원
- [ ] 웹소켓 실시간 업데이트
- [ ] 고급 텍스트 분석 (감정 분석, 키워드 추출)
- [ ] 다국어 지원 강화

### v0.3.0 (예정)
- [ ] 머신러닝 기반 콘텐츠 분류
- [ ] 이미지 분석 및 OCR
- [ ] PDF 및 문서 파일 지원
- [ ] 클러스터링 및 분산 처리

---

*이 문서는 Web Search MCP 프로젝트의 한국어 가이드입니다. 영문 문서는 [README.md](README.md)를 참조하세요.*