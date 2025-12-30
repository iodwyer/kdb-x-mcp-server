import logging
import pykx as kx
from typing import Dict, Any, TypedDict
from datetime import date

from mcp_server.utils.kdbx import get_kdb_connection

logger = logging.getLogger(__name__)

# Define QueryParams TypedDict at module level
QueryParams = TypedDict("QueryParams", {
    "sd": date,
    "ed": date,
    "tickers": str | list[str],
    "minPrice": float,
    "maxPrice": float
})

async def api_complex_query_impl(params: QueryParams) -> Dict[str, Any]:
    try:
        conn = get_kdb_connection()

        result = conn.mcp.apiCall('.api.complex', params)
        if 0==len(result):
            return {"status": "success", "data": [], "message": "No rows returned"}

        # rows = result.py()
        rows = result.pd()

        logger.info(f"Query returned {len(rows)} rows.")
        return {"status": "success", "data": rows}

    except Exception as e:
        logger.error(f"Query failed: {e}")
        return {"status": "error", "message": str(e)}


def register_tools(mcp_server):
    @mcp_server.tool()
    async def kdbx_run_api_complex(params: QueryParams) -> dict:
        """
        Query price data for one or more tickers within a date and price range.

        This API retrieves records matching the supplied date range, tickers,
        and optional price constraints.

        Args:
            params (QueryParams): Dictionary of query parameters with the
                following keys:
                
                - sd (date): Start date (inclusive)
                - ed (date): End date (inclusive)
                - tickers (str | list[str]): One ticker symbol or a list of
                ticker symbols to query (e.g. "AAPL" or ["AAPL", "MSFT"]).
                - minPrice (float): Minimum price filter (inclusive).
                - maxPrice (float): Maximum price filter (inclusive).

        Returns:
            Dict[str, Any]: A dictionary containing the query results and
            metadata such as record count or status information.

        Raises:
            ValueError: If required parameters are missing or invalid.
        """
        return await api_complex_query_impl(params)

    return ['kdbx_run_api_complex']