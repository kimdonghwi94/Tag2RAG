import pytest
import asyncio
from unittest.mock import AsyncMock, patch

from src.web_mcp.resources.report import ReportResource


@pytest.fixture
def report_resource():
    return ReportResource()


@pytest.mark.asyncio
async def test_site_analysis_report_generation(report_resource):
    """Test site analysis report generation."""
    report_id = "site_analysis_example"
    
    result = await report_resource.generate_report(report_id)
    
    assert result is not None
    assert isinstance(result, str)
    assert "웹사이트 분석 보고서" in result
    assert "기본 정보" in result
    assert "페이지 탐색 결과" in result


@pytest.mark.asyncio
async def test_summary_report_generation(report_resource):
    """Test summary report generation."""
    report_id = "summary_article123"
    
    result = await report_resource.generate_report(report_id)
    
    assert result is not None
    assert isinstance(result, str)
    assert "웹페이지 요약 보고서" in result
    assert "요약" in result
    assert "주요 포인트" in result


@pytest.mark.asyncio
async def test_invalid_report_id(report_resource):
    """Test handling of invalid report ID."""
    report_id = "invalid_format"
    
    result = await report_resource.generate_report(report_id)
    
    assert result is not None
    assert "오류" in result
    assert "잘못된 보고서 ID 형식" in result


@pytest.mark.asyncio
async def test_unsupported_report_type(report_resource):
    """Test handling of unsupported report type."""
    report_id = "unsupported_type_123"
    
    result = await report_resource.generate_report(report_id)
    
    assert result is not None
    assert "오류" in result
    assert "지원하지 않는 보고서 타입" in result


@pytest.mark.asyncio
async def test_report_caching(report_resource):
    """Test report caching functionality."""
    report_id = "site_analysis_cache_test"
    
    # First call - should generate new report
    result1 = await report_resource.generate_report(report_id)
    
    # Second call - should return cached report
    result2 = await report_resource.generate_report(report_id)
    
    assert result1 == result2
    assert report_id in report_resource.reports_cache


def test_site_analysis_report_structure(report_resource):
    """Test the structure of site analysis report."""
    sample_data = {
        "url": "https://example.com",
        "pages": [
            {
                "url": "https://example.com",
                "status": "success",
                "title": "Example Page",
                "description": "Test description",
                "content_length": 5000,
                "internal_links": 10,
                "external_links": 2
            }
        ],
        "metadata": {
            "status_code": 200,
            "content_type": "text/html",
            "content_length": 5000
        }
    }
    
    result = report_resource._generate_site_analysis_report(sample_data)
    
    assert "# 웹사이트 분석 보고서" in result
    assert "https://example.com" in result
    assert "Example Page" in result
    assert "총 발견된 페이지" in result


def test_summary_report_structure(report_resource):
    """Test the structure of summary report."""
    sample_data = {
        "url": "https://example.com/article",
        "rag_data": {
            "title": "Test Article",
            "summary": "This is a test summary of the article content.",
            "key_points": [
                "First key point",
                "Second key point",
                "Third key point"
            ],
            "keywords": ["test", "article", "content", "summary"]
        }
    }
    
    result = report_resource._generate_summary_report(sample_data)
    
    assert "# 웹페이지 요약 보고서" in result
    assert "Test Article" in result
    assert "This is a test summary" in result
    assert "주요 포인트" in result
    assert "First key point" in result
