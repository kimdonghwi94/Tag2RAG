"""Dynamic resource generation for reports."""


import json

from fastmcp.server.context import Context


def generate_report(report_id: str, ctx: Context) -> bytes:
    """Return a JSON report for the given identifier.

    The actual report creation logic should be implemented here.
    """
    ctx.info(f"Generating report {report_id}")
    data = {"id": report_id, "summary": "TODO"}
    return json.dumps(data).encode("utf-8")
