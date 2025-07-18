import asyncio
from fastmcp import Resource
from typing import Dict, Any

class ReportResource(Resource):
    """
    A dynamic resource that generates reports based on a report_id.
    The URI format is `data://reports/{report_id}`.
    """
    SCHEME = "data"
    NAME = "reports"

    async def get(self, report_id: str) -> Dict[str, Any]:
        """
        Generates and returns a report for the given report_id.
        
        :param report_id: The unique identifier for the report.
        :return: A dictionary containing the report data.
        """
        # NOTE: The user will implement the actual report generation logic.
        # This could involve fetching data from a database or another service
        # based on the report_id.
        print(f"Generating report for report_id: {report_id}")
        
        # Simulate an async operation, e.g., a database query
        await asyncio.sleep(1) 
        
        return {
            "report_id": report_id,
            "title": f"Analysis Report for {report_id}",
            "content": "This is the dynamically generated content of the report.",
            "status": "completed",
        }