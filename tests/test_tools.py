import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock

from src.web_mcp.tools.crawler import WebCrawlerTool
from src.web_mcp.tools.metadata import MetadataExtractorTool
from src.web_mcp.tools.summarizer import SummarizerTool


@pytest.fixture
def crawler_tool():
    return WebCrawlerTool()


@pytest.fixture
def metadata_tool():
    return MetadataExtractorTool()


@pytest.fixture
def summarizer_tool():
    return SummarizerTool()


class TestWebCrawlerTool:
    """Test cases for WebCrawlerTool."""
    
    @pytest.mark.asyncio
    async def test_list_pages_invalid_url(self, crawler_tool):
        """Test list_pages with invalid URL."""
        result = await crawler_tool.list_pages("invalid-url")
        
        assert result["success"] is False
        assert "Invalid URL format" in result["error"]
    
    @pytest.mark.asyncio
    async def test_list_pages_valid_url_structure(self, crawler_tool):
        """Test list_pages return structure with valid URL."""
        # Mock the _discover_pages method to avoid actual HTTP requests
        with patch.object(crawler_tool, '_discover_pages') as mock_discover:
            mock_discover.return_value = [
                {
                    "url": "https://example.com",
                    "status": "success",
                    "title": "Example Page",
                    "content_length": 5000
                }
            ]
            
            result = await crawler_tool.list_pages("https://example.com")
            
            assert result["success"] is True
            assert "start_url" in result
            assert "summary" in result
            assert "pages" in result
            assert "successful_pages" in result
            assert "failed_pages" in result
    
    @pytest.mark.asyncio
    async def test_fetch_page_timeout(self, crawler_tool):
        """Test _fetch_page with timeout."""
        with patch('httpx.AsyncClient') as mock_client:
            mock_session = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_session
            mock_session.get.side_effect = asyncio.TimeoutError()
            
            result = await crawler_tool._fetch_page(mock_session, "https://example.com")
            
            assert result["status"] == "timeout"
            assert result["reason"] == "Request timeout"


class TestMetadataExtractorTool:
    """Test cases for MetadataExtractorTool."""
    
    @pytest.mark.asyncio
    async def test_extract_page_intro_invalid_url(self, metadata_tool):
        """Test extract_page_intro with invalid URL."""
        result = await metadata_tool.extract_page_intro("invalid-url")
        
        assert result["success"] is False
        assert "Invalid URL format" in result["error"]
    
    @pytest.mark.asyncio
    async def test_extract_page_intro_structure(self, metadata_tool):
        """Test extract_page_intro return structure."""
        mock_html = """
        <html>
            <head>
                <title>Test Page</title>
                <meta name="description" content="Test description">
            </head>
            <body>
                <h1>Main Heading</h1>
                <p>This is test content for the page.</p>
            </body>
        </html>
        """
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_session = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_session
            
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = mock_html.encode()
            mock_response.headers = {'content-type': 'text/html'}
            mock_response.raise_for_status.return_value = None
            mock_session.get.return_value = mock_response
            
            result = await metadata_tool.extract_page_intro("https://example.com")
            
            assert result["success"] is True
            assert "introduction" in result
            assert "metadata" in result
            assert result["metadata"]["title"] == "Test Page"
    
    def test_generate_page_intro(self, metadata_tool):
        """Test _generate_page_intro method."""
        metadata = {
            "title": "Test Page",
            "description": "This is a test page description for testing purposes.",
            "structured_data": {},
            "content_summary": {}
        }
        
        intro = metadata_tool._generate_page_intro(metadata)
        
        assert intro is not None
        assert len(intro) > 0
        assert "This is a test page description" in intro


class TestSummarizerTool:
    """Test cases for SummarizerTool."""
    
    @pytest.mark.asyncio
    async def test_generate_summary_invalid_url(self, summarizer_tool):
        """Test generate_summary with invalid URL."""
        result = await summarizer_tool.generate_summary("invalid-url")
        
        assert result["success"] is False
        assert "Invalid URL format" in result["error"]
    
    @pytest.mark.asyncio
    async def test_generate_summary_structure(self, summarizer_tool):
        """Test generate_summary return structure."""
        mock_html = """
        <html>
            <head>
                <title>Test Article</title>
            </head>
            <body>
                <h1>Main Article Title</h1>
                <p>This is the first paragraph of the article content.</p>
                <p>This is the second paragraph with more detailed information.</p>
                <ul>
                    <li>First important point</li>
                    <li>Second important point</li>
                </ul>
                <p>This is the conclusion paragraph of the article.</p>
            </body>
        </html>
        """
        
        with patch('httpx.AsyncClient') as mock_client:
            mock_session = AsyncMock()
            mock_client.return_value.__aenter__.return_value = mock_session
            
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.content = mock_html.encode()
            mock_response.headers = {'content-type': 'text/html'}
            mock_response.raise_for_status.return_value = None
            mock_session.get.return_value = mock_response
            
            result = await summarizer_tool.generate_summary("https://example.com")
            
            assert result["success"] is True
            assert "rag_data" in result
            assert "summary" in result
            assert "url" in result["rag_data"]
            assert "title" in result["rag_data"]
            assert "summary" in result["rag_data"]
            assert "key_points" in result["rag_data"]
            assert "keywords" in result["rag_data"]
    
    def test_clean_text(self, summarizer_tool):
        """Test _clean_text method."""
        dirty_text = "  This   is    a   test   text   with   extra   spaces.  "
        clean_text = summarizer_tool._clean_text(dirty_text)
        
        assert clean_text == "This is a test text with extra spaces."
    
    def test_extract_key_sections(self, summarizer_tool):
        """Test _extract_key_sections method."""
        from bs4 import BeautifulSoup
        
        html = """
        <div>
            <h1>Main Title</h1>
            <h2>Subtitle</h2>
            <ul>
                <li>First item</li>
                <li>Second item</li>
            </ul>
            <strong>Important text</strong>
            <a href="https://example.com">Example Link</a>
        </div>
        """
        
        soup = BeautifulSoup(html, 'lxml')
        sections = summarizer_tool._extract_key_sections(soup)
        
        assert "headings" in sections
        assert "lists" in sections
        assert "important_text" in sections
        assert "links" in sections
        assert len(sections["headings"]) >= 2
        assert len(sections["lists"]) >= 1
    
    def test_generate_summary_content(self, summarizer_tool):
        """Test _generate_summary method."""
        content = """
        This is the first sentence of the content. This is the second sentence with more details.
        This is the third sentence that provides additional context. This is the fourth sentence
        that concludes the main points of the content.
        """
        
        sections = {
            "headings": ["H1: Main Title", "H2: Subtitle"],
            "lists": [["First item", "Second item"]],
            "important_text": ["Important text"],
            "links": [{"text": "Example Link", "href": "https://example.com"}]
        }
        
        summary = summarizer_tool._generate_summary(content, sections)
        
        assert "summary_text" in summary
        assert "key_sentences" in summary
        assert "keywords" in summary
        assert "statistics" in summary
        assert summary["statistics"]["word_count"] > 0
        assert len(summary["keywords"]) > 0


@pytest.mark.asyncio
async def test_tools_integration():
    """Integration test for all tools working together."""
    crawler = WebCrawlerTool()
    metadata = MetadataExtractorTool()
    summarizer = SummarizerTool()
    
    # Test that all tools can be instantiated
    assert crawler is not None
    assert metadata is not None
    assert summarizer is not None
    
    # Test invalid URL handling across all tools
    invalid_url = "not-a-valid-url"
    
    crawler_result = await crawler.list_pages(invalid_url)
    metadata_result = await metadata.extract_page_intro(invalid_url)
    summarizer_result = await summarizer.generate_summary(invalid_url)
    
    assert crawler_result["success"] is False
    assert metadata_result["success"] is False
    assert summarizer_result["success"] is False
